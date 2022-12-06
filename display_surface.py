import pygame

class DisplaySurface:
    def __init__(self, size, **pos) -> None:
        self.surface = pygame.Surface(size, flags = pygame.SRCALPHA)
        self.rect = self.surface.get_rect(**pos)
    
    def get_size(self):
        return self.surface.get_size()
    
    def get_height(self):
        return self.surface.get_width()
    
    def fill(self, color):
        self.surface.fill(color)
    
    def set_alpha(self, value):
        self.surface.set_alpha(value)
    
    def clear(self):
        self.surface = pygame.Surface(self.get_size(), flags = pygame.SRCALPHA)