import math
import random
import socket
from _thread import *
import threading
import time
import pickle
from Config import Config
from entities.Rock import Rock
from entities.Ship import Ship

class Server:
    MAX_PLAYERS = 2
    PLAYER = 0
    
    def __init__(self):
        self.server = "localhost" #192.168.1.24
        self.port = 5555
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.players = []
        self.rocks = []
        self.rocks_lock = threading.Lock()
        self.players_lock = threading.Lock()
        self.update_thread = threading.Thread(target=self.update_main_thread)
        self.update_thread.start()


        try:
            self.socket.bind((self.server, self.port))
        except socket.error as e:
            str(e)

        self.socket.listen(self.MAX_PLAYERS)
        print("Waiting for a connection, Server Started")

    def connect(self):
        conn, addr = self.socket.accept()
        print("Connected to:", addr)
        self.players.append(Ship())
        if self.PLAYER == 0:
            self.rocks = []
            self.rocks.append(Rock({'x':100,'y':100, 'size':1, 'speed': random.uniform(1, 6), 'angle': random.uniform(0, 2 * math.pi)}))
            self.rocks.append(Rock({'x':300,'y':200, 'size':1, 'speed': random.uniform(1, 6), 'angle': random.uniform(0, 2 * math.pi)}))
            self.rocks.append(Rock({'x':700,'y':300, 'size':1, 'speed': random.uniform(1, 6), 'angle': random.uniform(0, 2 * math.pi)}))
        start_new_thread(self.threaded_client, (conn, self.PLAYER))
        self.PLAYER += 1

    def update_main_thread(self):
        while True:
            for ship in self.players:
                ship.update_invincibility()
            # with self.rocks_lock:
            for rock in self.rocks:
                rock.float()
                rock.check_collision(self.players)
            time.sleep(0.05)
    
    def threaded_client(self, conn, player):
        rock_dicts = []
        ship_dicts = []
        for rock in self.rocks:
            rock_dicts.append(rock.to_dict())
        for ship in self.players:
            ship_dicts.append(ship.to_dict())
        initial_data = {
            "rocks": rock_dicts,
            "players": ship_dicts,
        }
        print("Sending initial: ", initial_data)
        conn.send(pickle.dumps(initial_data))
        # conn.send(pickle.dumps(self.players[player]))
        reply = ""
        while True:
            rock_dicts = []
            ship_dicts = []
            for rock in self.rocks:
                rock_dicts.append(rock.to_dict())
            for ship in self.players:
                ship_dicts.append(ship.to_dict())
            try:
                try:
                    data = pickle.loads(conn.recv(100000))
                except EOFError as e:
                    print(e)
                    break

                if ('event' in data and data['event'] == 'move'):
                    # find the ship by its uuid
                    for ship in self.players:
                        if ship.uuid == data['uuid']:
                            if data['direction'] == 'up' and ship.rect.y > 0:
                                ship.velocity[1] = -1
                            elif data['direction'] == 'down' and ship.rect.y < Config.getHeight():
                                ship.velocity[1] = 1
                            else:
                                ship.velocity[1] = 0
        
                            if data['direction'] == 'left' and ship.rect.x > 0:
                                ship.velocity[0] = -1
                            elif data['direction'] == 'right' and ship.rect.x < Config.getWidth():
                                ship.velocity[0] = 1
                            else:
                                ship.velocity[0] = 0
                            ship.move()
                            
                    pass
                # for ship in self.players:
                #     shipId = ship.uuid
                #     if ship.uuid == data['uuid']:
                #         ship.from_dict(data)

                if not data:
                    print("Disconnected")
                    break
                else:
                    reply = {"players": ship_dicts, "rocks": rock_dicts}
                #     print("Received: ", data)
                #     print("Sending: ", reply)
                # print(f"Taille des données à envoyer : {len(pickle.dumps(reply))} octets")
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