# server/tcp_server.py

import asyncio
from protocol.codec import decode_line, encode, ProtocolError
from protocol import constants as C

# Timeout (seconds) to wait for the peer server's NAME-CHECK-REPLY
NAME_CHECK_TIMEOUT = 3.0

handlers = {}


def register_handler(op):
    def wrapper(fn):
        handlers[op] = fn
        return fn
    return wrapper


def _send(ctx, writer, msg):
    """Encode, log, and write a response."""
    ctx.log.info(f"TX {msg.strip()}")
    writer.write(msg.encode())


async def _check_name_on_peer(ctx, rq, name):
    """Send a NAME-CHECK to the peer server via UDP and wait for the reply.
    Returns True if the name already exists on the peer, False otherwise."""

    if ctx.udp_transport is None:
        # No UDP transport available (should not happen in normal operation)
        return False

    loop = asyncio.get_running_loop()
    future = loop.create_future()
    ctx.pending_name_checks[rq] = future

    # Send NAME-CHECK to peer
    msg = encode(C.NAME_CHECK, rq, name)
    peer_addr = (ctx.peer_ip, ctx.peer_udp_port)
    ctx.log.info(f"UDP TX to peer {peer_addr}: {msg.strip()}")
    ctx.udp_transport.sendto(msg.encode(), peer_addr)

    try:
        result = await asyncio.wait_for(future, timeout=NAME_CHECK_TIMEOUT)
        return result  # True = exists on peer, False = does not
    except asyncio.TimeoutError:
        ctx.log.warning(f"NAME-CHECK timeout for '{name}' (rq {rq}), assuming unique")
        return False
    finally:
        ctx.pending_name_checks.pop(rq, None)


# handlers
# Each handler returns True to signal "close the connection", or None/False to
# keep the connection open for more messages.


#  REGISTER
@register_handler(C.REGISTER)
async def handle_register(ctx, writer, fields):

    if len(fields) != 5:
        _send(ctx, writer, encode(C.REGISTER_DENIED, "0", "Bad field count"))
        return False

    rq, name, ip, tcp_s, udp_s = fields

    # Region check
    if not ctx.is_ip_in_region(ip):
        _send(ctx, writer, encode(C.REFER, rq, ctx.peer_ip_for_clients))
        return False

    # Port validation
    try:
        tcp_port = int(tcp_s)
        udp_port = int(udp_s)
        if not (1 <= tcp_port <= 65535 and 1 <= udp_port <= 65535):
            raise ValueError
    except ValueError:
        _send(ctx, writer, encode(C.REGISTER_DENIED, rq, "Invalid port number"))
        return False

    # Cross-server name uniqueness check
    exists_on_peer = await _check_name_on_peer(ctx, rq, name)
    if exists_on_peer:
        _send(ctx, writer, encode(C.REGISTER_DENIED, rq,
                                  "Name already registered on another server"))
        return False

    ok, reason = ctx.db.register_user(name, ip, tcp_port, udp_port, ctx.server_name)

    if ok:
        _send(ctx, writer, encode(C.REGISTERED, rq))
    else:
        _send(ctx, writer, encode(C.REGISTER_DENIED, rq, reason))

    return False


# deregister user and close the TCP connection
@register_handler(C.DE_REGISTER)
async def handle_deregister(ctx, writer, fields):

    if len(fields) < 2:
        return True  # malformed -> close

    rq, name = fields[0], fields[1]

    deleted = ctx.db.delete_user(name)

    if deleted:
        ctx.log.info(f"User '{name}' deregistered – closing connection")
    else:
        ctx.log.info(f"DE-REGISTER ignored: '{name}' not found – closing connection")

    # Signal the connection loop to close
    return True


