import pygame
from tile import *

class Tree:
    def __init__(self, name, game, pos) -> None:
        self.top = pygame.sprite.GroupSingle()
        self.bottom = pygame.sprite.GroupSingle()
        self.shadow = pygame.sprite.GroupSingle()
        self.generate_tree(name, game, pos)
        self.interaction_hitbox = pygame.Rect((self.get_bottom().hitbox.left - 3, self.get_bottom().rect.top), (self.get_bottom().hitbox.width + 10, self.get_bottom().rect.height))
        # Tile(game.visible_sprites, self.interaction_hitbox.topleft, get_surface(self.interaction_hitbox.size, 'blue'), z=layers['tree'])
        self.hp = 5
        self.wood_id = 4
    
    def get_bottom(self) -> Tile:
        return self.bottom.sprite
    
    def get_top(self) -> Tile:
        return self.top.sprite
    
    def generate_tree(self, name: pygame.Surface, game, pos):
        path = f'map/Texture/tilesets/trees/{name}/'
        image = import_graphics(f'{path}tree.png')
        shadow_image = import_graphics(f'{path}shadow.png')
        width, height = image.get_size()
        x, y = pos

        top_image = pygame.Surface((width, height * 0.8), flags = pygame.SRCALPHA)
        image_rect = image.get_rect(topleft = (0, 0))
        top_image.blit(image, image_rect)
        groups = [game.visible_sprites, self.top]
        Tile(groups = groups, image = top_image, z = layers['tree'], topleft = (x, y))

        bottom_image = pygame.Surface((width, height * 0.2), flags = pygame.SRCALPHA)
        image_rect.bottom = bottom_image.get_height()
        bottom_image.blit(image, image_rect)
        groups = [game.visible_sprites, game.obsticle_sprites, self.bottom]
        Tile(groups = groups, z = layers['player'], topleft = (x, y + top_image.get_height()), image = bottom_image, hitbox_offset=(0.95, 0.8))

        # Tile(groups=game.visible_sprites, pos=self.get_bottom().hitbox.topleft, image=get_surface(self.get_bottom().hitbox.size, 'blue'), z=layers['tree'])
        groups = [game.visible_sprites, self.shadow]
        Tile(groups=groups, image=shadow_image, z=layers['shadow'], special_flag=pygame.BLEND_RGBA_MULT, center = (self.get_top().rect.centerx, self.get_bottom().rect.centery - 20))
    
    def kill(self, game):
        col, row = self.get_bottom().rect.bottom // TILE_SIZE, self.get_bottom().rect.centerx // TILE_SIZE
        game.ground.grid[col][row].append('F')
        tab = game.ground.trees_sprites
        self.bottom.sprite.kill()
        self.top.sprite.kill()
        self.shadow.sprite.kill()
        tab.remove(self)
    
    def chop(self, game):
        self.hp -= 1
        if self.hp > 0: return
        game.player.inventory.add_item(self.wood_id, randrange(3, 5))
        self.kill(game)
