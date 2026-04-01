# client_app.py

import sys
import asyncio
from client.client import TcpClient

tcp_client = None


async def main():
    global tcp_client

    print("PYTHON CLIENT READY", flush=True)

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
                print("PONG", flush=True)

            elif cmd == "REGISTER":
                # REGISTER Alice 127.0.0.1 5000 6000 127.0.0.1 10000
                if len(parts) < 7:
                    print("ERROR Invalid REGISTER format", flush=True)
                    continue

                name = parts[1]
                ip = parts[2]
                tcp_port = int(parts[3])
                udp_port = int(parts[4])
                server_ip = parts[5]
                server_tcp = int(parts[6])

                tcp_client = TcpClient(name, 0, False, [])
                tcp_client.client_ip = ip
                tcp_client.tcp_port = tcp_port
                tcp_client.udp_port = udp_port

                ok = await tcp_client.connect(server_ip, server_tcp)
                if not ok:
                    print("ERROR TCP connect failed", flush=True)
                    continue

                await tcp_client.register()
                

            elif cmd == "UPDATE":
                if tcp_client is None:
                    print("ERROR No active client", flush=True)
                    continue

                if len(parts) < 5:
                    print("ERROR Invalid UPDATE format", flush=True)
                    continue

                tcp_client.client_ip = parts[1]
                tcp_client.tcp_port = int(parts[2])
                tcp_client.udp_port = int(parts[3])
                tcp_client.server_port = int(parts[4])

                await tcp_client.update()
                print("UPDATE SENT", flush=True)

            elif cmd == "SUBJECTS":
                if tcp_client is None:
                    print("ERROR No active client", flush=True)
                    continue

                if len(parts) < 2:
                    print("ERROR Invalid SUBJECTS format", flush=True)
                    continue

                subjects = parts[1:]
                await tcp_client.subjects_update(*subjects)
                print("SUBJECTS SENT", flush=True)

            elif cmd == "DEREGISTER":
                if tcp_client is None:
                    print("ERROR No active client", flush=True)
                    continue

                await tcp_client.deregister()
                print("DEREGISTER SENT", flush=True)

            elif cmd == "EXIT":
                if tcp_client is not None:
                    await tcp_client.close()
                print("BYE", flush=True)
                break

            else:
                print(f"UNKNOWN COMMAND: {cmd}", flush=True)

        except Exception as e:
            print(f"ERROR {e}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())