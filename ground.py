import pygame
from tile import *
from random import choice
from settings import *
from support import *
from tree import Tree

class Ground:
    def __init__(self, game) -> None:
        self.grid = [[['F'] for j in range(40)] for i in range(40)]
        self.soil_sprites = pygame.sprite.Group()
        self.plant_sprites = pygame.sprite.Group()
        self.trees_sprites = []
        self.soil_graphics = self.import_soil_graphics()
        
        self.generate_map(game)
        self.add_trees(game)
    
    def add_trees(self, game):
        tree_types = ('small', 'big', 'large')

        for j in range(30):
            x, y = randrange(0, 35 * TILE_SIZE), randrange(0, 35 * TILE_SIZE)
            tree = Tree(choice(tree_types), game, (x, y))
            self.trees_sprites.append(tree)
            if not 'F' in self.grid[tree.bottom.sprite.rect.bottom // TILE_SIZE][tree.bottom.sprite.rect.centerx // TILE_SIZE]: return
            self.grid[tree.bottom.sprite.rect.bottom // TILE_SIZE][tree.bottom.sprite.rect.centerx // TILE_SIZE].remove('F')

    
    def import_soil_graphics(self):
#(top, bottop, left, right, top-left, top-right, bottop-left, bottop-right)
        graphics = {'________':None, 'X_______': None, '_X______': None, '__X_____': None, 
                    '___X____': None, 'XX______': None, 'X_X_____': None, 'X__X____': None,
                    '_XX_____': None, '_X_X____': None, '__XX____': None, '_X_X____': None,
                    'XXX_____': None, '_XXX____': None, 'X_XX____': None, 'XX_X____': None,
                    'XXXX____': None,
                    }
        path = 'map/Texture/tilesets/soil/'

        for tile in graphics.keys():
            graphics[tile] = import_graphics(f'{path}{tile}.png')
        
        return graphics 

    def generate_map(self, game):
        path = 'map/Texture/tilesets/grass.png'
        grass_graphics = import_cut_graphicks(path, (TILE_SIZE, TILE_SIZE))
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                x = col * TILE_SIZE
                y = row * TILE_SIZE
                surface = choice(grass_graphics)
                Tile(groups = game.visible_sprites, image = surface, topleft = (x, y))
    
    def add_soil(self, point, game):
        x, y = point
        col, row = x // TILE_SIZE, y //TILE_SIZE
        if 'S' in self.grid[row][col]: return
        if not 'F' in self.grid[row][col]: return
        self.grid[row][col].append('S')
        game.player.current_item.usage_interaction()
        # SoilTile(groups = [game.visible_sprites, self.soil_sprites], tileset = self.soil_graphics, topleft = (col * TILE_SIZE, row * TILE_SIZE))
        groups = [game.visible_sprites, self.soil_sprites]
        SoilTile(groups=groups, tileset=self.soil_graphics, topleft = (col * TILE_SIZE, row * TILE_SIZE))
        self.soil_sprites.update(self.grid, (col, row))
    
    def add_plant(self, point, game, type):
        x, y = point
        col, row = x // TILE_SIZE, y //TILE_SIZE
        if 'S' not in self.grid[row][col]: return
        if 'P' in self.grid[row][col]: return
        self.grid[row][col].append('P')
        game.player.current_item.usage_interaction()
        Plant(groups=[game.visible_sprites, self.plant_sprites], type=type, topleft = (col * TILE_SIZE, row * TILE_SIZE))
    
    def harvest_plant(self, col, row, game, plant):
        if not plant.hitbox.x // TILE_SIZE == col: return
        if not plant.hitbox.y // TILE_SIZE == row: return
        if not plant.grown(): return

        game.player.current_item.usage_interaction()
        plant.harvest(game)
        self.grid[row][col].remove('P')
        
    def harvest(self, point, game):
        x, y = point
        col, row = x // TILE_SIZE, y //TILE_SIZE
        for plant in self.plant_sprites.sprites():
            self.harvest_plant(col, row, game, plant)
        
    def chop_tree(self, point, game, tree):
        if not tree.interaction_hitbox.collidepoint(point): return
        print('nigger')
        game.player.current_item.usage_interaction()
        tree.chop(game)
        
    def chop(self, point, game):
        for tree in self.trees_sprites:
            self.chop_tree(point, game, tree)

    def update(self):
        self.plant_sprites.update()
        