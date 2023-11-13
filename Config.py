# singleton class for configuration
import pygame

class Config():
    __instance = None
    __width = 720
    __height = 480
    __fps = 60
    __screen = None
    
    @staticmethod
    def getInstance():
        if Config.__instance == None:
            Config()
        return Config.__instance

    def __init__(self):
        if Config.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Config.__instance = self
            Config.__width = 720
            Config.__height = 480
            Config.__fps = 60
            Config.__screen = pygame.display.set_mode((Config.__width, Config.__height))
    def getWidth(self):
        return self.__width
    def setWidth(self, width):
        self.__width = width

    def getHeight(self):
        return self.__height
    def getFps(self):
        return self.__fps
    

    def getScreen(self):
        return self.__screen
    def setScreen(self, screen):
        self.__screen = screen
    def regenerateScreen(self):
        self.__screen = pygame.display.set_mode((self.__width, self.__height))