import pygame
import os
from Config import Config

class Ship():
    def __init__(self):
        self.config = Config.getInstance()
        self.image_filename = os.path.join("assets", "player.png")
        self.rect = self.get_image().get_rect(x=self.config.getWidth() / 2, y=self.config.getHeight() / 2)
        self.speed = 4
        self.velocity = [0,0]
        self.bullets = []
    
    def move(self):
        self.rect.move_ip(self.velocity[0] * self.speed, self.velocity[1] * self.speed)
    
    def draw(self,screen):
        screen.blit(self.get_image(), self.rect)

    def get_image(self):
        return pygame.image.load(self.image_filename)
    
    def to_dict(self):
        res = {
            "x": self.rect.x,
            "y": self.rect.y,
            "speed": self.speed,
            "velocity": self.velocity,
            "bullets": []
        }

        for bullet in self.bullets:
            res["bullets"].append(bullet.to_dict())
        return res
    
    def from_dict(self, data):
        self.rect.x = data["x"]
        self.rect.y = data["y"]
        self.speed = data["speed"]
        self.velocity = data["velocity"]
        self.bullets = data["bullets"]
