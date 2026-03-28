#import socket

#s = socket.socket()
#s.connect(("127.0.0.1",10000))

#msg = "|REGISTER|1|Alice|127.0.0.1|5000|6000|\n"
#s.sendall(msg.encode())

#print(s.recv(1024).decode())

#s.close()

import asyncio
import client.client
from server.main import Ctx

cfg = {
    "server_name": "ClientTest",
    "host": "0.0.0.0",
    "tcp_port": 10000,
    "udp_port": 20000,
    "region_prefixes": ["127."],
    "peer_ip": "127.0.0.1",
    "peer_udp_port": 20001,
    "peer_ip_for_clients": "127.0.0.1",
    "db_path": "serverA.db",
}
ctx = Ctx(cfg)

async def test_client():
    print("Starting test client...")
    from client.client import TcpClient
    client = TcpClient(ctx, "TestClient1", 0, False, ["Subject1", "Subject2"])
    await client.start_client("127.0.0.1", 10000)
    print(f"Client IP: {await client.get_my_ip()}")
    

    #register
    await client.register()

asyncio.run(test_client())

