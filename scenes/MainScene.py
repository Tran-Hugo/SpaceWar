from entities.Rock import Rock
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
        self.ship = Ship()
    
    def ProcessInput(self, events, pressed_keys):
        if pressed_keys[pygame.K_UP] and self.ship.rect.y > 0 :
            self.ship.velocity[1] = -1
        elif pressed_keys[pygame.K_DOWN] and self.ship.rect.y < self.config.getHeight() - self.ship.rect.height :
            self.ship.velocity[1] = 1
        else:
            self.ship.velocity[1] = 0

        if pressed_keys[pygame.K_LEFT] and self.ship.rect.x > 0 :
            self.ship.velocity[0] = -1
        elif pressed_keys[pygame.K_RIGHT] and self.ship.rect.x < self.config.getWidth() - self.ship.rect.width:
            self.ship.velocity[0] = 1
        else:
            self.ship.velocity[0] = 0

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    opposite = mouse_y - self.ship.rect.y
                    adjacent = mouse_x - self.ship.rect.x
                    angle = math.atan2(opposite, adjacent)
                    self.ship.bullets.append(Bullet(self.ship.rect.x, self.ship.rect.y, angle))

    def Update(self):
        self.ship.move()   

    def Render(self, screen):
        # For the sake of brevity, the title scene is a blank red screen
        screen.fill((0, 0, 0))
        self.ship.draw(screen)
        for bullet in self.ship.bullets:
            bullet.move()
            bullet.draw()
            if bullet.rect.x < 0 or bullet.rect.x > self.config.getWidth() or bullet.rect.y < 0 or bullet.rect.y > self.config.getHeight():
                self.ship.bullets.remove(bullet)
