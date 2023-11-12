import pygame
import os
import math
from math import *

class Rock():
    def __init__(self, x, y):
        self.rock_img = pygame.image.load(os.path.join("assets", "rock.png"))
        self.surf = pygame.Surface((60, 60))
        self.rock = pygame.transform.smoothscale(self.rock_img, (60, 60))
        self.rect = self.rock.get_rect(x=x, y=y)
        self.x, self.y = x, y
        self.rot = 5

    def rotate(self):
        rotated_image = pygame.transform.rotate(self.rock, self.rot)
        new_rect = rotated_image.get_rect(center = self.rock.get_rect(center = (self.x, self.y)).center)

        self.rot += 0.2

        return rotated_image, new_rect

    def draw(self,screen):
        screen.blit(self.rotate()[0], self.rotate()[1])
