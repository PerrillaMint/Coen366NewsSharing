
# server/config.py

import sys


def load_config(server_id=None):
    
    if server_id is None:
        server_id = sys.argv[1].upper() if len(sys.argv) > 1 else "A"

    configs = {
        "A": {
            "server_name": "A",
            "host": "0.0.0.0",
            "tcp_port": 10000,
            "udp_port": 20000,
            # DEV ASSUMPTION:
            # Server A serves localhost clients
            "region_prefixes": ["127."],
            # Peer server info (Server B)
            "peer_ip": "127.0.0.1",
            "peer_udp_port": 20001,
            "peer_ip_for_clients": "127.0.0.1",
            "db_path": "serverA.db",
        },
        "B": {
            "server_name": "B",
            "host": "0.0.0.0",
            "tcp_port": 10001,
            "udp_port": 20001,
            "region_prefixes": ["10."],
            #"region_prefixes": ["192.168."],
            # Peer server info (Server A)
            "peer_ip": "127.0.0.1",
            "peer_udp_port": 20000,
            "peer_ip_for_clients": "127.0.0.1",
            "db_path": "serverB.db",
        },
    }

    if server_id not in configs:
        raise ValueError(f"Unknown server id: {server_id}. Use A or B.")

    return configs[server_id]
