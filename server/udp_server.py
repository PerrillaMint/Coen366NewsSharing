# server/udp_server.py

import asyncio
import socket
from protocol.codec import decode_line, encode, ProtocolError
from protocol import constants as C

# Retry config for fire-and-forget peer messages (FORWARD, PUBLISH-COMMENT)
PEER_RETRY_COUNT = 2        # total retries after the first send
PEER_RETRY_DELAY = 0.5      # seconds between retries
PEER_ACK_TIMEOUT = 1.5      # seconds to wait for FORWARD-ACK


class UDPServerProtocol(asyncio.DatagramProtocol):

    def __init__(self, ctx):
        self.ctx = ctx
        self.transport = None
        # Maps msg_id -> asyncio.Event for FORWARD-ACK tracking
        self.pending_forward_acks = {}

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
                self._handle_forward(fields, addr)

            elif op == C.NAME_CHECK:
                self._handle_name_check(fields, addr)

            elif op == C.NAME_CHECK_REPLY:
                self._handle_name_check_reply(fields)

            elif op == C.FORWARD_ACK:
                self._handle_forward_ack(fields)

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

        # FORWARD to peer server (with retry)
        fwd_msg = encode(C.FORWARD, rq, name, subject, title, text)
        asyncio.ensure_future(self._send_to_peer_with_retry(rq, fwd_msg))

        # #8 — Acknowledge successful publish back to the client
        self._send_to(addr, encode(C.PUBLISH_CONFIRMED, rq, subject, title))

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
            asyncio.ensure_future(self._send_to_peer_with_retry(name, fwd_msg))

        self.ctx.log.info(f"COMMENT from '{name}' on '{subject}': {title}")

    #  FORWARD — received from peer server
    def _handle_forward(self, fields, addr):

        if len(fields) < 5:
            self.ctx.log.warning("FORWARD: bad field count, dropping")
            return

        rq = fields[0]
        name = fields[1]
        subject = fields[2]
        title = fields[3]
        text = fields[4]

        # #9 — Validate subject is in the allowed list
        if subject not in C.VALID_SUBJECTS:
            self.ctx.log.warning(
                f"FORWARD dropped: invalid subject '{subject}'")
            return

        # #9 — Validate title and text are non-empty
        if not title.strip() or not text.strip():
            self.ctx.log.warning("FORWARD dropped: empty title or text")
            return

        # Send ACK back to the peer so it can stop retrying (#10)
        self._send_to(addr, encode(C.FORWARD_ACK, rq))

        # Send MESSAGE to all local interested users
        self._send_to_interested(name, subject, title, text)

        self.ctx.log.info(f"FORWARD relayed for '{name}' on '{subject}': {title}")

    #  NAME-CHECK — peer asks "does this name exist locally?"
    def _handle_name_check(self, fields, addr):

        if len(fields) < 2:
            return

        rq = fields[0]
        name = fields[1]

        exists = self.ctx.db.user_exists(name)
        reply = encode(C.NAME_CHECK_REPLY, rq, name, "1" if exists else "0")
        self._send_to(addr, reply)
        self.ctx.log.info(f"NAME-CHECK for '{name}': exists={exists}")

    #  NAME-CHECK-REPLY — response from peer about name existence
    def _handle_name_check_reply(self, fields):

        if len(fields) < 3:
            return

        rq = fields[0]
        name = fields[1]
        exists = fields[2] == "1"

        future = self.ctx.pending_name_checks.get(rq)
        if future and not future.done():
            future.set_result(exists)
            self.ctx.log.info(
                f"NAME-CHECK-REPLY for '{name}' (rq {rq}): exists={exists}")
        else:
            self.ctx.log.warning(
                f"NAME-CHECK-REPLY for unknown/expired rq {rq}")

    #  FORWARD-ACK — peer acknowledges it received our FORWARD
    def _handle_forward_ack(self, fields):

        if len(fields) < 1:
            return

        rq = fields[0]
        evt = self.pending_forward_acks.get(rq)
        if evt and not evt.is_set():
            evt.set()
            self.ctx.log.info(f"FORWARD-ACK received for rq {rq}")
        else:
            self.ctx.log.warning(f"FORWARD-ACK for unknown/expired rq {rq}")

    #  Retry helper — send to peer and retry until ACK or limit reached (#10)
    async def _send_to_peer_with_retry(self, rq, msg):
        """Send msg to peer. Retry up to PEER_RETRY_COUNT times if no
        FORWARD-ACK is received within PEER_ACK_TIMEOUT."""

        evt = asyncio.Event()
        self.pending_forward_acks[rq] = evt

        peer_addr = (self.ctx.peer_ip, self.ctx.peer_udp_port)

        for attempt in range(1 + PEER_RETRY_COUNT):
            self.ctx.log.info(
                f"UDP TX to peer {peer_addr} (attempt {attempt + 1}): "
                f"{msg.strip()}")
            self.transport.sendto(msg.encode(), peer_addr)

            try:
                await asyncio.wait_for(evt.wait(), timeout=PEER_ACK_TIMEOUT)
                # ACK received
                self.pending_forward_acks.pop(rq, None)
                return
            except asyncio.TimeoutError:
                if attempt < PEER_RETRY_COUNT:
                    self.ctx.log.warning(
                        f"No ACK for rq {rq}, retrying "
                        f"({attempt + 1}/{PEER_RETRY_COUNT})...")

        self.ctx.log.error(
            f"Peer did not ACK rq {rq} after {1 + PEER_RETRY_COUNT} attempts")
        self.pending_forward_acks.pop(rq, None)

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
