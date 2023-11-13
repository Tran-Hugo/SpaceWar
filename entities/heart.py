import time
import pygame
import os
from Config import Config
from PIL import Image

class Heart():
    def __init__(self):
        self.life = 3
        self.heart_image = pygame.image.load(os.path.join("assets", "full_heart.png")).convert_alpha()
        self.heart_width, self.heart_height = 30, 30

    def lose_life(self):
        if self.life > 0:
            self.life -= 1

    def draw_hearts(self, surface):
        x, y = 10, 10
        heart_spacing = 5
        for _ in range(self.life):
            surface.blit(self.heart_image, (x, y))
            x += self.heart_width + heart_spacing

    def draw(self, screen):
        
        self.draw_hearts(screen)

# Exemple d'utilisation dans votre programme principal :
# heart = Heart()
# heart.get_damage()  # Appliquer des dégâts
# heart.get_health()  # Récupérer de la vie
# heart.draw(screen)  # Dessiner les cœurs sur l'écran
