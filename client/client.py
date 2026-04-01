import asyncio
import sys
from abc import ABC, abstractmethod
from protocol.codec import decode_line, encode, ProtocolError
from protocol import constants as C


def ui(msg: str):
    print(msg, flush=True)


def debug(msg: str):
    print(msg, file=sys.stderr, flush=True)


class BaseClient(ABC):

    def __init__(self, name, rq_counter=0, is_registered=False, subjects=None):
        self.client_ip = "127.0.0.1"
        self.server_ip = "0.0.0.0"

        self.server_port = 0
        self.udp_port = 0
        self.tcp_port = 0

        self.writer = None
        self.reader = None

        self.name = name
        self.rq_counter = rq_counter
        self.is_registered = is_registered
        self.subjects = subjects or []

    async def init_network_info(self):
        self.client_ip = await self.get_my_ip()

    @abstractmethod
    async def send_message(self, message: str):
        pass

    async def get_next_rq(self):
        self.rq_counter += 1
        return self.rq_counter

    async def close(self):
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
            debug(f"Connection to {self.server_ip}:{self.server_port} closed.")

    async def get_my_ip(self):
        transport = None
        try:
            loop = asyncio.get_running_loop()
            transport, _ = await loop.create_datagram_endpoint(
                lambda: asyncio.DatagramProtocol(),
                remote_addr=("8.8.8.8", 1)
            )
            return transport.get_extra_info("sockname")[0]
        except Exception as e:
            debug(f"[UDP] Error getting local IP: {e}")
            return "127.0.0.1"
        finally:
            if transport:
                transport.close()


class TcpClient(BaseClient):

    def __init__(self, name, rq_counter=0, is_registered=False, subjects=None):
        super().__init__(name, rq_counter, is_registered, subjects)

    async def start_client(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        await self.init_network_info()
        return await self.connect(self.server_ip, self.server_port)

    async def connect(self, server_ip, server_port):
        try:
            self.server_ip = server_ip
            self.server_port = server_port

            self.reader, self.writer = await asyncio.wait_for(
                asyncio.open_connection(server_ip, server_port),
                timeout=5.0
            )

            address_info = self.writer.get_extra_info("sockname")
            self.tcp_port = address_info[1]

            debug(f"[TCP] Connected to {self.server_ip}:{self.server_port}")

            self._listen_task = asyncio.create_task(self.listen_forever())
            return True
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError) as e:
            ui(f"ERROR|TCP connect failed: {e}")
            return False

    async def send_message(self, message: str):
        if not self.writer or self.writer.is_closing():
            debug("[TCP] Error: Not connected. Attempting to reconnect...")
            ok = await self.connect(self.server_ip, self.server_port)
            if ok:
                debug("[TCP] Successfully reconnected")
            else:
                return

        try:
            if not message.endswith("\n"):
                message += "\n"

            self.writer.write(message.encode())
            await self.writer.drain()
            debug(f"[TCP] Sent: {message.strip()}")
        except Exception as e:
            ui(f"ERROR|TCP send failed: {e}")
            await self.close()

    async def listen_forever(self):
        try:
            while True:
                line = await self.reader.readline()

                if not line:
                    debug("[TCP] Server closed the connection.")
                    break

                text = line.decode().strip()
                debug(f"[TCP] Received: {text}")
                await self.handle_server_message(text)

        except asyncio.CancelledError:
            pass
        except Exception as e:
            ui(f"ERROR|TCP listener failed: {e}")
        finally:
            await self.close()

    async def register(self):
        rq = await self.get_next_rq()
        msg = encode(C.REGISTER, rq, self.name, self.client_ip, self.tcp_port, self.udp_port)
        await self.send_message(msg)

    async def deregister(self):
        rq = await self.get_next_rq()
        msg = encode(C.DE_REGISTER, rq, self.name)
        await self.send_message(msg)

    async def update(self):
        rq = await self.get_next_rq()
        msg = encode(C.UPDATE, rq, self.name, self.client_ip, self.tcp_port, self.udp_port)
        await self.send_message(msg)

    async def subjects_update(self, *subjects):
        rq = await self.get_next_rq()
        msg = encode(C.SUBJECTS, rq, self.name, *subjects)
        await self.send_message(msg)

    async def handle_server_message(self, data: str):
        op, fields = decode_line(data)

        if op == C.REGISTERED:
            await self.handle_registered(fields)
        elif op == C.REGISTER_DENIED:
            await self.handle_register_denied(fields)
        elif op == C.REFER:
            await self.handle_refer(fields)
        elif op == C.UPDATE_CONFIRMED:
            await self.handle_update_confirmed(fields)
        elif op == C.UPDATE_DENIED:
            await self.handle_update_denied(fields)
        elif op == C.SUBJECTS_UPDATED:
            await self.handle_subjects_updated(fields)
        elif op == C.SUBJECTS_REJECTED:
            await self.handle_subjects_rejected(fields)
        elif op == C.USERS_LIST:
            await self.handle_users_list(fields)
        else:
            debug(f"[TCP] Unknown op: {op}")
    async def handle_users_list(self, fields):
    # fields[0] is rq id
        users = fields[1:]
        ui("USERS-LIST|" + ",".join(users))
        
    async def handle_registered(self, fields):
        self.is_registered = True
        ui("REGISTERED")

    async def handle_register_denied(self, fields):
        ui(f"REGISTER-DENIED|{fields[1]}")

    async def handle_refer(self, fields):
        ui(f"REFER|{fields[1]}")

    async def handle_update_confirmed(self, fields):
        ui("UPDATE-CONFIRMED")

    async def handle_update_denied(self, fields):
        ui(f"UPDATE-DENIED|{fields[1]}")

    async def handle_subjects_updated(self, fields):
        self.subjects_list = fields[2:]
        ui("SUBJECTS-UPDATED")

    async def handle_subjects_rejected(self, fields):
        ui("SUBJECTS-REJECTED")


