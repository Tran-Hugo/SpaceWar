import math
import time
import pygame
import os
from Config import Config
from entities.Bullet import Bullet

class Ship():
    def __init__(self):
        self.config = Config.getInstance()
        self.player = pygame.image.load(os.path.join("assets", "player.png"))
        self.rect = self.player.get_rect(x=self.config.getWidth() / 2, y=self.config.getHeight() / 2)
        self.speed = 4
        self.velocity = [0,0]
        self.bullets = []
        self.lifes = 3
        self.invincible = False
        self.invincible_duration = 3
        self.invincible_timer = 0
        self.blink_interval = 0.2  # Intervalle de clignotement en secondes
        self.last_blink_time = 0
        self.visible = True
    
    def move(self):
        self.rect.move_ip(self.velocity[0] * self.speed, self.velocity[1] * self.speed)

    def shoot(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        opposite = mouse_y - self.rect.y
        adjacent = mouse_x - self.rect.x
        angle = math.atan2(opposite, adjacent)
        self.bullets.append(Bullet(self.rect.x, self.rect.y, angle))
    
    def lose_life(self):
        self.lifes -=1
        if self.lifes <= 0:
            print('you loose')
        else:
            self.invincible = True
            self.invincible_timer = time.time()
            self.last_blink_time = time.time()

    def update_invincibility(self):
        if self.invincible and time.time() - self.invincible_timer >= self.invincible_duration:
            self.invincible = False

    def update_blink(self):
        # Clignotement du vaisseau pendant l'invincibilité
        current_time = time.time()
        if self.invincible and current_time - self.last_blink_time >= self.blink_interval:
            self.last_blink_time = current_time
            self.visible = not self.visible

    def draw(self,screen):
        self.update_invincibility()
        self.update_blink()

        if not self.invincible or (self.invincible and self.visible):
            screen.blit(self.player, self.rect)
