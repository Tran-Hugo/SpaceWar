import socket
import pickle

from entities.Rock import Rock

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.123" # 192.168.1.24
        self.port = 5555
        self.addr = (self.server, self.port)
        self.obj = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            data = pickle.loads(self.client.recv(104824))
            print("Received: ", data)
            # if isinstance(data, list) and all(isinstance(rock, Rock) for rock in data):
            #     self.rocks = data
            #     print("Received rocks:", self.rocks)
            # else:
            #     print("Received unexpected data:", data)
            return data
        except socket.error as e:
            print(e)
    
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(104824))
        except socket.error as e:
            print(e)

    def getObj(self):
        return self.obj