import socket
from _thread import *
import pickle
from entities.Ship import Ship

class Server:
    MAX_PLAYERS = 2
    PLAYER = 0
    
    def __init__(self):
        self.server = "localhost" #192.168.1.24
        self.port = 5555
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.players = []

        try:
            self.socket.bind((self.server, self.port))
        except socket.error as e:
            str(e)

        self.socket.listen(self.MAX_PLAYERS)
        print("Waiting for a connection, Server Started")

    def connect(self):
        conn, addr = self.socket.accept()
        print("Connected to:", addr)
        self.players.append(Ship().to_dict())

        start_new_thread(self.threaded_client, (conn, self.PLAYER))
        self.PLAYER += 1

    def threaded_client(self, conn, player):
        conn.send(pickle.dumps(self.players[player]))
        reply = ""
        while True:
            try:
                try:
                    data = pickle.loads(conn.recv(20480))
                except EOFError as e:
                    print(e)
                    break
                self.players[player] = data

                if not data:
                    print("Disconnected")
                    break
                else:
                    reply = self.players
                    print("Received: ", data)
                    print("Sending: ", reply)

                conn.sendall(pickle.dumps(reply))
            except Exception as e:
                print(e)
                break

        self.players.pop(player)
        self.PLAYER -= 1
        print("Lost connection")
        conn.close()

if __name__ == "__main__":
    server = Server()
    while True:
        server.connect()