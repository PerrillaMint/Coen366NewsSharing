# server/tcp_server.py

import asyncio
from protocol.codec import decode_line, encode, ProtocolError
from protocol import constants as C


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


#  REGISTER
@register_handler(C.REGISTER)
async def handle_register(ctx, writer, fields):

    if len(fields) != 5:
        _send(ctx, writer, encode(C.REGISTER_DENIED, "0", "Bad field count"))
        return

    rq, name, ip, tcp_s, udp_s = fields

    # Region check
    if not ctx.is_ip_in_region(ip):
        _send(ctx, writer, encode(C.REFER, rq, ctx.peer_ip_for_clients))
        return

    # Port validation
    try:
        tcp_port = int(tcp_s)
        udp_port = int(udp_s)
        if not (1 <= tcp_port <= 65535 and 1 <= udp_port <= 65535):
            raise ValueError
    except ValueError:
        _send(ctx, writer, encode(C.REGISTER_DENIED, rq, "Invalid port number"))
        return

    ok, reason = ctx.db.register_user(name, ip, tcp_port, udp_port, ctx.server_name)

    if ok:
        _send(ctx, writer, encode(C.REGISTERED, rq))
    else:
        _send(ctx, writer, encode(C.REGISTER_DENIED, rq, reason))



#  DE-REGISTER  (server closes the TCP connection)
@register_handler(C.DE_REGISTER)
async def handle_deregister(ctx, writer, fields):

    if len(fields) < 2:
        return  # malformed, just ignore

    rq, name = fields[0], fields[1]

    deleted = ctx.db.delete_user(name)

    if deleted:
        ctx.log.info(f"User '{name}' deregistered")
    else:
        ctx.log.info(f"DE-REGISTER ignored: '{name}' not found")


#  UPDATE
@register_handler(C.UPDATE)
async def handle_update(ctx, writer, fields):

    if len(fields) != 5:
        _send(ctx, writer, encode(C.UPDATE_DENIED, "0", "Bad field count"))
        return

    rq, name, ip, tcp_s, udp_s = fields

    # Check user exists
    if not ctx.db.user_exists(name):
        _send(ctx, writer, encode(C.UPDATE_DENIED, rq, "Name does not exist"))
        return

    # If new IP is out of region -> REFER, deregister, server closes connection
    if not ctx.is_ip_in_region(ip):
        _send(ctx, writer, encode(C.REFER, rq, ctx.peer_ip_for_clients))
        ctx.db.delete_user(name)
        ctx.log.info(f"User '{name}' referred and deregistered (IP out of region)")
        return

    # Port validation
    try:
        tcp_port = int(tcp_s)
        udp_port = int(udp_s)
        if not (1 <= tcp_port <= 65535 and 1 <= udp_port <= 65535):
            raise ValueError
    except ValueError:
        _send(ctx, writer, encode(C.UPDATE_DENIED, rq, "Invalid port number"))
        return

    ok, reason = ctx.db.update_user(name, ip, tcp_port, udp_port)

    if ok:
        _send(ctx, writer, encode(C.UPDATE_CONFIRMED, rq, name, ip, tcp_s, udp_s))
    else:
        _send(ctx, writer, encode(C.UPDATE_DENIED, rq, reason))


#  SUBJECTS
@register_handler(C.SUBJECTS)
async def handle_subjects(ctx, writer, fields):

    if len(fields) < 2:
        _send(ctx, writer, encode(C.SUBJECTS_REJECTED, "0", "?", "Bad field count"))
        return

    rq = fields[0]
    name = fields[1]
    subjects = fields[2:]

    # Check user exists
    if not ctx.db.user_exists(name):
        _send(ctx, writer, encode(C.SUBJECTS_REJECTED, rq, name, *subjects))
        return

    # Validate subjects against allowed list
    for subj in subjects:
        if subj not in C.VALID_SUBJECTS:
            _send(ctx, writer, encode(C.SUBJECTS_REJECTED, rq, name, *subjects))
            return

    ok = ctx.db.update_subjects(name, subjects)

    if ok:
        _send(ctx, writer, encode(C.SUBJECTS_UPDATED, rq, name, *subjects))
    else:
        _send(ctx, writer, encode(C.SUBJECTS_REJECTED, rq, name, *subjects))



#  Client connection handler
async def handle_client(reader, writer, ctx):

    addr = writer.get_extra_info("peername")
    ctx.log.info(f"TCP connection from {addr}")

    try:
        data = await reader.readline()
        if not data:
            return

        text = data.decode()
        ctx.log.info(f"RX {text.strip()}")

        op, fields = decode_line(text)

        handler = handlers.get(op)

        if not handler:
            ctx.log.warning(f"Unknown command: {op}")
            return

        await handler(ctx, writer, fields)
        await writer.drain()

    except ProtocolError as e:
        ctx.log.warning(f"Protocol error: {e}")

    except Exception as e:
        ctx.log.error(f"Error handling client: {e}")

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