#  UPDATE
@register_handler(C.UPDATE)
async def handle_update(ctx, writer, fields):

    if len(fields) != 5:
        _send(ctx, writer, encode(C.UPDATE_DENIED, "0", "Bad field count"))
        return False

    rq, name, ip, tcp_s, udp_s = fields

    # Check user exists
    if not ctx.db.user_exists(name):
        _send(ctx, writer, encode(C.UPDATE_DENIED, rq, "Name does not exist"))
        return False

    # If new IP is out of region -> REFER, deregister, close connection
    if not ctx.is_ip_in_region(ip):
        _send(ctx, writer, encode(C.REFER, rq, ctx.peer_ip_for_clients))
        await writer.drain()
        ctx.db.delete_user(name)
        ctx.log.info(f"User '{name}' referred and deregistered (IP out of region) "
                     "– closing connection")
        return True  # close the TCP connection

    # Port validation
    try:
        tcp_port = int(tcp_s)
        udp_port = int(udp_s)
        if not (1 <= tcp_port <= 65535 and 1 <= udp_port <= 65535):
            raise ValueError
    except ValueError:
        _send(ctx, writer, encode(C.UPDATE_DENIED, rq, "Invalid port number"))
        return False

    ok, reason = ctx.db.update_user(name, ip, tcp_port, udp_port)

    if ok:
        _send(ctx, writer, encode(C.UPDATE_CONFIRMED, rq, name, ip, tcp_s, udp_s))
    else:
        _send(ctx, writer, encode(C.UPDATE_DENIED, rq, reason))

    return False


#  SUBJECTS
@register_handler(C.SUBJECTS)
async def handle_subjects(ctx, writer, fields):

    if len(fields) < 2:
        _send(ctx, writer, encode(C.SUBJECTS_REJECTED, "0", "?", "Bad field count"))
        return False

    rq = fields[0]
    name = fields[1]
    subjects = fields[2:]

    # Check user exists
    if not ctx.db.user_exists(name):
        _send(ctx, writer, encode(C.SUBJECTS_REJECTED, rq, name, *subjects))
        return False

    # Validate subjects against allowed list
    for subj in subjects:
        if subj not in C.VALID_SUBJECTS:
            _send(ctx, writer, encode(C.SUBJECTS_REJECTED, rq, name, *subjects))
            return False

    ok = ctx.db.update_subjects(name, subjects)

    if ok:
        _send(ctx, writer, encode(C.SUBJECTS_UPDATED, rq, name, *subjects))
    else:
        _send(ctx, writer, encode(C.SUBJECTS_REJECTED, rq, name, *subjects))

    return False


# Client connection loop

async def handle_client(reader, writer, ctx):
    """Read messages in a loop until the client disconnects or a handler
    signals that the connection should be closed (e.g. DE-REGISTER, REFER)."""

    addr = writer.get_extra_info("peername")
    ctx.log.info(f"TCP connection from {addr}")

    try:
        while True:
            data = await reader.readline()

            # Empty bytes means the client closed the connection
            if not data:
                ctx.log.info(f"Client {addr} disconnected")
                break

            text = data.decode()
            ctx.log.info(f"RX {text.strip()}")

            try:
                op, fields = decode_line(text)
            except ProtocolError as e:
                ctx.log.warning(f"Protocol error: {e}")
                continue  # skip bad message, keep connection open

            handler = handlers.get(op)

            if not handler:
                ctx.log.warning(f"Unknown command: {op}")
                continue

            close_connection = await handler(ctx, writer, fields)
            await writer.drain()

            if close_connection:
                ctx.log.info(f"Closing connection to {addr} (handler requested)")
                break

    except asyncio.IncompleteReadError:
        ctx.log.info(f"Client {addr} disconnected (incomplete read)")

    except ConnectionResetError:
        ctx.log.info(f"Client {addr} connection reset")

    except Exception as e:
        ctx.log.error(f"Error handling client {addr}: {e}")

    finally:
        writer.close()
        await writer.wait_closed()


#  Start TCP server
async def run_tcp_server(ctx):

    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, ctx),
        ctx.host,
        ctx.tcp_port,
    )

    ctx.log.info(f"TCP listening on {ctx.host}:{ctx.tcp_port}")

    async with server:
        await server.serve_forever()