class UdpClient(BaseClient):

    def __init__(self, name, rq_counter=0, is_registered=False, subjects=None):
        super().__init__(name, rq_counter, is_registered, subjects)

    async def send_message(self, message: str):
        loop = asyncio.get_running_loop()
        transport = None
        try:
            transport, _ = await loop.create_datagram_endpoint(
                lambda: asyncio.DatagramProtocol(),
                remote_addr=(self.server_ip, self.server_port)
            )

            self.udp_port = transport.get_extra_info("sockname")[1]
            transport.sendto(message.encode())
            debug(f"[UDP] Sent: {message.strip()}")
        except Exception as e:
            ui(f"ERROR|UDP send failed: {e}")
        finally:
            if transport:
                transport.close()

    async def publish(self, subject, title, text):
        rq = await self.get_next_rq()
        msg = encode(C.PUBLISH, rq, self.name, subject, title, text)
        await self.send_message(msg)

    async def publish_comment(self, subject, title, text):
        msg = encode(C.PUBLISH_COMMENT, self.name, subject, title, text)
        await self.send_message(msg)

    async def datagram_received(self, data, addr):
        try:
            text = data.decode()
            debug(f"[UDP] RX from {addr}: {text.strip()}")

            op, fields = decode_line(text)

            if op == C.PUBLISH_DENIED:
                await self.handle_publish_denied(fields, addr)
            elif op == C.MESSAGE:
                await self.handle_message(fields, addr)
            elif op == C.COMMENT:
                await self.handle_comment(fields, addr)
            else:
                debug(f"[UDP] Unknown op: {op}")

        except ProtocolError as e:
            ui(f"ERROR|UDP protocol error: {e}")
        except Exception as e:
            ui(f"ERROR|UDP receive failed: {e}")

    async def handle_publish_denied(self, fields, addr):
        ui(f"PUBLISH-DENIED|{fields[1]}")

    async def handle_message(self, fields, addr):
        ui(f"MESSAGE|{fields[0]}|{fields[1]}|{fields[2]}|{fields[3]}")

    async def handle_comment(self, fields, addr):
        ui(f"COMMENT|{fields[0]}|{fields[1]}|{fields[2]}|{fields[3]}")
