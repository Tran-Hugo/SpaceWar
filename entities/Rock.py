import random
import pygame
import os
import math
from math import *

from Config import Config
from entities.Explosion import Explosion

class Rock():
    def __init__(self, x, y):
        self.rock_img = pygame.image.load(os.path.join("assets", "rock.png"))
        self.surf = pygame.Surface((60, 60))
        self.rock = pygame.transform.smoothscale(self.rock_img, (60, 60))
        self.rect = self.rock.get_rect(center= (x,y))
        self.x, self.y = x, y
        self.rot = 5

        self.speed = random.uniform(1, 3)
        self.angle = random.uniform(0, 2 * math.pi)

        self.config = Config.getInstance()
        self.screen_width = self.config.getWidth()
        self.screen_height = self.config.getHeight()

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
    
    def check_bullet_collision(self, ships, rocks, explosion_group):
        for ship in ships:
            for bullet in ship.bullets:
                if self.rect.colliderect(bullet.rect):
                    ship.bullets.remove(bullet)
                    explosion = Explosion(self.x,self.y)
                    explosion_group.add(explosion)
                    rocks.remove(self)
        return False
    
    def draw(self,screen):
        rotated_image, new_rect = self.rotate()
        # pygame.draw.rect(self.config.getScreen(), (255, 0, 0), self.rect, 1) # debug
        screen.blit(rotated_image, new_rect)
