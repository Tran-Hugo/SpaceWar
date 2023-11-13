import random
from entities.Heart import Heart
from entities.Rock import Rock
from entities.Score import Score
from scenes.BaseScene import BaseScene
from entities.Ship import Ship
import pygame
import math
from Config import Config
from entities.Bullet import Bullet

class MainScene(BaseScene):
    def __init__(self):
        BaseScene.__init__(self)
        pygame.font.init()
        self.config = Config.getInstance()
        self.score = Score()
        self.ship = Ship()
        self.heart = Heart()
        self.rocks = [Rock(200,250),Rock(300,150),Rock(500,300)]
        self.explosion_group = pygame.sprite.Group()
    
    def ProcessInput(self, events, pressed_keys):
        if self.ship is not None:
            if pressed_keys[pygame.K_z] and self.ship.rect.y > 0 :
                self.ship.velocity[1] = -1
            elif pressed_keys[pygame.K_s] and self.ship.rect.y < self.config.getHeight() - self.ship.rect.height :
                self.ship.velocity[1] = 1
            else:
                self.ship.velocity[1] = 0

            if pressed_keys[pygame.K_q] and self.ship.rect.x > 0 :
                self.ship.velocity[0] = -1
            elif pressed_keys[pygame.K_d] and self.ship.rect.x < self.config.getWidth() - self.ship.rect.width:
                self.ship.velocity[0] = 1
            else:
                self.ship.velocity[0] = 0

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.ship.shoot()

    def Update(self):
        if self.ship is not None:
            self.heart.update_life(self.ship)
            self.ship.move()
            for rock in self.rocks:
                rock.float()
                if rock.check_collision([self.ship]):
                    print("lifes = "+ str(self.ship.lifes))
                rock.check_bullet_collision([self.ship], self.rocks, self.explosion_group, self.score)
            self.explosion_group.update()
            if self.ship.lifes <= 0:
                self.heart.update_life(self.ship)
                self.remove_ship()
        else :
            for rock in self.rocks:
                rock.float()
                rock.check_collision([])
                rock.check_bullet_collision([], self.rocks, self.explosion_group, self.score)
            self.explosion_group.update()
        if len(self.rocks) == 0:
            for i in range(random.randint(2,5)):
                x = random.randint(0,500)
                y = random.randint(0,500)
                print(self.ship.x, self.ship.y)
                if(self.ship.x <= x <= self.ship.x + 60 and self.ship.y <= y <= self.ship.y + 60):
                    x = self.ship.rect.x + 100
                    y = self.ship.rect.y + 100
                self.rocks.append(Rock(x, y))

    def remove_ship(self):
        self.ship = None

    def Render(self, screen):
        screen.fill((0, 0, 0))
        self.score.draw()
        self.heart.draw(screen)
        if self.ship is None:
            for rock in self.rocks:
                rock.draw(screen)
            self.explosion_group.draw(screen)
            font = pygame.font.Font(None, 36)
            text = font.render("You Lose", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.config.getWidth() / 2, self.config.getHeight() / 2))
            screen.blit(text, text_rect)
        else:
            self.ship.draw(screen)
            for bullet in self.ship.bullets:
                bullet.move()
                bullet.draw()
                if bullet.rect.x < 0 or bullet.rect.x > self.config.getWidth() or bullet.rect.y < 0 or bullet.rect.y > self.config.getHeight():
                    self.ship.bullets.remove(bullet)
            for rock in self.rocks:
                rock.draw(screen)
            self.explosion_group.draw(screen)
