import asyncio
from abc import ABC, abstractmethod
from protocol.codec import decode_line, encode, ProtocolError
from protocol import constants as C

class BaseClient(ABC):

    def __init__(self, name, rq_counter, is_registered, subjects):
        self.client_ip = self.get_my_ip()
        self.server_ip = '0.0.0.0'

        self.server_port = 0
        self.udp_port = 0 #listen port for udp
        self.tcp_port = 0 #listen port for tcp

        # In async, we manage 'reader' and 'writer' objects instead of sock
        self.writer = None
        self.reader = None

        self.name = name
        self.rq_counter = rq_counter
        self.is_registered = is_registered
        self.subjects = subjects

    @abstractmethod
    async def send_message(self, message: str):
        #Must be an async method.
        pass

    async def get_next_rq(self):
        self.rq_counter += 1
        return self.rq_counter

    async def close(self):
        #Closes the stream writer safely.
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
            print(f"Connection to {self.server_ip}:{self.server_port} closed.")
    
    async def get_my_ip(self):
        try:
            loop = asyncio.get_running_loop()
            
            # We create a temporary transport just to send the packet
            transport, protocol = await loop.create_datagram_endpoint(
                lambda: asyncio.DatagramProtocol(),
                remote_addr=('8.8.8.8', 1)
            )
            #get its own ip address
            return transport.get_extra_info('sockname')[0]
        except Exception as e:
            print(f"[UDP] Error: {e}")
        finally:
            transport.close()

# --- TCP Implementation ---

class TcpClient(BaseClient):

    def __init__(self, name, rq_counter, is_registered, subjects):
        super().__init__( name, rq_counter, is_registered, subjects)

    async def start_client(self, server_ip, server_port):
        listener = await asyncio.start_server(self.handle_incoming_peer, '0.0.0.0', 0)
        self.tcp_port = listener.sockets[0].getsockname()[1]

        # saving values for potential reconnection logic
        self.server_ip = server_ip
        self.server_port = server_port

        self.connect(self.server_ip, self.server_port)

    async def connect(self, server_ip, server_port):
        try:
            self.reader, self.writer = await asyncio.wait_for(
                asyncio.open_connection(server_ip, server_port), 
                timeout=5.0
            )
            #get tcp port #
            address_info = self.writer.get_extra_info('sockname')
            self.tcp_port = address_info[1]
            print(f"[TCP] Connected to {self.server_ip}:{self.server_port}")
            
            # Start the background listener task
            self._listen_task = asyncio.create_task(self.listen_forever())
            return True
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError) as e:
            print(f"[TCP] Connection failed: {e}")
            return False

    async def send_message(self, message: str):
        if not self.writer or self.writer.is_closing():
            print("[TCP] Error: Not connected. Attempting to Reconnect...")
            if self.connect(self, self.server_ip, self.server_port):
                print("[TCP] Successfully Reconnected")
            else:
                return

        try:
            # Ensure the message ends with a newline for the protocol
            if not message.endswith('\n'):
                message += '\n'
                
            self.writer.write(message.encode())
            await self.writer.drain()
            print(f"[TCP] Sent: {message.strip()}")
        except Exception as e:
            print(f"[TCP] Send error: {e}")
            await self.close()

    async def listen_forever(self):
        try:
            while True:
                # readline() is better than read(4096) because it respects the \n framing used in the encode/decode logic.
                line = await self.reader.readline()
                
                if not line:
                    print("[TCP] Server closed the connection.")
                    break
                
                print(f"[TCP] Received: {line.decode().strip()}")
                self.handle_server_message(line)
                
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"[TCP] Listener error: {e}")
        finally:
            await self.close()

    #REGISTER
    async def register(self):
        msg = encode(C.REGISTER, self.rq_counter, self.name, self.client_ip, self.tcp_port, self.udp_port)
        self.send_message(msg)
        
    #DEREGISTRATION
    async def deregister(self):
        msg = encode(C.DE_REGISTER, self.rq_counter, self.name)
        self.send_message(msg)

    #UPDATE
    async def update(self):
        msg = encode(C.REGISTER, self.rq_counter, self.name, self.client_ip, self.tcp_port, self.udp_port)
        self.send_message(msg)

    #SUBJECTS
    async def subjects(self, *fields):
        msg = encode(C.REGISTER, self.rq_counter, self.name, *fields)
        self.send_message(msg)

    def handle_server_message(self, data):
        op, fields = decode_line(data)

        if op == C.REGISTERED:
            self.handle_registered(fields)
        elif op == C.REGISTER_DENIED:
            self.handle_register_denied(fields)
        elif op == C.REFER:
            self.handle_refer(fields)
        elif op == C.UPDATE_CONFIRMED:
            self.handle_update_confirmed(fields)
        elif op == C.UPDATE_DENIED:
            self.handle_update_denied(fields)
        elif op == C.SUBJECTS_UPDATED:
            self.handle_subjects_updated(fields)
        elif op == C.SUBJECTS_REJECTED:
            self.handle_subjects_rejected(fields)
        else:
            self.ctx.log.warning(f"UDP unknown op: {op}") 

    #HANDLERS
    async def handle_registered(self, fields):
        print(f"User Registered (RQ# {fields[0]})")

    async def handle_register_denied(self, fields):
        print(f"User Registration Denied (RQ# {fields[0]}) | Reason: {fields[1]}")
        #TODO
        #retry or give up
        #when gives up, tcp connection closed
        self.close()

    async def handle_refer(self, fields):
        print(f"User Referred (RQ# {fields[0]}) | New IP Address: {fields[1]}")

    async def handle_update_confirmed(self, fields):
        print(f"Update Confirmed (RQ# {fields[0]})")

    async def handle_update_denied(self, fields):
        print(f"Update Denied (RQ# {fields[0]}) | Reason: {fields[1]}")
        self.close()
    
    async def handle_subjects_updated(self, fields):
        print(f"Subjects Updated (RQ# {fields[0]})")

    async def handle_subjects_rejected(self, fields):
        print(f"Subjects Update Rejected (RQ# {fields[0]}) | List of Subjects: {fields[2:]}")
        #TODO
        #user can retry as many times as needed
        #close TCP connection when done
        self.close()

