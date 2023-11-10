from BaseScene import BaseScene
import pygame

class MainScene(BaseScene):
    def __init__(self):
        BaseScene.__init__(self)
        self.message = "MAIN"
        pygame.font.init() 
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render(self.message, True,(0, 255, 0))
    
    def Render(self, screen):
        # For the sake of brevity, the title scene is a blank red screen
        screen.fill((0, 0, 0))

        screen.blit(self.text, (100,100))
