import sys
import asyncio
from client.client import TcpClient
from protocol.codec import encode,decode_line
from protocol import constants as C
from server.config import load_config
from server.persistence import Database
from client.client import UdpClient

udp_live_client = None
tcp_live_client = None

server_cfg = None
server_db = None
remote_server_ip = None
clients = {}
active_client_key = None
async def handle_publish(parts):
    global udp_live_client, active_client_key

    if udp_live_client is None:
        out("ERROR|UDP client not initialized")
        return

    if active_client_key is None:
        out("ERROR|No active client")
        return

    if len(parts) < 4:
        out("ERROR|Invalid PUBLISH format")
        return

    subject = parts[1]
    title = parts[2]
    text = parts[3]

    udp_live_client.name = active_client_key
    await udp_live_client.publish(subject, title, text)

    out("PUBLISH SENT")

async def handle_comment_latest(parts):

    global udp_live_client, active_client_key

    if udp_live_client is None:
        out("ERROR|UDP client not initialized")
        return

    if active_client_key is None:
        out("ERROR|No active client")
        return

    if len(parts) < 2:
        out("ERROR|Invalid COMMENT_LATEST format")
        return

    if udp_live_client.latest_message is None:
        out("ERROR|No message available to comment on")
        return

    text = parts[1]

    subject = udp_live_client.latest_message["subject"]
    title = udp_live_client.latest_message["title"]

    udp_live_client.name = active_client_key
    await udp_live_client.publish_comment(subject, title, text)

    out("COMMENT SENT")
        
async def handle_init_client(parts):
    global server_cfg, remote_server_ip

    try:
        if server_cfg is None:
            out("ERROR|Server config not initialized")
            return

        temp_client = TcpClient("temp")
        await temp_client.init_network_info()
        local_ip = temp_client.client_ip

        server_ip = remote_server_ip if remote_server_ip else server_cfg["host"]
        server_port = server_cfg["tcp_port"]

        reader, writer = await asyncio.open_connection(server_ip, server_port)

        try:
            msg = encode(C.GET_USER_BY_IP, "1", local_ip)
            if not msg.endswith("\n"):
                msg += "\n"

            writer.write(msg.encode())
            await writer.drain()

            line = await reader.readline()
            if not line:
                out("ERROR|No response from server for GET-USER-BY-IP")
                return

            text = line.decode().strip()
            op, fields = decode_line(text)

            if op != C.USER_INFO:
                out(f"ERROR|Unexpected response: {text}")
                return

            if len(fields) < 2:
                out("ERROR|Bad USER-INFO response")
                return

            if fields[1] == "NOT-FOUND":
                out(f"ERROR|No registered client found for IP {local_ip}")
                return

            name = fields[1]
            ip = fields[2]
            tcp_port = fields[3]
            udp_port = fields[4]
           
           
            out(
                f"CLIENT-INIT|{name}|{ip}|{tcp_port}|{udp_port}|"
                f"{server_ip}|{server_port}"
            )

        finally:
            writer.close()
            await writer.wait_closed()

    except Exception as e:
        out(f"ERROR|INIT_CLIENT failed: {e}")
def out(msg: str):
    print(msg, flush=True)


def make_key(name: str):
    return name


async def handle_init_server(parts):
    global server_cfg, server_db, remote_server_ip

    if len(parts) < 2:
        out("ERROR|Invalid INIT_SERVER format")
        return

    server_id = parts[1].upper()
    remote_server_ip = parts[2] if len(parts) > 2 else None

    try:
        server_cfg = await load_config(server_id)
        server_db = Database(server_cfg["db_path"])

        server_name = server_cfg["server_name"]
        server_ip = remote_server_ip if remote_server_ip else server_cfg["host"]
        tcp_port = server_cfg["tcp_port"]
        udp_port = server_cfg["udp_port"]

        out(f"SERVER-INIT|{server_name}|{server_ip}|{tcp_port}|{server_ip}|{udp_port}|")
    except Exception as e:
        out(f"ERROR|INIT_SERVER failed: {e}")

async def request_users_from_server(server_ip: str, server_port: int):
    global server_db

    try:
        if server_db is None:
            out("ERROR|Server DB not initialized")
            return

        users = server_db.list_users()
        names = [user["name"] for user in users]
        out("CLIENT-LIST|" + ",".join(names))

    except Exception as e:
        out(f"ERROR|LOADUSERS failed: {e}")


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
    global active_client_key, udp_live_client, tcp_live_client

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

    # start UDP listener for the UI-owned client
    if udp_live_client is None:
        udp_live_client = UdpClient(name, 0, True, [])
        udp_live_client.client_ip = ip
        udp_live_client.server_ip = server_ip
        udp_live_client.server_port = 20000
        udp_live_client.udp_port = udp_port

        await udp_live_client.start_listener()
        out(f"UDP-LISTENER-STARTED|{ip}|{udp_port}")

    await client.register()

    clients[key] = client
    tcp_live_client = client
    active_client_key = key

    out(f"CLIENT-ADDED|{key}")
    out(f"CLIENT-SELECTED|{key}")
    out(serialize_client(client))

async def handle_select(parts):
    global active_client_key, server_db, server_cfg

    if len(parts) < 2:
        out("ERROR|Invalid SELECT format")
        return

    key = parts[1]

    if server_db is None or server_cfg is None:
        out("ERROR|Server DB not initialized")
        return

    user = server_db.get_user(key)
    if user is None:
        out(f"ERROR|Unknown client: {key}")
        return

    subjects = server_db.get_subjects(key)

    active_client_key = key
    out(f"CLIENT-SELECTED|{key}")

    registered = "1"
    server_ip = server_cfg["host"]
    server_port = server_cfg["tcp_port"]
    subjects_csv = ",".join(subjects)

    out(
        f"STATE|{user['name']}|{user['ip']}|{user['tcp_port']}|{user['udp_port']}|"
        f"{server_ip}|{server_port}|{registered}|{subjects_csv}"
    )


async def handle_update(parts):
    client = get_active_client()
    if client is None:
        out("ERROR|No active client")
        return

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
    global active_client_key, udp_live_client

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

    if udp_live_client is not None:
        await udp_live_client.close_listener()
        udp_live_client = None

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
            elif cmd == "INIT_CLIENT":
                await handle_init_client(parts)
            elif cmd == "INIT_SERVER":
                await handle_init_server(parts)
            elif cmd == "REGISTER":
                await handle_register(parts)
            elif cmd == "PUBLISH":
                await handle_publish(parts)
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
            elif cmd == "COMMENT_LATEST":
                await handle_comment_latest(parts)
            elif cmd == "EXIT":
                for client in list(clients.values()):
                    try:
                        await client.close()
                    except Exception:
                        pass

                if udp_live_client is not None:
                    await udp_live_client.close_listener()
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