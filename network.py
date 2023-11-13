import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost" # 192.168.1.24
        self.port = 5555
        self.addr = (self.server, self.port)
        self.obj = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(20480))
        except socket.error as e:
            print(e)
    
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(20480))
        except socket.error as e:
            print(e)

    def getObj(self):
        return self.obj