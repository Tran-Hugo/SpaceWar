from scenes.BaseScene import BaseScene
from scenes.MainScene import MainScene
import pygame

class EntryScene(BaseScene):
    def __init__(self):
        BaseScene.__init__(self)
        self.message = "Press any key"
        pygame.font.init() 
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render(self.message, True,(0, 255, 0))

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.SwitchToScene(MainScene())
    
    def Render(self, screen):
        # For the sake of brevity, the title scene is a blank red screen
        screen.fill((0, 0, 0))
        # print(screen)
        screen.blit(self.text, (100,100))
