import asyncio
from abc import ABC, abstractmethod
from protocol.codec import decode_line, encode, ProtocolError
from protocol import constants as C

class BaseClient(ABC):
    DEFAULT_TCP_PORT = 10000
    DEFAULT_UDP_PORT = 20000

    def __init__(self, host: str, port: int, name: str, rq_counter: int, is_registered: bool, subjects):
        self.host = host
        self.port = port

        # In async, we manage 'reader' and 'writer' objects instead of sock
        self.writer = None
        #self.reader = None

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
            print(f"Connection to {self.host}:{self.port} closed.")

# --- TCP Implementation ---

class TcpClient(BaseClient):

    BUFFER_SIZE = 4096

    def __init__(self, host, port, name, rq_counter, is_registered, subjects, local_ip, local_tcp):
        super().__init__(host, port, name, rq_counter, is_registered, subjects)

    async def send_message(self, message: str):
        try:
            # open_connection performs the handshake and returns a reader and writer
            reader, self.writer = await asyncio.wait_for(
                asyncio.open_connection(self.host, self.port), 
                timeout=5.0
            )
            
            self.writer.write(message.encode())
            await self.writer.drain() # Ensure data is actually sent
            print(f"[TCP] Sent: {message}")

            # Wait for response
            data = await reader.read(4096)
            print(f"Server said: {data.decode()}")
            
        except asyncio.TimeoutError:
            print("The TCP server took too long to respond!")
        except Exception as e:
            print(f"[TCP] Error: {e}")
        finally:
            await self.close()

    #"REGISTER, RQ#, Name, IP, TCP_Port, UDP_Port"
    async def register(self, server_ip, server_port):
        try:
            # open_connection performs the handshake and returns a reader and writer
            reader, self.writer = await asyncio.wait_for(
                asyncio.open_connection(self.host, self.port), 
                timeout=5.0
            )
            # Create and send message
            message = f"REGISTER {self.rq_counter} {self.name} {self.ip_addr} {self.tcp_port} {self.udp_port}\n"
            self.writer.write(message.encode())
            await self.writer.drain() # Ensure data is actually sent
            print(f"[TCP] Sent: {message}")

            # Wait for response
            data = await reader.read(4096)
            response = data.decode()
            print(f"Server said: {response}")

            split = response.split(' ')
            if split[0] == "REGISTERED":
                 print(f"Registration Successful (RQ# {split[1]})")

            elif split[0] == "REGISTER-DENIED":
                reason = " ".join(split[2:])
                print(f"Registration Successful (RQ# {split[1]}): {reason}")
                #TODO : retry or retry after waiting depending on the reason
            elif split[0] == "REFER":
                print(f"Referring to new Server (RQ# {split[1]}): {split[2]})")
                #TODO : when client IP address not in the server's range, connect to new server address
                # close current server connection and connect to new server
                self.register(split[2], server_port)
            
        except asyncio.TimeoutError:
            print("The TCP server took too long to respond!")
        except Exception as e:
            print(f"[TCP] Error: {e}")
        finally:
            await self.close()
            self.rq_counter += 1

    #DEREGISTRATION

    #UPDATE

    #"SUBJECTS, RQ#, Name, List_of_subjects"

# --- UDP Implementation ---

class UdpClient(BaseClient):
    async def send_message(self, message: str):
        loop = asyncio.get_running_loop()
        
        # We create a temporary transport just to send the packet
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: asyncio.DatagramProtocol(),
            remote_addr=(self.host, self.port)
        )
        
        try:
            transport.sendto(message.encode())
            print(f"[UDP] Sent: {message}")
        except Exception as e:
            print(f"[UDP] Error: {e}")
        finally:
            transport.close()

    #"PUBLISH, RQ#, Name, Subject, Title, Text"

    #"PUBLISH-COMMENT, Name, Subject, Title, Text"

    #LISTENER FOR NEWS