import sys
import asyncio
from client.client import TcpClient
from protocol.codec import encode, decode_line
from protocol import constants as C
from server.config import load_config

clients = {}
active_client_key = None
async def handle_init_server(parts):
    if len(parts) < 2:
        out("ERROR|Invalid INIT_SERVER format")
        return

    server_id = parts[1].upper()

    try:
        cfg = await load_config(server_id)

        server_name = cfg["server_name"]
        server_ip = cfg["host"]
        tcp_port = cfg["tcp_port"]
        udp_port = cfg["udp_port"]

        # For now:
        # IP = same as server IP
        # Server TCP = blank
        out(f"SERVER-INIT|{server_name}|{server_ip}|{tcp_port}|{server_ip}|{udp_port}|")
    except Exception as e:
        out(f"ERROR|INIT_SERVER failed: {e}")

async def request_users_from_server(server_ip: str, server_port: int):
    reader = None
    writer = None

    try:
        reader, writer = await asyncio.open_connection(server_ip, server_port)

        msg = encode(C.LIST_USERS, "1")
        if not msg.endswith("\n"):
            msg += "\n"

        writer.write(msg.encode())
        await writer.drain()

        line = await reader.readline()
        if not line:
            out("ERROR|No response from server for LIST-USERS")
            return

        text = line.decode().strip()
        op, fields = decode_line(text)

        if op != C.USERS_LIST:
            out(f"ERROR|Unexpected response: {text}")
            return

        users = fields[1:]

        for name in users:
            if name not in clients:
                client = TcpClient(name, 0, True, [])
                client.server_ip = server_ip
                client.server_port = server_port
                clients[name] = client

        out("CLIENT-LIST|" + ",".join(users))

    except Exception as e:
        out(f"ERROR|LOADUSERS failed: {e}")

    finally:
        if writer:
            writer.close()
            await writer.wait_closed()
    reader = None
    writer = None

    try:
        reader, writer = await asyncio.open_connection(server_ip, server_port)

        msg = encode(C.LIST_USERS, "1")
        if not msg.endswith("\n"):
            msg += "\n"

        writer.write(msg.encode())
        await writer.drain()

        line = await reader.readline()
        if not line:
            out("ERROR|No response from server for LIST-USERS")
            return

        text = line.decode().strip()
        op, fields = decode_line(text)

        if op != C.USERS_LIST:
            out(f"ERROR|Unexpected response: {text}")
            return

        users = fields[1:]   # fields[0] = rq id
        out("CLIENT-LIST|" + ",".join(users))

    except Exception as e:
        out(f"ERROR|LOADUSERS failed: {e}")

    finally:
        if writer:
            writer.close()
            await writer.wait_closed()


def out(msg: str):
    print(msg, flush=True)


def make_key(name: str):
    return name


async def ensure_connected(client: TcpClient):
    if client.writer is None or client.writer.is_closing():
        ok = await client.connect(client.server_ip, client.server_port)
        return ok
    return True


def serialize_client(client: TcpClient):
    subjects = ",".join(client.subjects_list) if getattr(client, "subjects_list", None) else ""
    registered = "1" if client.is_registered else "0"

    return (
        f"STATE|{client.name}|{client.client_ip}|{client.tcp_port}|{client.udp_port}|"
        f"{client.server_ip}|{client.server_port}|{registered}|{subjects}"
    )


def get_active_client():
    global active_client_key

    if active_client_key is None:
        return None

    return clients.get(active_client_key)


async def handle_register(parts):
    global active_client_key

    # REGISTER Alice 127.0.0.1 5000 6000 127.0.0.1 10000
    if len(parts) < 7:
        out("ERROR|Invalid REGISTER format")
        return

    name = parts[1]
    ip = parts[2]
    tcp_port = int(parts[3])
    udp_port = int(parts[4])
    server_ip = parts[5]
    server_tcp = int(parts[6])

    key = make_key(name)

    if key in clients:
        out(f"ERROR|Client already exists: {name}")
        return

    client = TcpClient(name, 0, False, [])
    client.client_ip = ip
    client.tcp_port = tcp_port
    client.udp_port = udp_port
    client.server_ip = server_ip
    client.server_port = server_tcp

    ok = await client.connect(server_ip, server_tcp)
    if not ok:
        out("ERROR|TCP connect failed")
        return

    await client.register()

    clients[key] = client
    active_client_key = key

    out(f"CLIENT-ADDED|{key}")
    out(f"CLIENT-SELECTED|{key}")
    out(serialize_client(client))


