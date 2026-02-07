import socket

s = socket.socket()
s.connect(("127.0.0.1",10000))

msg = "|REGISTER|1|Alice|127.0.0.1|5000|6000|\n"
s.sendall(msg.encode())

print(s.recv(1024).decode())

s.close()
