# server/persistence.py

import sqlite3
import time

class Database:

    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.create_tables()

    def create_tables(self):
        cur = self.conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            name TEXT PRIMARY KEY,
            ip TEXT,
            tcp_port INTEGER,
            udp_port INTEGER,
            server TEXT,
            updated REAL
        )
        """)

        self.conn.commit()

    def register_user(self, name, ip, tcp_port, udp_port, server):

        cur = self.conn.cursor()

        cur.execute("SELECT name FROM users WHERE name=?", (name,))
        if cur.fetchone():
            return False, "Name already exists"

        cur.execute("""
        INSERT INTO users VALUES(?,?,?,?,?,?)
        """, (name, ip, tcp_port, udp_port, server, time.time()))

        self.conn.commit()

        return True, ""
