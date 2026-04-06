
# server/config.py

import sys
import asyncio
import os

def ui(msg: str):
    print(msg, flush=True)


def debug(msg: str):
    print(msg, file=sys.stderr, flush=True)

#TODO: Refactor to load from file/env vars instead of hardcoding configs in code. This is just for demo purposes and makes it easy to run multiple servers on the same machine.
async def get_my_ip():
        transport = None
        try:
            loop = asyncio.get_running_loop()
            transport, _ = await loop.create_datagram_endpoint(
                lambda: asyncio.DatagramProtocol(),
                remote_addr=("8.8.8.8", 80)
            )
            return transport.get_extra_info("sockname")[0]
        except Exception as e:
            debug(f"[Server] Error getting local IP: {e}")
            return "127.0.0.1"
        finally:
            if transport:
                transport.close()


async def _get_peer_ip(server_id):
    """Get peer IP from environment variable or prompt user if not set."""
    peer_server = "B" if server_id == "A" else "A"

    # Try environment variables in order of specificity
    peer_ip = os.getenv(f"SERVER_{peer_server}_IP") or os.getenv("PEER_IP")

    if peer_ip:
        return peer_ip

    # Prompt user if not set
    print(f"\nServer {server_id} started. Waiting for configuration...")
    print(f"Enter the IP address of Server {peer_server} (or press Enter for 127.0.0.1): ", end="", flush=True)
    user_input = input().strip()

    return user_input if user_input else "127.0.0.1"


def _get_region_prefixes(local_ip):
    region_prefixes = local_ip.rsplit(".", 1)[0] + "."
    return [region_prefixes]


async def load_config(server_id=None):

    if server_id is None:
        server_id = sys.argv[1].upper() if len(sys.argv) > 1 else "A"

    local_ip = await get_my_ip()
    print(f"\nServer {server_id} Local IP: {local_ip}")
    region_prefixes = _get_region_prefixes(local_ip)
    print(f"\nServer {server_id} Region Prefixes: {region_prefixes}")
    peer_ip = await _get_peer_ip(server_id)
    print(f"\nServer {server_id} Peer IP: {peer_ip}")

    configs = {
        "A": {
            "server_name": "A",
            "host": local_ip,
            "tcp_port": 10000,
            "udp_port": 20000,
            # DEV ASSUMPTION:
            # Server A serves localhost clients by default; update region_prefixes for your subnet
            "region_prefixes": region_prefixes,
            # Peer server info (Server B)
            "peer_ip": peer_ip,
            "peer_udp_port": 20000,
            "peer_ip_for_clients": peer_ip,
            "db_path": "serverA.db",
        },
        "B": {
            "server_name": "B",
            "host": local_ip,
            "tcp_port": 10000,
            "udp_port": 20000,
            "region_prefixes": region_prefixes,
            #"region_prefixes": ["192.168."],
            # Peer server info (Server A)
            "peer_ip": peer_ip,
            "peer_udp_port": 20000,
            "peer_ip_for_clients": peer_ip,
            "db_path": "serverB.db",

            #TODO : maybe add server C with localhost for testing
        },
    }

    if server_id not in configs:
        raise ValueError(f"Unknown server id: {server_id}. Use A or B.")

    return configs[server_id]
