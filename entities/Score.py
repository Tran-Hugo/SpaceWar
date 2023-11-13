import pygame
from Config import Config

class Score():

    def __init__(self) :
       self.score = 0
       self.config = Config.getInstance()
       self.font = pygame.font.Font(None, 36)
       self.text = self.font.render(str(self.score), True,(255, 255, 255))

    def add(self, points):
        self.score += points
        self.text = self.font.render(str(self.score), True,(255, 255, 255))
        
    def draw(self):
        self.config.getScreen().blit(self.text, (25,15))