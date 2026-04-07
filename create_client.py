import asyncio
import sys
from client.client import TcpClient, UdpClient

async def create_client(name=None, server_ip=None, udp_port=20001):
    print("Creating client...")

    if name is None:
        name = sys.argv[1]

    if server_ip is None:
        server_ip = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"

    udp_port = int(sys.argv[3]) if len(sys.argv) > 3 else udp_port

    tcp_client = TcpClient(name, 0, False, ["Sports"])
    tcp_client.udp_port = udp_port

    ok = await tcp_client.start_client(server_ip, 10000)
    if not ok:
        print("Failed to connect.")
        return

    udp_client = UdpClient(name, tcp_client.rq_counter, False, ["Sports"])
    udp_client.client_ip = tcp_client.client_ip
    udp_client.server_ip = server_ip
    udp_client.server_port = 20000
    udp_client.udp_port = udp_port

    await udp_client.start_listener()

    print(f"Client IP: {tcp_client.client_ip}")
    print(f"TCP Port: {tcp_client.tcp_port}")
    print(f"UDP Port: {udp_client.udp_port}")

    await tcp_client.register()
    print("Client registered.")

    try:
        while True:
            cmd = await asyncio.to_thread(input, "Command (subjects/publish/comment/quit): ")

            if cmd == "quit":
                break

            elif cmd == "subjects":
                subjects_line = await asyncio.to_thread(input, "Enter subjects separated by commas: ")
                subjects = [s.strip() for s in subjects_line.split(",") if s.strip()]
                await tcp_client.subjects_update(*subjects)

            elif cmd == "publish":
                subject = await asyncio.to_thread(input, "Subject: ")
                title = await asyncio.to_thread(input, "Title: ")
                text = await asyncio.to_thread(input, "Text: ")
                await udp_client.publish(subject, title, text)

            elif cmd == "comment":
                subject = await asyncio.to_thread(input, "Subject: ")
                title = await asyncio.to_thread(input, "Title: ")
                text = await asyncio.to_thread(input, "Comment: ")
                await udp_client.publish_comment(subject, title, text)

    finally:
        await udp_client.close_listener()
        await tcp_client.close()

asyncio.run(create_client())