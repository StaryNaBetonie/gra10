import pygame
from support import *
from settings import *

def impoer_item(id, quantity):
    item_data = items[id]
    item_type = item_data['item type']
    if item_type is ItemType.Hoe:
        item = Hoe(item_data, quantity)
    elif item_type is ItemType.Seeds:
        item = Seeds(item_data, quantity)
    elif item_type is ItemType.Sickle:
        item = Sickle(item_data, quantity)
    elif item_type is ItemType.Material:
        item = Item(item_data, quantity)
    elif item_type is ItemType.Axe:
        item = Axe(item_data, quantity)
    return item

class Item:
    def __init__(self, item_data, quantity) -> None:
        self.id = item_data['id']

        self.item_type = item_data['item type']

        self.quantity = quantity
        self.max_stack = item_data['max_stack']

        self.sprite = ItemSprite(self)

    def use(self, point, game):
        pass

    def should_kill(self):
        if self.quantity > 0: return False
        else: return True
    
    def render(self, screen: pygame.Surface, pos, font: pygame.font.Font):
        self.sprite.render(screen, pos, font)
    
    def usage_interaction(self):
        self.quantity -= 1

class Tool(Item):
    def __init__(self, item_data, quantity) -> None:
        super().__init__(item_data, quantity)
        self.max_durability = item_data['durability']
        self.durability = self.max_durability
    
    def should_kill(self):
        if super().should_kill(): return super().should_kill()
        if self.durability > 0: return False
        else: return True
    
    def usage_interaction(self):
        self.durability -= 1
    
    def render(self, screen: pygame.Surface, pos, font: pygame.font.Font):
        super().render(screen, pos, font)

        durability_offset = pygame.Vector2(TILE_SIZE * 0.125, TILE_SIZE - 10)
        muliplyer = self.durability / self.max_durability
        durability_rect = pygame.Rect(pos + durability_offset, (TILE_SIZE * 0.75 * muliplyer, 5))

        color = 'green'
        if muliplyer <= 0.5: color = 'orange'
        if muliplyer <= 0.2: color = 'red'

        pygame.draw.rect(screen, color, durability_rect)
    
class Hoe(Tool):
    def use(self, point, game):
        game.ground.add_soil(point, game)

class Sickle(Tool):
    def use(self, point, game):
        game.ground.harvest(point, game)

class Seeds(Item):
    def __init__(self, item_data, quantity) -> None:
        super().__init__(item_data, quantity)
        self.type = item_data['type']

    def use(self, point, game):
        game.ground.add_plant(point, game, self.type)

class Axe(Tool):
    def use(self, point, game):
        game.ground.chop(point, game)

class ItemSprite:
    def __init__(self, item) -> None:
        self.item = item
        self.image = import_graphics(f'map/Texture/items_sprites/{item.id}.png').convert_alpha()
        self.number_offset = pygame.Vector2(TILE_SIZE - 18, TILE_SIZE -15)
    
    def render(self, screen: pygame.Surface, pos, font: pygame.font.Font):
        screen.blit(self.image, pos)

        if self.item.quantity == 1: return
        number_image = font.render(str(self.item.quantity), False, '#ffff99')
        number_pos = pos + self.number_offset
        screen.blit(number_image, number_pos)
        
    




