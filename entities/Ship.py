import pygame
import os
from Config import Config

class Ship():
    def __init__(self):
        self.config = Config.getInstance()
        self.player = pygame.image.load(os.path.join("assets", "player.png"))
        self.rect = self.player.get_rect(x=self.config.getWidth() / 2, y=self.config.getHeight() / 2)
        self.speed = 4
        self.velocity = [0,0]
        self.bullets = []
    
    def move(self):
        self.rect.move_ip(self.velocity[0] * self.speed, self.velocity[1] * self.speed)
    
    def draw(self,screen):
        screen.blit(self.player, self.rect)
