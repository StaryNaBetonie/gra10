import pygame
from settings import *
from support import *
from player import Player
from crafting_recipie import CraftingRecipie
from display_surface import DisplaySurface

class Crafting:
    def __init__(self, player: Player) -> None:
        self.sprite = CraftingSprite(self)
        self.player = player
        self.start()

    def start(self):
        self.number_of_items = 1
        self.pointer_index = 0
        self.available_craftings = self.get_available_craftings()

    def go_up(self):
        if len(self.available_craftings) == 0: return
        self.number_of_items = min(self.available_craftings[self.pointer_index].number_of_craftable_items, self.number_of_items + 1)
    
    def go_down(self):
        self.number_of_items = max(1, self.number_of_items - 1) 
    
    def turn_left(self):
        self.number_of_items = 1
        self.pointer_index = max(0, self.pointer_index - 1)
    
    def turn_right(self):
        self.number_of_items = 1
        size = len(self.available_craftings) - 1
        self.pointer_index = min(size, self.pointer_index + 1)
    
    def get_available_craftings(self):
        available_craftings = []
        player_items = self.player.inventory.get_number_of_all_item()
        for data in list(crafting_recipies.items()):
            recipie = CraftingRecipie(data)
            if not recipie.get_number_of_craftable_items(player_items) == 0:
                available_craftings.append(recipie)
        return available_craftings
    
    def craft(self):
        if len(self.available_craftings) == 0: return
        item_to_craft = self.available_craftings[self.pointer_index]
        for material_id, material_quantity in item_to_craft.materials:
            self.player.inventory.remove_item(material_id, material_quantity * self.number_of_items)
        self.player.inventory.add_item(item_to_craft.id, item_to_craft.quantity * self.number_of_items)
        self.start()

    def render(self, window):
        self.sprite.render(window)

class CraftingSprite:
    def __init__(self, crafting: Crafting) -> None:
        self.crafting = crafting

        self.background = pygame.Surface(WINDOW_SIZE)
        self.background.set_alpha(150)

        self.display = DisplaySurface((WINDOW_WIDTH * 0.3, WINDOW_HEIGHT * 0.4), center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        self.crafting_space = DisplaySurface(self.display.get_size(), center = self.display.rect.center)
        self.crafting_space.fill('#375bff')
        self.crafting_space.set_alpha(200)


        self.pointer = import_graphics('map/Texture/inventory_pointer.png')
        self.cell = import_graphics('map/Texture/inventory.png')
        self.cell_rect = self.cell.get_rect(topleft = (20, self.display.get_height() // 2))

        self.font1 = pygame.font.Font(None, 64)
        self.font2 = pygame.font.Font(None, 25)
    
    def render(self, screen: pygame.Surface):
        self.display.clear()
        screen.blit(self.background, (0, 0))
        screen.blit(self.crafting_space.surface, self.crafting_space.rect)

        for i, crafting_recipie in enumerate(self.crafting.available_craftings):
            pos = pygame.Vector2(20 + (TILE_SIZE + 10) * i, 20)
            if self.crafting.pointer_index == i:
                self.display.surface.blit(self.pointer, pos)
            crafting_recipie.render(self.display.surface, self.font2, pos)

        if not len(self.crafting.available_craftings) == 0:
            text_image = self.font1.render(str(self.crafting.number_of_items), False, 'white')
            text_rect = text_image.get_rect(center = self.cell_rect.center)
            self.display.surface.blit(self.cell, self.cell_rect)
            self.display.surface.blit(text_image, text_rect)
            self.crafting.available_craftings[self.crafting.pointer_index].render_recipe(self.display, self.font2)

        screen.blit(self.display.surface, self.display.rect)