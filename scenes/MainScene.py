import sys
from entities.Heart import Heart
from entities.Rock import Rock
from entities.Score import Score
from scenes.BaseScene import BaseScene
from entities.Ship import Ship
from entities.Explosion import Explosion
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
        self.game_over = False
    
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
                if event.type == pygame.QUIT:
                    self.network.send({"event": "quit","uuid": self.ship.uuid})
                    pygame.quit()
                    sys.exit()

    def Update(self):
        state = self.network.send({"event": "update"})
        updated_rocks = state['rocks']
        updated_players = state['players']
        explosions = state['explosions']
        self.score.set(state['score'])

        for explosion in explosions:
            if explosion['uuid'] not in [explosion.uuid for explosion in self.explosion_group]:
                new_explosion = Explosion(explosion['x'], explosion['y'])
                new_explosion.from_dict(explosion)
                self.explosion_group.add(new_explosion)
        self.explosion_group.update()
        if (len(self.explosion_group) > 0):
            self.network.send({"event": "delete_explosion", "explosion_uuid": [explosion.uuid for explosion in self.explosion_group]})
        

        if len(self.players) < len(updated_players):
            for updated_ship in updated_players:
                if updated_ship['uuid'] not in [ship.uuid for ship in self.players]:
                    self.players.append(Ship(updated_ship))

        if len(self.players) > len(updated_players):
            players_to_remove = []
            for ship in self.players:
                if updated_players:
                    for updated_ship in updated_players:
                        if ship.uuid == updated_ship['uuid']:
                            break
                        else :
                            players_to_remove.append(ship)
                else:
                    players_to_remove.append(ship)

            for ship in players_to_remove:
                self.players.remove(ship)

        self.updateRocks(updated_rocks)

        for ship in self.players:
            for updated_ship in updated_players:
                if ship.uuid == updated_ship['uuid']:
                    ship.from_dict(updated_ship)
                    if self.ship.uuid == ship.uuid: #met à jour uniquement le vaisseau du joueur
                        if ship.lifes == 0:
                            self.game_over = True
                        self.heart.update_life(ship)

        if len(self.rocks) == 0:
            self.network.send({"event": "new_rocks"})

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
        if self.game_over:
            font = pygame.font.Font(None, 36)
            text = font.render("You Lose", True, (255, 255, 255))
            text_rect = text.get_rect(center=(Config.getWidth() / 2, Config.getHeight() / 2))
            screen.blit(text, text_rect)
        

    def updateRocks(self, rocks):
        self_rocks = [rock.uuid for rock in self.rocks]
        updated_rocks = [rock['uuid'] for rock in rocks]
        diff = set(self_rocks).difference(updated_rocks)
        for rock in self.rocks:
            if rock.uuid in diff:
                self.rocks.remove(rock)

        for updated_rock in rocks:
            if updated_rock['uuid'] in self_rocks:
                for rock in self.rocks:
                    if rock.uuid == updated_rock['uuid']:
                        rock.from_dict(updated_rock)
                continue

            new_rock = Rock(updated_rock)
            self.rocks.append(new_rock)
            