async def handle_select(parts):
    global active_client_key

    if len(parts) < 2:
        out("ERROR|Invalid SELECT format")
        return

    key = parts[1]

    if key not in clients:
        out(f"ERROR|Unknown client: {key}")
        return

    active_client_key = key
    out(f"CLIENT-SELECTED|{key}")
    out(serialize_client(clients[key]))


async def handle_update(parts):
    client = get_active_client()
    if client is None:
        out("ERROR|No active client")
        return

    # UPDATE 127.0.0.1 5001 6001 10000
    if len(parts) < 5:
        out("ERROR|Invalid UPDATE format")
        return

    client.client_ip = parts[1]
    client.tcp_port = int(parts[2])
    client.udp_port = int(parts[3])
    client.server_port = int(parts[4])

    ok = await ensure_connected(client)
    if not ok:
        out("ERROR|Reconnect failed")
        return

    await client.update()
    out("UPDATE SENT")
    out(serialize_client(client))


async def handle_subjects(parts):
    client = get_active_client()
    if client is None:
        out("ERROR|No active client")
        return

    if len(parts) < 2:
        out("ERROR|Invalid SUBJECTS format")
        return

    subjects = parts[1:]
    client.subjects_list = subjects

    ok = await ensure_connected(client)
    if not ok:
        out("ERROR|Reconnect failed")
        return

    await client.subjects_update(*subjects)
    out("SUBJECTS SENT")
    out(serialize_client(client))


async def handle_deregister():
    global active_client_key

    client = get_active_client()
    if client is None:
        out("ERROR|No active client")
        return

    ok = await ensure_connected(client)
    if not ok:
        out("ERROR|Reconnect failed")
        return

    current_key = active_client_key

    await client.deregister()
    out("DEREGISTER SENT")

    try:
        await client.close()
    except Exception:
        pass

    if current_key in clients:
        del clients[current_key]

    out(f"CLIENT-REMOVED|{current_key}")

    if clients:
        active_client_key = next(iter(clients))
        out(f"CLIENT-SELECTED|{active_client_key}")
        out(serialize_client(clients[active_client_key]))
    else:
        active_client_key = None
        out("NO-CLIENTS")


async def handle_list():
    names = ",".join(clients.keys())
    out(f"CLIENT-LIST|{names}")


async def handle_getstate():
    client = get_active_client()
    if client is None:
        out("ERROR|No active client")
        return

    out(serialize_client(client))


async def main():
    out("PYTHON CLIENT READY")

    while True:
        try:
            line = await asyncio.to_thread(sys.stdin.readline)
            if not line:
                break

            line = line.strip()
            if not line:
                continue

            parts = line.split()
            cmd = parts[0].upper()

            if cmd == "PING":
                out("PONG")
                
            elif cmd == "INIT_SERVER":
                await handle_init_server(parts)

            elif cmd == "REGISTER":
                await handle_register(parts)

            elif cmd == "SELECT":
                await handle_select(parts)

            elif cmd == "UPDATE":
                await handle_update(parts)

            elif cmd == "SUBJECTS":
                await handle_subjects(parts)

            elif cmd == "DEREGISTER":
                await handle_deregister()

            elif cmd == "LIST":
                await handle_list()

            elif cmd == "GETSTATE":
                await handle_getstate()

            elif cmd == "EXIT":
                for client in list(clients.values()):
                    try:
                        await client.close()
                    except Exception:
                        pass

                out("BYE")
                break
            elif cmd == "LOADUSERS":
                if len(parts) < 3:
                    out("ERROR|Invalid LOADUSERS format")
                    continue

                server_ip = parts[1]
                server_port = int(parts[2])
                await request_users_from_server(server_ip, server_port)

            else:
                out(f"ERROR|Unknown command: {cmd}")

        except Exception as e:
            out(f"ERROR|{e}")


if __name__ == "__main__":
    asyncio.run(main())