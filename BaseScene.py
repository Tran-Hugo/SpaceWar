import pygame
class BaseScene:
    def __init__(self):
        self.next = self

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    
    def ProcessInput(self, events):
        print("uh-oh, you didn't override this in the child class")

    def Update(self):
        print("uh-oh, you didn't override this in the child class")

    def Render(self, screen):
        print("uh-oh, you didn't override this in the child class")

    def SwitchToScene(self, next_scene):
        self.next = next_scene

    def Terminate(self):
        self.SwitchToScene(None)