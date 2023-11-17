import math
import time
import uuid
import pygame
import os
from Config import Config
from entities.Bullet import Bullet

class Ship():
    def __init__(self, data= None):
        if data is not None:
            # print("data = " + str(data))
            self.uuid = data["uuid"]
        else:
            self.uuid = str(uuid.uuid4())
        self.image_filename = os.path.join("assets", "player.png")
        self.rect = self.get_image().get_rect(x=Config.getWidth() / 2, y=Config.getHeight() / 2)
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

    def shoot(self, network):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        opposite = mouse_y - self.rect.y
        adjacent = mouse_x - self.rect.x
        angle = math.atan2(opposite, adjacent)
        bullets = network.send({'event': 'shot', 'player_uuid' : 0, 'bullet_angle': angle})['players'][0]['bullets']
        if len(self.bullets) == 0:
            for bullet in bullets:
                new_bullet = Bullet(bullet['x'], bullet['y'], bullet['angle'])
                new_bullet.from_dict(bullet)
                self.bullets.append(new_bullet)
                continue

        for bullet in bullets:
            for self_bullet in self.bullets:
                if bullet['uuid'] == self_bullet.uuid:
                    break
                else:
                    new_bullet = Bullet(bullet['x'], bullet['y'], bullet['angle'])
                    new_bullet.from_dict(bullet)
                    self.bullets.append(new_bullet)
                    print('Test 1', self.bullets)
                    break

    
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
            screen.blit(self.get_image(), self.rect)

    def get_image(self):
        return pygame.image.load(self.image_filename)
    
    def to_dict(self):
        res = {
            "uuid": self.uuid,
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
        if len(self.bullets) == 0:
            for bullet in data["bullets"]:
                new_bullet = Bullet(bullet['x'], bullet['y'], bullet['angle'])
                new_bullet.from_dict(bullet)
                self.bullets.append(new_bullet)
                continue
        else : 
            for bullet in data["bullets"]:
                for self_bullet in self.bullets:
                    if bullet['uuid'] == self_bullet.uuid:
                        self_bullet.from_dict(bullet)
                        break
                    else:
                        new_bullet = Bullet(bullet['x'], bullet['y'], bullet['angle'])
                        new_bullet.from_dict(bullet)
                        self.bullets.append(new_bullet)

