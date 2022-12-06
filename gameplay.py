import pygame
from ground import Ground
from player import Player
from support import *
from settings import *

class Gameplay:
    def __init__(self) -> None:
        self.events = {'w': False, 'a':False, 's':False, 'd':False}

        self.visible_sprites = CustomCamera()
        self.updatable_sprites = pygame.sprite.Group()
        self.obsticle_sprites = pygame.sprite.Group()

        self.ground = Ground(self)
        self.player = Player(groups=[self.visible_sprites, self.updatable_sprites], pos=(500, 500), z=layers['player'])
    
    def clear_events(self):
        for key in self.events.keys(): self.events[key] = False

    def render(self, screen):
        self.visible_sprites.custom_draw(self.player)
        self.player.inventory.sprite.render(screen)
        self.player.render(screen)

    def update(self):
        self.updatable_sprites.update(self)
        self.ground.update()

    def use_item(self):
        self.player.use_item(self)

class CustomCamera(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_heigth = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
    
    def custom_draw(self, player: Player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_heigth

        for sprite in sorted(self.sprites(), key = lambda sprite: (sprite.z, sprite.rect.centery)):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos, special_flags = sprite.special_flag)
