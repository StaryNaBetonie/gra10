import pygame
from support import *
from settings import *
from display_surface import DisplaySurface

class CraftingRecipie:
    def __init__(self, data) -> None:
        #(id of crafted item, quantity of crafted item): [(id of material1, quantity of material1), (id of material2, quantity of material2) ... ])
        self.make_recipie(data)

    def make_recipie(self, data: dict):
        self.id, self.quantity = data[0]
        self.materials = data[1]
        self.number_of_craftable_items = 0
        self.sprite = CraftingRecipieSprite(self)
    
    def get_number_of_craftable_items(self, player_items: dict):
        your_materials = []
        for material_id, material_quantity in self.materials:
            if not material_id in list(player_items.keys()):
                your_materials.append(0)
            else:
                number = player_items[material_id] // material_quantity
                your_materials.append(number)
        number_to_return = min(your_materials)
        self.number_of_craftable_items = number_to_return
        return number_to_return
    
    def render(self, display, font, pos):
        self.sprite.render(display, font, pos)
    
    def render_recipe(self, display, font):
        self.sprite.render_recipe(display, font)

class CraftingRecipieSprite:
    def __init__(self, crafting_recipie: CraftingRecipie) -> None:
        self.crafting_recipie = crafting_recipie
        self.recipe_display = DisplaySurface((WINDOW_WIDTH * 0.3 - TILE_SIZE - 40, WINDOW_HEIGHT * 0.4 - TILE_SIZE - 40), topleft = (0, 0))
        self.import_graphics()
    
    def import_graphics(self):
        self.cell = import_graphics('map/Texture/inventory.png')
        path = 'map/Texture/items_sprites/'
        self.item_image = import_graphics(f'{path}{self.crafting_recipie.id}.png')

        self.material_graphics = {}
        for material_id, _ in self.crafting_recipie.materials:
            self.material_graphics[material_id] = import_graphics(f'{path}{material_id}.png')
    
    def render(self, display: pygame.Surface, font: pygame.font.Font, pos):
        display.blit(self.item_image, pos)

        if self.crafting_recipie.quantity == 1: return

        text_image = font.render(str(self.crafting_recipie.quantity), False, 'white')
        offset = pygame.Vector2(TILE_SIZE - 21, TILE_SIZE - 18)
        display.blit(text_image, pos + offset)
    
    def render_recipe(self, display: DisplaySurface, font: pygame.font.Font):
        self.recipe_display.clear()
        self.recipe_display.rect.bottomright = display.get_size()

        for index, material_data in enumerate(self.crafting_recipie.materials):
            material_id, material_quantity = material_data
            pos = pygame.Vector2(100 + index * (TILE_SIZE + 10), 20)
            self.recipe_display.surface.blit(self.cell, pos)
            material_image = self.material_graphics[material_id]
            self.recipe_display.surface.blit(material_image, pos)

            if not material_quantity == 1:
                text_image = font.render(str(material_quantity), False, 'white')
                offset = pygame.Vector2(TILE_SIZE - 21, TILE_SIZE - 18)
                self.recipe_display.surface.blit(text_image, pos + offset)
        
        display.surface.blit(self.recipe_display.surface, self.recipe_display.rect)


