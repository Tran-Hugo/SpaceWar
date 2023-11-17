import random
from entities.Heart import Heart
from entities.Rock import Rock
from entities.Score import Score
from scenes.BaseScene import BaseScene
from entities.Ship import Ship
import pygame
import math
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
        self.init_game()
        self.score = Score()
        # self.ship = Ship()
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
                state = self.network.send({"event": "move", "direction": "up", "uuid": self.ship.uuid})

            elif pressed_keys[pygame.K_s] and self.ship.rect.y < Config.getHeight() - self.ship.rect.height :
                state = self.network.send({"event": "move", "direction": "down", "uuid": self.ship.uuid})
            else:
                self.ship.velocity[1] = 0

            if pressed_keys[pygame.K_q] and self.ship.rect.x > 0 :
                state = self.network.send({"event": "move", "direction": "left", "uuid": self.ship.uuid})
                self.ship.velocity[0] = -1
            elif pressed_keys[pygame.K_d] and self.ship.rect.x < Config.getWidth() - self.ship.rect.width:
                state = self.network.send({"event": "move", "direction": "right", "uuid": self.ship.uuid})
                self.ship.velocity[0] = 1
            else:
                self.ship.velocity[0] = 0

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.ship.shoot(self.network)

    def Update(self):
        ship_dict = self.ship.to_dict()
        state = self.network.send({"test": "input"})
        print("state = " + str(state))

        updated_rocks = state['rocks']
        updated_players = state['players']
        if len(self.players) < len(updated_players):
            for updated_ship in updated_players:
                if updated_ship['uuid'] not in [ship.uuid for ship in self.players]:
                    self.players.append(Ship(updated_ship))
        # for rock, updated_rock in zip(self.rocks, updated_rocks):
        # for updated_rock in updated_rocks:
        #     # rock.from_dict(updated_rock)
        #     self.rocks[self.rocks.index(updated_rock)].from_dict(updated_rock)
        for updated_rock in updated_rocks:
            for rock in self.rocks:
                if rock.uuid == updated_rock['uuid']:
                    rock.from_dict(updated_rock)

        for ship in self.players:
            for updated_ship in updated_players:
                if ship.uuid == updated_ship['uuid']:
                    ship.from_dict(updated_ship)

            
        if self.ship is not None:
            self.heart.update_life(self.ship)
            self.ship.move()
            # for rock in self.rocks:
            #     rock.float()
            #     if rock.check_collision([self.ship]):
            #         print("lifes = "+ str(self.ship.lifes))
            #     rock.check_bullet_collision([self.ship], self.rocks, self.explosion_group, self.score)
            # self.explosion_group.update()
            if self.ship.lifes <= 0:
                self.heart.update_life(self.ship)
                self.remove_ship()
            # for ship in self.players:
            #     new_ship = Ship()
            #     new_ship.from_dict(ship)
                # ship.move()
            #     self.players[self.players.index(ship)] = new_ship
            #     print(ship)
        # else :
            # for rock in self.rocks:
            #     rock.float()
            #     rock.check_collision([])
            #     rock.check_bullet_collision([], self.rocks, self.explosion_group, self.score)
            # self.explosion_group.update()
            # for ship in self.players:
            #     new_ship = Ship()
            #     new_ship.from_dict(ship)
            #     new_ship.move()
            #     self.players[self.players.index(ship)] = new_ship
        if len(self.rocks) == 0:
            for i in range(random.randint(2,5)):
                x = random.randint(0,500)
                y = random.randint(0,500)
                if(self.ship.x <= x <= self.ship.x + 60 and self.ship.y <= y <= self.ship.y + 60):
                    x = self.ship.rect.x + 100
                    y = self.ship.rect.y + 100
                self.rocks.append(Rock(x, y))

    def remove_ship(self):
        self.ship = None

    def Render(self, screen):
        screen.fill((0, 0, 0))
        if self.ship is None:
            for rock in self.rocks:
                rock.draw(screen)
            self.explosion_group.draw(screen)
            font = pygame.font.Font(None, 36)
            text = font.render("You Lose", True, (255, 255, 255))
            text_rect = text.get_rect(center=(Config.getWidth() / 2, Config.getHeight() / 2))
            screen.blit(text, text_rect)
            for ship in self.players:
                ship.draw(screen)
                for bullet in ship.bullets:
                    bullet.move()
                    bullet.draw()
                    if bullet.rect.x < 0 or bullet.rect.x > Config.getWidth() or bullet.rect.y < 0 or bullet.rect.y > Config.getHeight():
                        ship.bullets.remove(bullet)
        else:
            for rock in self.rocks:
                rock.draw(screen)
            self.explosion_group.draw(screen)

            for ship in self.players:
                ship.draw(screen)
                print("ship = ", ship.bullets)
                for bullet in ship.bullets:
                    bullet.draw()
                    
        self.heart.draw(screen)
        self.score.draw()

        
