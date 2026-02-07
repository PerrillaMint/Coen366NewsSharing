# server/config.py

def load_config():
    return {
        "server_name": "A",
        "host": "0.0.0.0",
        "tcp_port": 10000,

        # DEV ASSUMPTION:
        # Server A serves localhost clients
        "region_prefixes": ["127."],

        # Placeholder for later Server B
        "peer_ip_for_clients": "127.0.0.1",

        "db_path": "serverA.db"
    }
