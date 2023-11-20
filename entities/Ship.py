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
        self.invincible_duration = 1
        self.invincible_timer = 0
        self.blink_interval = 0.2  # Intervalle de clignotement en secondes
        self.last_blink_time = 0
        self.visible = True
        self.invincible_i = 0
    
    def move(self):
        self.rect.move_ip(self.velocity[0] * self.speed, self.velocity[1] * self.speed)

    def shoot(self, network):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        opposite = mouse_y - self.rect.y
        adjacent = mouse_x - self.rect.x
        angle = math.atan2(opposite, adjacent)
        players = network.send({'event': 'shot', 'player_uuid' : self.uuid, 'bullet_angle': angle})['players']
        for player in players:
            if player['uuid'] == self.uuid:
                self.from_dict(player)
                break
        blaster_sound = pygame.mixer.Sound(os.getcwd()+"/assets/sounds/blaster2.mp3")
        blaster_sound.play()
    
    def lose_life(self):
        self.lifes -=1
        if self.lifes <= 0:
            print('you loose')
        else:
            self.invincible = True
            self.invincible_timer = time.time()
            self.last_blink_time = time.time()

    def update_invincibility(self):
        self.visible = not self.visible
        if self.invincible and time.time() - self.invincible_timer >= self.invincible_duration:
            self.invincible = False

    def update_blink(self):
        # Clignotement du vaisseau pendant l'invincibilité
        current_time = time.time()
        if self.invincible and current_time - self.last_blink_time >= self.blink_interval:
            self.last_blink_time = current_time

    def draw(self,screen):
        self.update_invincibility()
        self.update_blink()
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 1) #Debug hitbox

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
            "bullets": [],
            "lifes": self.lifes,
            "invincible": self.invincible,
            "invincible_timer": self.invincible_timer,
            "last_blink_time": self.last_blink_time,
            "visible": self.visible,
        }

        for bullet in self.bullets:
            res["bullets"].append(bullet.to_dict())
        return res
    
    def from_dict(self, data):
        self.uuid = data["uuid"]
        self.rect.x = data["x"]
        self.rect.y = data["y"]
        self.speed = data["speed"]
        self.velocity = data["velocity"]
        self.lifes = data["lifes"]
        self.invincible = data["invincible"]
        self.invincible_timer = data["invincible_timer"]
        self.last_blink_time = data["last_blink_time"]
        self.visible = data["visible"]

        if len(self.bullets) == 0:
            for bullet in data["bullets"]:
                new_bullet = Bullet(bullet['x'], bullet['y'], bullet['angle'])
                new_bullet.from_dict(bullet)
                self.bullets.append(new_bullet)
                continue
        else : 
            self_ids = set([bullet.uuid for bullet in self.bullets])
            data_ids = set([bullet['uuid'] for bullet in data["bullets"]])
            diff = self_ids.difference(data_ids)
            for bullet in self.bullets:
                if bullet.uuid in diff:
                    self.bullets.remove(bullet)

            for bullet in data["bullets"]:
                if bullet['uuid'] in self_ids:
                    for b in self.bullets:
                        if b.uuid == bullet['uuid']:
                            b.from_dict(bullet)
                    continue
                
                new_bullet = Bullet(bullet['x'], bullet['y'], bullet['angle'])
                new_bullet.from_dict(bullet)
                self.bullets.append(new_bullet)
