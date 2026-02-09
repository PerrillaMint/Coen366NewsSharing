# server/persistence.py

import sqlite3
import time


class Database:

    def __init__(self, path):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.create_tables()

    #  Schema
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

        cur.execute("""
        CREATE TABLE IF NOT EXISTS subjects(
            name TEXT,
            subject TEXT,
            PRIMARY KEY (name, subject),
            FOREIGN KEY (name) REFERENCES users(name) ON DELETE CASCADE
        )
        """)

        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.commit()

    #  Registration
    def register_user(self, name, ip, tcp_port, udp_port, server):

        cur = self.conn.cursor()

        cur.execute("SELECT name FROM users WHERE name=?", (name,))
        if cur.fetchone():
            return False, "Name already exists"

        cur.execute(
            "INSERT INTO users VALUES(?,?,?,?,?,?)",
            (name, ip, tcp_port, udp_port, server, time.time()),
        )
        self.conn.commit()
        return True, ""

    #  Deregistration
    def delete_user(self, name):
        cur = self.conn.cursor()

        cur.execute("SELECT name FROM users WHERE name=?", (name,))
        if not cur.fetchone():
            return False

        cur.execute("DELETE FROM subjects WHERE name=?", (name,))
        cur.execute("DELETE FROM users WHERE name=?", (name,))
        self.conn.commit()
        return True

    #  Update user info
    def update_user(self, name, ip, tcp_port, udp_port):
        cur = self.conn.cursor()

        cur.execute("SELECT name FROM users WHERE name=?", (name,))
        if not cur.fetchone():
            return False, "Name does not exist"

        cur.execute(
            "UPDATE users SET ip=?, tcp_port=?, udp_port=?, updated=? WHERE name=?",
            (ip, tcp_port, udp_port, time.time(), name),
        )
        self.conn.commit()
        return True, ""

    #  Subjects
    def update_subjects(self, name, subjects):
        cur = self.conn.cursor()

        cur.execute("SELECT name FROM users WHERE name=?", (name,))
        if not cur.fetchone():
            return False

        # Replace all subjects
        cur.execute("DELETE FROM subjects WHERE name=?", (name,))
        for subj in subjects:
            cur.execute("INSERT INTO subjects VALUES(?,?)", (name, subj))

        self.conn.commit()
        return True

    def get_subjects(self, name):
        cur = self.conn.cursor()
        cur.execute("SELECT subject FROM subjects WHERE name=?", (name,))
        return [row[0] for row in cur.fetchall()]

    #  Queries
    def get_user(self, name):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users WHERE name=?", (name,))
        row = cur.fetchone()
        if not row:
            return None
        return {
            "name": row[0],
            "ip": row[1],
            "tcp_port": row[2],
            "udp_port": row[3],
            "server": row[4],
            "updated": row[5],
        }

    def user_exists(self, name):
        cur = self.conn.cursor()
        cur.execute("SELECT name FROM users WHERE name=?", (name,))
        return cur.fetchone() is not None

    def get_users_by_subject(self, subject):
        """Return list of user dicts who are interested in this subject."""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT u.name, u.ip, u.udp_port
            FROM users u
            JOIN subjects s ON u.name = s.name
            WHERE s.subject = ?
        """, (subject,))
        return [
            {"name": row[0], "ip": row[1], "udp_port": row[2]}
            for row in cur.fetchall()
        ]

    def user_has_subject(self, name, subject):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT 1 FROM subjects WHERE name=? AND subject=?",
            (name, subject),
        )
        return cur.fetchone() is not None
