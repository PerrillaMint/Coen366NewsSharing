# server/main.py

import asyncio
from server.config import load_config
from server.persistence import Database
from server.log import make_logger
from server.tcp_server import run_tcp_server

class Ctx:
    def __init__(self, cfg):
        self.server_name = cfg["server_name"]
        self.host = cfg["host"]
        self.tcp_port = cfg["tcp_port"]
        self.region_prefixes = cfg["region_prefixes"]
        self.peer_ip_for_clients = cfg["peer_ip_for_clients"]
        self.db = Database(cfg["db_path"])
        self.log = make_logger(self.server_name)

    def is_ip_in_region(self, ip):
        return any(ip.startswith(p) for p in self.region_prefixes)


async def main():
    cfg = load_config()
    ctx = Ctx(cfg)
    await run_tcp_server(ctx)

if __name__ == "__main__":
    asyncio.run(main())
