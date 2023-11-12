import pygame
import os
import math
from Config import Config

class Bullet():
    SPEED = 5

    def __init__(self, x, y, angle = 0) :
        self.config = Config.getInstance()
        self.img = pygame.image.load(os.path.join("assets", "bullet.png"))
        self.img = pygame.transform.rotate(self.img, -math.degrees(angle) - 90)
        self.rect = self.img.get_rect(center = (x,y))
        offset = pygame.math.Vector2(20, 0) # Offset the bullet from the ship
        self.pos = pygame.math.Vector2(x, y) + offset
        self.velocity = pygame.math.Vector2(1, 0).rotate(math.degrees(angle)) * self.SPEED
        self.angle = angle

    def move(self):
        self.pos += self.velocity
        self.rect.center = self.pos
        # vector = pygame.math.Vector2()
        # vector.from_polar((self.SPEED, math.degrees(self.angle)))
        # self.pos = (self.pos + vector)
        # self.rect.center = round(self.pos[0]), round(self.pos[1])
        
    def draw(self):
        self.config.getScreen().blit(self.img, self.rect)
        # pygame.draw.rect(self.config.getScreen(), (255, 0, 0), self.rect, 1) # debug