from entities.Heart import Heart
from entities.Rock import Rock
from entities.Score import Score
from scenes.BaseScene import BaseScene
from entities.Ship import Ship
import pygame
from Config import Config
from network import Network

class MainScene(BaseScene):
    def __init__(self):
        BaseScene.__init__(self)
        pygame.font.init()
        self.rocks = []
        self.players = []
        self.config = Config.getInstance()
        self.network = Network()
        self.ship = None
        self.init_game()
        self.score = Score()
        self.heart = Heart()
        self.explosion_group = pygame.sprite.Group()
    
    def init_game(self):
        initial_data = self.network.getObj()
        for rock in initial_data['rocks']:
            self.rocks.append(Rock(rock))
        for player in initial_data['players']:
            self.ship = Ship(player)
            self.players.append(self.ship)

    def ProcessInput(self, events, pressed_keys):
        if self.ship is not None:
            if pressed_keys[pygame.K_z] and self.ship.rect.y > 0 :
                self.network.send({"event": "move", "direction": "up", "uuid": self.ship.uuid})

            elif pressed_keys[pygame.K_s] and self.ship.rect.y < Config.getHeight() - self.ship.rect.height :
                self.network.send({"event": "move", "direction": "down", "uuid": self.ship.uuid})

            if pressed_keys[pygame.K_q] and self.ship.rect.x > 0 :
                self.network.send({"event": "move", "direction": "left", "uuid": self.ship.uuid})
                
            elif pressed_keys[pygame.K_d] and self.ship.rect.x < Config.getWidth() - self.ship.rect.width:
                self.network.send({"event": "move", "direction": "right", "uuid": self.ship.uuid})
                
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.ship.shoot(self.network)

    def Update(self):
        state = self.network.send({"event": "update"})
        updated_rocks = state['rocks']
        updated_players = state['players']
        if len(self.players) < len(updated_players):
            for updated_ship in updated_players:
                if updated_ship['uuid'] not in [ship.uuid for ship in self.players]:
                    self.players.append(Ship(updated_ship))

        for updated_rock in updated_rocks:
            for rock in self.rocks:
                if rock.uuid == updated_rock['uuid']:
                    rock.from_dict(updated_rock)

        for ship in self.players:
            for updated_ship in updated_players:
                if ship.uuid == updated_ship['uuid']:
                    ship.from_dict(updated_ship)
                    self.heart.update_life(ship)

        # if len(self.rocks) == 0:
        #     for i in range(random.randint(2,5)):
        #         x = random.randint(0,500)
        #         y = random.randint(0,500)
        #         if(self.ship.x <= x <= self.ship.x + 60 and self.ship.y <= y <= self.ship.y + 60):
        #             x = self.ship.rect.x + 100
        #             y = self.ship.rect.y + 100
        #         self.rocks.append(Rock(x, y))

    def Render(self, screen):
        screen.fill((0, 0, 0))
        
        for rock in self.rocks:
            rock.draw(screen)
        self.explosion_group.draw(screen)
        for ship in self.players:
            ship.draw(screen)
            for bullet in ship.bullets:
                    bullet.draw()
        self.heart.draw(screen)
        self.score.draw()

        
