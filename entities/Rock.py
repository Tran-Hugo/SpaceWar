import random
import uuid
import pygame
import os
import math
from math import *

from Config import Config
from entities.Explosion import Explosion

class Rock():
    def __init__(self, data):
        if "uuid" in data:
            self.uuid = data["uuid"]
        else:
            self.uuid = str(uuid.uuid4())
        self.rock_img = pygame.image.load(os.path.join("assets", "rock.png"))
        self.surf = pygame.Surface((60, 60))
        self.original_size = 60  # Taille originale du rocher
        self.size = data["size"]  # Facteur de taille, 1 par défaut (taille normale)
        self.rock = pygame.transform.smoothscale(self.rock_img, (int(self.original_size * data['size']), int(self.original_size * data['size'])))
        # self.rock = pygame.transform.smoothscale(self.rock_img, (60, 60))
        self.rect = self.rock.get_rect(center= (data["x"],data["y"]))
        self.x, self.y = data["x"], data["y"]
        self.rot = 5

        self.speed = data["speed"]
        self.angle = data["angle"]

        # self.config = Config.getInstance()
        self.screen_width = Config.getWidth()
        self.screen_height = Config.getHeight()

    def rotate(self):
        rotated_image = pygame.transform.rotate(self.rock, self.rot)
        new_rect = rotated_image.get_rect(center=(self.x, self.y))
        self.rot += 0.2

        return rotated_image, new_rect
    
    def float(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        if self.x < 0:
            self.x = self.screen_width
        elif self.x > self.screen_width:
            self.x = 0

        if self.y < 0:
            self.y = self.screen_height
        elif self.y > self.screen_height:
            self.y = 0

        self.rect.center = (self.x, self.y)

    def check_collision(self, ships):
        for ship in ships:
            if self.rect.colliderect(ship.rect) and ship.invincible == False:
                ship.lose_life()          
                return True
        return False
    
    def check_bullet_collision(self, ships, rocks, explosion_group, score):
        for ship in ships:
            for bullet in ship.bullets:
                if self.rect.colliderect(bullet.rect):
                    ship.bullets.remove(bullet)
                    explosion = Explosion(self.x,self.y)
                    explosion_group.add(explosion)
                    rocks.remove(self)
                    if self.size > 0.5:
                        score.add(100)
                        for i in range(random.randint(1,4)):
                            rocks.append(Rock(self.x,self.y,self.size/2))
                    else:
                        score.add(200)
        return False
    
    def to_dict(self):
        res = {
            "uuid": self.uuid,
            "x": self.x,
            "y": self.y,
            "size": self.size,
            "speed": self.speed,
            "angle": self.angle,
        }
        return res
    
    def from_dict(self, data):
        self.uuid = data["uuid"]
        self.x = data["x"]
        self.y = data["y"]
        self.size = data["size"]
        self.speed = data["speed"]
        self.angle = data["angle"]
        self.rect = self.rock.get_rect(center= (self.x,self.y))
    
    def draw(self,screen):
        rotated_image, new_rect = self.rotate()
        # pygame.draw.rect(self.config.getScreen(), (255, 0, 0), self.rect, 1) # debug
        screen.blit(rotated_image, new_rect)
