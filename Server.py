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
from entities.Bullet import Bullet

class Server:
    MAX_PLAYERS = 2
    PLAYER = 0
    # TPF = 1/60 # Time per frame
    
    def __init__(self):
        self.server = "localhost" #192.168.1.24 | 192.168.1.123
        self.port = 5555
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.players = []
        self.rocks = []
        self.score = 0
        self.explosions = []
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
        new_player = Ship()
        self.players.append(new_player)
        if len(self.rocks) == 0:
            self.rocks = []

            for i in range(random.randint(4, 7)):
                x = random.uniform(0, Config.getWidth())
                y = random.uniform(0, Config.getHeight())

                while Config.getWidth() / 2 - 30 <= x <= Config.getWidth() / 2 + 30 and Config.getHeight() / 2 - 30 <= y <= Config.getHeight() / 2 + 30:
                    x = random.uniform(0, Config.getWidth())
                    y = random.uniform(0, Config.getHeight())
                    
                self.rocks.append(Rock({'x': x, 'y': y, 'size': 1, 'speed': random.uniform(1, 6), 'angle': random.uniform(0, 2 * math.pi)}))
        start_new_thread(self.threaded_client, (conn, new_player))
        self.PLAYER += 1

    def update_main_thread(self):
        while True:
            for ship in self.players:
                ship.update_invincibility()
                if ship.lifes <= 0:
                    self.players.remove(ship)
            for rock in self.rocks:
                rock.float()
                rock.check_collision(self.players)
                res = rock.check_bullet_collision(self.players, self.rocks, self.score)
                self.score = res['score']

                for explosion in res['explosion']:
                    self.explosions.append(explosion)
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
        reply = ""
        while True:
            # start_time = time.time()
            try:
                try:
                    data = pickle.loads(conn.recv(100000))
                except EOFError as e:
                    print('Error :', e)
                    break

                if ('event' in data and data['event'] == 'shot'):
                    print("Shot")
                    for player in self.players:
                        if player.uuid == data['player_uuid']:
                            player.bullets.append(Bullet(player.rect.x, player.rect.y, data['bullet_angle']))
                            break
                if ('event' in data and data['event'] == 'delete_explosion'):
                    print("Delete explosion")
                    for explosion in self.explosions:
                        if explosion.uuid in data['explosion_uuid']:
                            self.explosions.remove(explosion)
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
                if ('event' in data and data['event'] == 'new_rocks'):
                    for i in range(random.randint(2,5)):
                        x = random.randint(0,500)
                        y = random.randint(0,500)
                        for player in self.players:
                            if(player.rect.x <= x <= player.rect.x + 60 and player.rect.y <= y <= player.rect.y + 60):
                                x = player.rect.x + 100
                                y = player.rect.y + 100
                        self.rocks.append(Rock({'x':x,'y':y, 'size':1, 'speed': random.uniform(1, 3), 'angle': random.uniform(0, 2 * math.pi)}))

                if ('event' in data and data['event'] == 'quit'):
                    print("Quit")
                    for ship in self.players:
                        if ship.uuid == data['uuid']:
                            self.players.remove(ship)
                            break

                if ('event' in data and data['event'] == 'update'):
                    for player in self.players:
                        for bullet in player.bullets:
                            bullet.move()
                            if bullet.rect.x < 0 or bullet.rect.x > Config.getWidth() or bullet.rect.y < 0 or bullet.rect.y > Config.getHeight():
                                player.bullets.remove(bullet)

                rock_dicts = []
                ship_dicts = []
                explosion_dicts = []
                for rock in self.rocks:
                    rock_dicts.append(rock.to_dict())
                for ship in self.players:
                    ship_dicts.append(ship.to_dict())

                for explosion in self.explosions:
                    explosion_dicts.append(explosion.to_dict())

                if not data:
                    print("Disconnected")
                    break
                else:
                    reply = {
                        "players": ship_dicts, 
                        "rocks": rock_dicts,
                        "explosions": explosion_dicts,
                        "score": self.score
                    }
                    print("Received: ", data)
                    print("Sending: ", reply)
                # print(f"Taille des données à envoyer : {len(pickle.dumps(reply))} octets")
                conn.sendall(pickle.dumps(reply))
            except Exception as e:
                print('Error :', e)
                break
            # end_time = time.time()
            # frame_time = end_time - start_time
            # if frame_time < self.TPF:
            #     sleep_time = self.TPF - frame_time
            #     time.sleep(sleep_time)
        
        self.PLAYER -= 1
        print("Lost connection")
        conn.close()

if __name__ == "__main__":
    server = Server()
    while True:
        server.connect()