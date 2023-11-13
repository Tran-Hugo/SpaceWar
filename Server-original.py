import socket
from _thread import *

MAX_PLAYERS = 2

server = "localhost" # 192.168.1.24
port = 5555

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    socket.bind((server, port))
except socket.error as e:
    str(e)

socket.listen(MAX_PLAYERS)
print("Waiting for a connection, Server Started")

pos = [(0,0), (100,100)]
PLAYERS = 0

def decode_pos(pos):
    pos = pos.split(",")
    return int(pos[0]), int(pos[1])
    
def encode_pos( pos):
    return str(pos[0]) + "," + str(pos[1])

def threaded_client(conn, player):
    conn.send(str.encode(encode_pos(pos[player])))
    reply = ""
    while True:
        try:
            data = decode_pos(conn.recv(2048).decode())
            pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                print("Received: ", data)
                print("Sending: ", reply)

            conn.sendall(str.encode(encode_pos(reply)))
        except:
            break

    print("Lost connection")
    conn.close()

while True:
    conn, addr = socket.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, PLAYERS))
    PLAYERS += 1