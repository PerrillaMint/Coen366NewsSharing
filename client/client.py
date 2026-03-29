import asyncio
from abc import ABC, abstractmethod
from protocol.codec import decode_line, encode, ProtocolError
from protocol import constants as C

class BaseClient(ABC):
    
    def __init__(self, ctx, name, rq_counter, is_registered, subjects_list):
        self.ctx = ctx
        self.client_ip = '0.0.0.0'
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
        self.subjects_list = subjects_list

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
            await self.writer.wait_closed()  # type: ignore
            print(f"Connection to {self.server_ip}:{self.server_port} closed.")
    
    async def get_my_ip(self):
        transport = None
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
            if transport:
                transport.close()

# --- TCP Implementation ---

class TcpClient(BaseClient):

    def __init__(self, ctx,name, rq_counter, is_registered, subjects):
        super().__init__( ctx, name, rq_counter, is_registered, subjects)

    async def start_client(self, server_ip, server_port):
        # saving values for potential reconnection logic
        self.server_ip = server_ip
        self.server_port = server_port

        # Discover client IP with asyncio transport helper (async call)
        self.client_ip = await self.get_my_ip()

        await self.connect(self.server_ip, self.server_port)

    async def connect(self, server_ip, server_port):
        try:
            self.reader, self.writer = await asyncio.wait_for(
                asyncio.open_connection(server_ip, server_port), 
                timeout=5.0
            )
            #get tcp port #
            address_info = self.writer.get_extra_info('sockname')
            self.tcp_port = address_info[1]
            self.ctx.log.info(f"[TCP Client] Connected to {self.server_ip}:{self.server_port}")
            
            # Start the background listener task
            self._listen_task = asyncio.create_task(self.listen_forever())
            return True
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError) as e:
            self.ctx.log.error(f"[TCP Client] Connection failed: {e}")
            return False

    async def send_message(self, message: str):
        if not self.writer or self.writer.is_closing():
            self.ctx.log.error(f"[TCP Client] Error: Not connected. Attempting to Reconnect to {self.server_ip}:{self.server_port}...")
            success = await self.connect(self.server_ip, self.server_port)
            if success:
               self.ctx.log.info(f"[TCP Client] Successfully Reconnected to {self.server_ip}:{self.server_port}")  
            else:
                return

        try:
            # Ensure the message ends with a newline for the protocol
            if not message.endswith('\n'):
                message += '\n'
                
            self.writer.write(message.encode())
            await self.writer.drain()
            self.ctx.log.info(f"[TCP Client] Sent: {message.strip()}")
            await self.get_next_rq()
        except Exception as e:
            self.ctx.log.error(f"[TCP Client] Send error: {e}")
            await self.close()

    async def listen_forever(self):
        try:
            while True:
                # readline() is better than read(4096) because it respects the \n framing used in the encode/decode logic.
                line = await self.reader.readline()
                
                if not line:
                    self.ctx.log.info(f"[TCP Client] Server closed the connection.")
                    break
                
                self.ctx.log.info(f"[TCP Client] Received: {line.decode().strip()}")
                await self.handle_server_message(line)
                
        except asyncio.CancelledError:
            pass
        except Exception as e:
            self.ctx.log.error(f"[TCP Client] Listener error: {e}")
        finally:
            await self.close()

    #REGISTER
    async def register(self):
        msg = encode(C.REGISTER, self.rq_counter, self.name, self.client_ip, self.tcp_port, self.udp_port)
        await self.send_message(msg)
        
    #DEREGISTRATION
    async def deregister(self):
        msg = encode(C.DE_REGISTER, self.rq_counter, self.name)
        await self.send_message(msg)

    #UPDATE
    async def update(self):
        msg = encode(C.UPDATE, self.rq_counter, self.name, self.client_ip, self.tcp_port, self.udp_port)
        await self.send_message(msg)

    #SUBJECTS
    async def subjects(self, *fields):
        msg = encode(C.SUBJECTS, self.rq_counter, self.name, *fields)
        await self.send_message(msg)

    async def handle_server_message(self, data):
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
        else:
            self.ctx.log.error(f"[TCP Client] Unknown op: {op}") 

    #HANDLERS
    async def handle_registered(self, fields):
        self.ctx.log.info(f"[TCP Client] User Registered (RQ# {fields[0]})")

    async def handle_register_denied(self, fields):
        self.ctx.log.error(f"[TCP Client] User Registration Denied (RQ# {fields[0]}) | Reason: {fields[1]}")
        #retry or give up
        if self.rq_counter < 3:  # Arbitrary retry limit
            self.ctx.log.info(f"[TCP Client] Retrying registration (Attempt {self.rq_counter + 1})...")
            await self.register()
        else:            self.ctx.log.error(f"[TCP Client] Registration failed after {self.rq_counter} attempts. Giving up.")

        #when gives up, tcp connection closed
        await self.close()

    async def handle_refer(self, fields):
        self.ctx.log.info(f"[TCP Client] User Referred (RQ# {fields[0]}) | New IP Address: {fields[1]}")
        #close current connection and connect to new IP
        await self.close()
        self.server_port = self.server_port + 1
        await self.start_client(fields[1], self.server_port)
        await self.register()
         

    async def handle_update_confirmed(self, fields):
        self.ctx.log.info(f"[TCP Client] Update Confirmed (RQ# {fields[0]})")

    async def handle_update_denied(self, fields):
        self.ctx.log.error(f"[TCP Client] Update Denied (RQ# {fields[0]}) | Reason: {fields[1]}")
        await self.close()
    
    async def handle_subjects_updated(self, fields):
        self.ctx.log.info(f"[TCP Client] Subjects Updated (RQ# {fields[0]})")

    async def handle_subjects_rejected(self, fields):
        self.ctx.log.error(f"[TCP Client] Subjects Update Rejected (RQ# {fields[0]}) | List of Subjects: {fields[2:]}")
        #TODO
        #user can retry as many times as needed
        #close TCP connection when done
        await self.close()

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
            self.ctx.log.info(f"[UDP Client] Sent: {message}")
        except Exception as e:
            self.ctx.log.error(f"[UDP Client] Error: {e}")
        finally:
            transport.close()

    #PUBLISH
    async def publish(self, Subject, Title, Text):
        #send msg to server
        msg = encode(C.PUBLISH, self.rq_counter, self.name, Subject, Title, Text)
        await self.send_message(msg)

    #PUBLISH-COMMENT
    async def publish_comment(self, Subject, Title, Text):
        #send msg to server
        msg = encode(C.PUBLISH_COMMENT, self.name, Subject, Title, Text)
        await self.send_message(msg)

    #LISTENER
    async def datagram_received(self, data, addr):
        try:
            
            text = data.decode()
            self.ctx.log.info(f"[UDP Client] RX from {addr}: {text.strip()}")

            op, fields = decode_line(text)

            if op == C.PUBLISH_DENIED:
                await self.handle_publish_denied(fields, addr)

            elif op == C.MESSAGE:
                await self.handle_message(fields, addr)

            elif op == C.COMMENT:
                await self.handle_comment(fields, addr)

            else:
                self.ctx.log.error(f"[UDP Client] Unknown op: {op}")

        except ProtocolError as e:
            self.ctx.log.error(f"[UDP Client] Protocol error from {addr}: {e}")
        except Exception as e:
            self.ctx.log.error(f"[UDP Client] Error from {addr}: {e}")

    #HANDLERS
    async def handle_publish_denied(self, fields, addr):
        #print message
        self.ctx.log.error(f"[UDP Client] Publish Denied by {addr} (RQ# {fields[0]}): {fields[1]}")

    async def handle_message(self, fields, addr):
        #if publish error, sender receives this
        if fields[0]==self.name:
            self.ctx.log.info(f"[UDP Client] Message sent back from {addr}\nWritten by: {fields[0]}\nSubject: {fields[1]}\nTitle: {fields[2]}\n{fields[3]}")
        else:
            #if not user who sent it, print message
            self.ctx.log.info(f"[UDP Client] Message Received from {addr}\nWritten by: {fields[0]}\nSubject: {fields[1]}\nTitle: {fields[2]}\n{fields[3]}")

    async def handle_comment(self, fields, addr):
        self.ctx.log.info(f"[UDP Client] Comment Received from {addr}\nWritten by: {fields[0]}\nSubject: {fields[1]}\nTitle: {fields[2]}\n{fields[3]}")