# --- UDP Implementation ---

class UdpClient(BaseClient):

    #HELPER FN
    async def send_message(self, message: str):
        loop = asyncio.get_running_loop()
        
        # We create a temporary transport just to send the packet
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: asyncio.DatagramProtocol(),
            remote_addr=(self.server_ip, self.server_port)
        )
        
        #get client udp port #
        self.udp_port = transport.get_extra_info('sockname')[1]

        try:
            transport.sendto(message.encode())
            print(f"[UDP] Sent: {message}")
        except Exception as e:
            print(f"[UDP] Error: {e}")
        finally:
            transport.close()

    #PUBLISH
    async def publish(self, Subject, Title, Text):
        #send msg to server
        msg = encode(C.PUBLISH, self.rq_counter, self.name, Subject, Title, Text)
        self.send_message(self, msg)

    #PUBLISH-COMMENT
    async def publish_comment(self, Subject, Title, Text):
        #send msg to server
        msg = encode(C.PUBLISH_COMMENT, self.name, Subject, Title, Text)
        self.send_message(self, msg)

    #LISTENER
    async def datagram_received(self, data, addr):
        try:
            #TODO add proper logs
            text = data.decode()
            self.ctx.log.info(f"UDP RX from {addr}: {text.strip()}")

            op, fields = decode_line(text)

            if op == C.PUBLISH_DENIED:
                self.handle_publish_denied(fields, addr)

            elif op == C.MESSAGE:
                self.handle_message(fields, addr)

            elif op == C.COMMENT:
                self.handle_comment(fields, addr)

            else:
                self.ctx.log.warning(f"UDP unknown op: {op}")

        except ProtocolError as e:
            self.ctx.log.warning(f"UDP protocol error from {addr}: {e}")
        except Exception as e:
            self.ctx.log.error(f"UDP error from {addr}: {e}")

    #HANDLERS
    async def handle_publish_denied(self, fields, addr):
        #print message
        print(f"Publish Denied by {addr} (RQ# {fields[0]}): {fields[1]}")

    async def handle_message(self, fields, addr):
        #if publish error, sender receives this
        if fields[0]==self.name:
            print(f"Message sent back from {addr}\nWritten by: {fields[0]}\nSubject: {fields[1]}\nTitle: {fields[2]}\n{fields[3]}")
        else:
            #if not user who sent it, print message
            print(f"Message Received from {addr}\nWritten by: {fields[0]}\nSubject: {fields[1]}\nTitle: {fields[2]}\n{fields[3]}")

    async def handle_comment(self, fields, addr):
        print(f"Comment Received from {addr}\nWritten by: {fields[0]}\nSubject: {fields[1]}\nTitle: {fields[2]}\n{fields[3]}")