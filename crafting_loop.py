import pygame
from crafting import Crafting

class CraftinglayLoop:
    def __init__(self, main) -> None:
        self.main = main
        self.crafting = Crafting(self.main.gameplay_loop.gameplay.player)
    
    def render(self):
        self.main.gameplay_loop.gameplay.render(self.main.screen)
        self.crafting.render(self.main.screen)
    
    def update(self):
        self.main.gameplay_loop.gameplay.update()
    
    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.main.screen = pygame.display.set_mode((1344, 758), pygame.SCALED)

                if event.key == pygame.K_e:
                    self.main.change_to_gameplay_loop()
                if event.key == pygame.K_a:
                    self.crafting.turn_left()
                if event.key == pygame.K_d:
                    self.crafting.turn_right()
                if event.key == pygame.K_SPACE:
                    self.crafting.craft()
                if event.key == pygame.K_w:
                    self.crafting.go_up()
                if event.key == pygame.K_s:
                    self.crafting.go_down()