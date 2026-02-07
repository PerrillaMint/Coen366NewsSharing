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


@register_handler(C.REGISTER)
async def handle_register(ctx, writer, fields):

    rq, name, ip, tcp_s, udp_s = fields

    if not ctx.is_ip_in_region(ip):
        writer.write(encode(C.REFER, rq, ctx.peer_ip_for_clients).encode())
        return

    ok, reason = ctx.db.register_user(
        name,
        ip,
        int(tcp_s),
        int(udp_s),
        ctx.server_name
    )

    if ok:
        writer.write(encode(C.REGISTERED, rq).encode())
    else:
        writer.write(encode(C.REGISTER_DENIED, rq, reason).encode())


@register_handler(C.DE_REGISTER)
async def handle_deregister(ctx, writer, fields):
    rq, name = fields
    ctx.db.delete_user(name)


@register_handler(C.UPDATE)
async def handle_update(ctx, writer, fields):

    rq, name, ip, tcp_s, udp_s = fields

    ok, reason = ctx.db.update_user(name, ip, int(tcp_s), int(udp_s))

    if ok:
        writer.write(encode(C.UPDATE_CONFIRMED, rq, name, ip, tcp_s, udp_s).encode())
    else:
        writer.write(encode(C.UPDATE_DENIED, rq, reason).encode())


@register_handler(C.SUBJECTS)
async def handle_subjects(ctx, writer, fields):

    rq = fields[0]
    name = fields[1]
    subjects = fields[2:]

    ok = ctx.db.update_subjects(name, subjects)

    if ok:
        writer.write(encode(C.SUBJECTS_UPDATED, rq, name, *subjects).encode())
    else:
        writer.write(encode(C.SUBJECTS_REJECTED, rq, name, *subjects).encode())


async def handle_client(reader, writer, ctx):

    try:
        data = await reader.readline()
        if not data:
            return

        text = data.decode()
        ctx.log.info(f"RX {text.strip()}")

        op, fields = decode_line(text)

        handler = handlers.get(op)

        if not handler:
            ctx.log.warning(f"Unknown command {op}")
            return

        await handler(ctx, writer, fields)
        await writer.drain()

    except ProtocolError as e:
        ctx.log.warning(str(e))

    finally:
        writer.close()
        await writer.wait_closed()


async def run_tcp_server(ctx):

    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, ctx),
        ctx.host,
        ctx.tcp_port
    )

    ctx.log.info(f"Listening TCP on {ctx.tcp_port}")

    async with server:
        await server.serve_forever()
