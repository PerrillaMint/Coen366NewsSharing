import asyncio
import sys
import client.client
from client.client import UdpClient
from client.client import TcpClient

async def create_client(Name = None, server_ip = None):
    print("Creating client...")

    if Name is None:
        Name = sys.argv[1]

    client = TcpClient(Name, 1, False, ["Subject1", "Subject2"])

    if server_ip is None:
        server_ip = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"

    await client.start_client(server_ip, 10000)

    print(f"Client IP: {await client.get_my_ip()}")

asyncio.run(create_client())

