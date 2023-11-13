import pygame
from pygame.locals import *
import sys
import json
import socket

class Lobby:
    def __init__(self):
        pygame.init()
        self.create_page()

    def create_page(self):
        window_width = 400
        window_height = 200
        black = (0, 0, 0)
        white = (255, 255, 255)

        screen = pygame.display.set_mode((window_width, window_height), RESIZABLE)
        pygame.display.set_caption('Input Pygame')

        font = pygame.font.Font(None, 36)
        instruction_text = font.render('Nom joueur:', True, white)

        input_rect = pygame.Rect(150, 50, 200, 50)
        input_color = white
        input_text = ''

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.send_data_to_server(input_text)
                        input_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

            screen.fill(black)
            pygame.draw.rect(screen, input_color, input_rect, 2)
            screen.blit(instruction_text, (50, 10))
            input_surface = font.render(input_text, True, white)
            screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))
            pygame.display.flip()

    def send_data_to_server(self, data):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 59001))
        serialized_data = json.dumps({"name": data}).encode('utf-8')
        client_socket.send(serialized_data)
        client_socket.close()

if __name__ == '__main__':
    lobby = Lobby()
