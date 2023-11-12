import pygame
import os
from Config import Config
from PIL import Image
class Ship():
    def __init__(self):
        self.config = Config.getInstance()
        self.player = pygame.image.load(os.path.join("assets", "player.png"))
        self.rect = self.player.get_rect(center=(self.config.getWidth() / 2, self.config.getHeight() / 2))
        self.speed = 4
        self.velocity = [0, 0]
        self.bullets = []
        self.heath = 5
        self.max_health = 1
        self.life= 3
        self.full_heart = pygame.image.load(os.path.join("assets", "full_heart.png")).convert_alpha()
        self.heart_width, self.heart_height = 30, 30
        
         
    def get_dammage(self):
        if self.health > 0:
            self.health -= 1
    
    def get_health(self):
        if self.health < self.max_health:
            self.health += 1
    def full_heart(self):
        for heart in range(self.health):
            screen.blit(full_heart,(heart * 50, 45))
    def draw_hearts(self, surface, num_hearts):
        x, y = 10, 10
        heart_spacing = 5

        for _ in range(num_hearts):
            surface.blit(self.full_heart, (x, y))
            x += self.heart_width + heart_spacing # la largeur des coeurs ainsi que l'espace qu'il y a entre les coeurs
            
    def move(self):
        self.rect.move_ip(self.velocity[0] * self.speed, self.velocity[1] * self.speed)
    from PIL import Image



    def draw(self, screen):
        screen.blit(self.player, self.rect)
        self.draw_hearts(screen, self.life)
