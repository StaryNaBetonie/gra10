import pygame
from settings import *
from support import *
from random import randrange

class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, image, hitbox_offset=(0.2, 0.8), z=layers['ground'], special_flag = 0, **pos) -> None:
        super().__init__(groups)
        self.z = z
        self.image = image
        self.rect = self.image.get_rect(**pos)
        self.hitbox = self.rect.copy().inflate(-self.rect.width * hitbox_offset[0], -self.rect.height * hitbox_offset[1])
        self.special_flag = special_flag

class SoilTile(Tile):
    def __init__(self, groups, tileset, hitbox_offset=(0.2, 0.8), z=layers['soil'], special_flag = 0, **pos) -> None:
        self.tileset = tileset
        self.status = '________'
        super().__init__(groups=groups, image = self.tileset[self.status], hitbox_offset=hitbox_offset, z=z, special_flag=special_flag, **pos)
    
    def update(self, grid, point):
        col = self.hitbox.top // TILE_SIZE
        row = self.hitbox.left // TILE_SIZE
        top = 'S' in grid[col - 1][row]
        bottom = 'S' in grid[col + 1][row]
        left = 'S' in grid[col][row - 1]
        right = 'S' in grid[col][row + 1]

        self.status = ''

        if top: self.status += 'X'
        else: self.status += '_'
        if bottom: self.status += 'X'
        else: self.status += '_'
        if left: self.status += 'X'
        else: self.status += '_'
        if right: self.status += 'X'
        else: self.status += '_'

        self.status += '____'
        self.image = self.tileset[self.status]

class Plant(Tile):
    def __init__(self, groups, type, hitbox_offset=(0.2, 0.8), z=layers['plants'], special_flag = 0, **pos) -> None:
        self.srogress_sprites = import_cut_graphicks(f'map/Texture/plants/{type}/progress.png', (TILE_SIZE, TILE_SIZE))
        self.max_progress = len(self.srogress_sprites) -1
        self.progress_index = 0
        super().__init__(groups = groups, image = self.srogress_sprites[self.progress_index], hitbox_offset = hitbox_offset, z = z, special_flag = special_flag, **pos)
        self.crop_id = get_crop_id(type)
    
    def update(self):
        if randrange(1000): return
        self.progress_index = min(self.max_progress, self.progress_index + 1)
        self.image = self.srogress_sprites[self.progress_index]
        self.rect = self.image.get_rect(topleft = self.rect.topleft)
        self.hitbox = self.rect.copy()
    
    def grown(self):
        return self.progress_index // self.max_progress
    
    def harvest(self, game):
        game.player.inventory.add_item(self.crop_id, randrange(1, 3))
        self.kill()