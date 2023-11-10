from BaseScene import BaseScene
from Ship import Ship
import pygame

class MainScene(BaseScene):
    def __init__(self):
        BaseScene.__init__(self)
        pygame.font.init()
        self.ship = Ship(100,100)
    
    def ProcessInput(self, events, pressed_keys):
        if pressed_keys[pygame.K_LEFT]:
            self.ship.velocity[0] = -1
        elif pressed_keys[pygame.K_RIGHT]:
            self.ship.velocity[0] = 1
        else:
            self.ship.velocity[0] = 0

        if pressed_keys[pygame.K_UP]:
            self.ship.velocity[1] = -1
        elif pressed_keys[pygame.K_DOWN]:
            self.ship.velocity[1] = 1
        else:
            self.ship.velocity[1] = 0

    def Update(self):
        self.ship.move()       

    def Render(self, screen):
        # For the sake of brevity, the title scene is a blank red screen
        screen.fill((0, 0, 0))
        self.ship.draw(screen)
