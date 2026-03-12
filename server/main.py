# server/main.py

import asyncio
from server.config import load_config
from server.persistence import Database
from server.log import make_logger
from server.tcp_server import run_tcp_server
from server.udp_server import run_udp_server


class Ctx:

    def __init__(self, cfg):
        self.server_name = cfg["server_name"]
        self.host = cfg["host"]
        self.tcp_port = cfg["tcp_port"]
        self.udp_port = cfg["udp_port"]
        self.region_prefixes = cfg["region_prefixes"]
        self.peer_ip = cfg["peer_ip"]
        self.peer_udp_port = cfg["peer_udp_port"]
        self.peer_ip_for_clients = cfg["peer_ip_for_clients"]
        self.db = Database(cfg["db_path"])
        self.log = make_logger(f"Server-{self.server_name}")

        # Set by run_udp_server so TCP handlers can send UDP packets
        self.udp_transport = None

        # Maps rq_id -> asyncio.Future for cross-server NAME-CHECK replies
        self.pending_name_checks = {}

    def is_ip_in_region(self, ip):
        return any(ip.startswith(p) for p in self.region_prefixes)


async def main():
    cfg = load_config()
    ctx = Ctx(cfg)

    ctx.log.info(f"Starting Server {ctx.server_name}")
    ctx.log.info(f"  TCP: {ctx.host}:{ctx.tcp_port}")
    ctx.log.info(f"  UDP: {ctx.host}:{ctx.udp_port}")
    ctx.log.info(f"  Region prefixes: {ctx.region_prefixes}")
    ctx.log.info(f"  Peer: {ctx.peer_ip}:{ctx.peer_udp_port}")

    # Start UDP server (returns transport, runs in background)
    udp_transport = await run_udp_server(ctx)
    ctx.udp_transport = udp_transport

    # Start TCP server (blocks / serves forever)
    try:
        await run_tcp_server(ctx)
    finally:
        udp_transport.close()


if __name__ == "__main__":
    asyncio.run(main())
