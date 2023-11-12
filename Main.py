import pygame
from scenes.EntryScene import EntryScene
from Config import Config

def run(fps, starting_scene):
        pygame.init()
        config = Config.getInstance()
        screen = config.getScreen()
        clock = pygame.time.Clock()

        active_scene = starting_scene

        while active_scene != None:
            pressed_keys = pygame.key.get_pressed()
            filtered_events = []
            for event in pygame.event.get():
                quit_attempt = False
                if event.type == pygame.QUIT:
                    quit_attempt = True
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_ESCAPE) or (pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT] and event.key == pygame.K_F4) :
                        quit_attempt = True

                if quit_attempt:
                    active_scene.Terminate()
                else:
                    filtered_events.append(event)
            active_scene.handling_events()
            active_scene.ProcessInput(filtered_events, pressed_keys)
            active_scene.Update()
            active_scene.Render(screen)

            active_scene = active_scene.next

            pygame.display.flip()
            clock.tick(fps)

run(60, EntryScene())