import pygame
from gameplay import Gameplay

class GameplayLoop:
    def __init__(self, main) -> None:
        self.main = main
        self.gameplay = Gameplay()
    
    def render(self):
        self.gameplay.render(self.main.screen)
    
    def update(self):
        self.gameplay.update()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.main.screen = pygame.display.set_mode((1344, 758), pygame.SCALED)
                if event.key == pygame.K_w:
                    self.gameplay.events['w'] = True
                if event.key == pygame.K_a:
                    self.gameplay.events['a'] = True
                if event.key == pygame.K_s:
                    self.gameplay.events['s'] = True
                if event.key == pygame.K_d:
                    self.gameplay.events['d'] = True
                if event.key == pygame.K_SPACE:
                    self.gameplay.use_item()
                if event.key == pygame.K_1:
                    self.gameplay.player.change_item(True)
                if event.key == pygame.K_2:
                    self.gameplay.player.change_item(False)
                if event.key == pygame.K_e:
                    self.gameplay.clear_events()
                    self.main.change_to_crafting_loop()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.gameplay.events['w'] = False
                if event.key == pygame.K_a:
                    self.gameplay.events['a'] = False
                if event.key == pygame.K_s:
                    self.gameplay.events['s'] = False
                if event.key == pygame.K_d:
                    self.gameplay.events['d'] = False

    


