import pygame
from gameplay_loop import GameplayLoop
from crafting_loop import CraftinglayLoop

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN|pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.running = True

        self.gameplay_loop = GameplayLoop(self)
        self.crafting_loop = CraftinglayLoop(self)
        self.change_to_gameplay_loop()
    
    def change_to_gameplay_loop(self):
        self.current_group = self.gameplay_loop
    
    def change_to_crafting_loop(self):
        self.crafting_loop.crafting.start()
        self.current_group = self.crafting_loop 
    
    def render(self):
        self.screen.fill('black')
        self.current_group.render()
        pygame.display.update()

    def main_loop(self):
        while self.running:
            self.clock.tick(60)
            self.current_group.get_events()
            self.render()
            self.current_group.update()
    
if __name__ == '__main__':
    game = Game()
    game.main_loop()