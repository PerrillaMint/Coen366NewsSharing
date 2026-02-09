# server/udp_server.py

import asyncio
import socket
from protocol.codec import decode_line, encode, ProtocolError
from protocol import constants as C


class UDPServerProtocol(asyncio.DatagramProtocol):

    def __init__(self, ctx):
        self.ctx = ctx
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def _is_from_peer(self, addr):
        return addr[0] == self.ctx.peer_ip and addr[1] == self.ctx.peer_udp_port

    def datagram_received(self, data, addr):
        try:
            text = data.decode()
            self.ctx.log.info(f"UDP RX from {addr}: {text.strip()}")

            op, fields = decode_line(text)

            if op == C.PUBLISH:
                self._handle_publish(fields, addr)

            elif op == C.PUBLISH_COMMENT:
                from_peer = self._is_from_peer(addr)
                self._handle_comment(fields, addr, from_peer)

            elif op == C.FORWARD:
                self._handle_forward(fields)

            else:
                self.ctx.log.warning(f"UDP unknown op: {op}")

        except ProtocolError as e:
            self.ctx.log.warning(f"UDP protocol error from {addr}: {e}")
        except Exception as e:
            self.ctx.log.error(f"UDP error from {addr}: {e}")

    #  PUBLISH — client publishes news
    def _handle_publish(self, fields, addr):

        if len(fields) < 5:
            self._send_to(
                addr,
                encode(C.PUBLISH_DENIED, "0", "Bad field count"),
            )
            return

        rq = fields[0]
        name = fields[1]
        subject = fields[2]
        title = fields[3]
        text = fields[4]

        # Validate user exists
        if not self.ctx.db.user_exists(name):
            self._send_to(addr, encode(C.PUBLISH_DENIED, rq, "User not registered"))
            return

        # Validate subject is in user's interest list
        if not self.ctx.db.user_has_subject(name, subject):
            self._send_to(
                addr,
                encode(C.PUBLISH_DENIED, rq, "Subject not in your interest list"),
            )
            return

        # Send MESSAGE to all local interested users
        self._send_to_interested(name, subject, title, text)

        # FORWARD to peer server
        fwd_msg = encode(C.FORWARD, name, subject, title, text)
        self._send_to_peer(fwd_msg)

        self.ctx.log.info(f"PUBLISH from '{name}' on '{subject}': {title}")

    #  PUBLISH-COMMENT
    def _handle_comment(self, fields, addr, from_peer=False):

        if len(fields) < 4:
            return

        name = fields[0]
        subject = fields[1]
        title = fields[2]
        text = fields[3]

        # If from a local client, validate user exists
        if not from_peer and not self.ctx.db.user_exists(name):
            self.ctx.log.warning(f"COMMENT from unknown user '{name}'")
            return

        # Send COMMENT to all local interested users
        comment_msg = encode(C.COMMENT, name, subject, title, text)
        self._send_to_interested_raw(subject, comment_msg)

        # Only forward to peer if this came from a local client (not from peer)
        if not from_peer:
            fwd_msg = encode(C.PUBLISH_COMMENT, name, subject, title, text)
            self._send_to_peer(fwd_msg)

        self.ctx.log.info(f"COMMENT from '{name}' on '{subject}': {title}")


    #  FORWARD 
    def _handle_forward(self, fields):

        if len(fields) < 4:
            return

        name = fields[0]
        subject = fields[1]
        title = fields[2]
        text = fields[3]

        # Send MESSAGE to all local interested users
        self._send_to_interested(name, subject, title, text)

        self.ctx.log.info(f"FORWARD relayed for '{name}' on '{subject}': {title}")


    #  Helpers
    def _send_to_interested(self, name, subject, title, text):
        msg = encode(C.MESSAGE, name, subject, title, text)
        self._send_to_interested_raw(subject, msg)

    def _send_to_interested_raw(self, subject, raw_msg):
        users = self.ctx.db.get_users_by_subject(subject)

        for user in users:
            dest = (user["ip"], user["udp_port"])
            self._send_to(dest, raw_msg)

    def _send_to(self, addr, msg):
        self.ctx.log.info(f"UDP TX to {addr}: {msg.strip()}")
        self.transport.sendto(msg.encode(), addr)

    def _send_to_peer(self, msg):
        peer_addr = (self.ctx.peer_ip, self.ctx.peer_udp_port)
        self.ctx.log.info(f"UDP TX to peer {peer_addr}: {msg.strip()}")
        self.transport.sendto(msg.encode(), peer_addr)


async def run_udp_server(ctx):

    loop = asyncio.get_running_loop()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: UDPServerProtocol(ctx),
        local_addr=(ctx.host, ctx.udp_port),
    )

    ctx.log.info(f"UDP listening on {ctx.host}:{ctx.udp_port}")

    return transport
