import socket
class Server():
    def __init__(self,server_ip,server_port):
        self.s = socket.socket()
        self.ServerOn = True
        HOST = server_ip
        PORT = server_port
        self.s.bind((HOST, PORT))
        self.s.listen(5)
        print("TCP Server Created")
    def listen(self):
        c, addr = self.s.accept()
        data = str(c.recv(1024))
        c.close()
        print data
        return data
    