import asyncio
import sys
from client.client import TcpClient

async def create_client(name=None, server_ip=None):
    print("Creating client...")

    if name is None:
        name = sys.argv[1]

    if server_ip is None:
        server_ip = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"

    client = TcpClient(name, 0, False, ["Subject1", "Subject2"])

    ok = await client.start_client(server_ip, 10000)
    if not ok:
        print("Failed to connect.")
        return

    print(f"Client IP: {await client.get_my_ip()}")

    await client.register()
    print("Client registered.")

    # keep client alive
    await asyncio.Event().wait()

asyncio.run(create_client())