import pygame
from item import *
from support import *

class Inventory:
    def __init__(self, player) -> None:
        self.player = player
        self.size = 8
        self.space = []
        self.all_items = {}
        self.add_item(0, 1)
        self.add_item(3, 1)
        self.add_item(5, 1)
        self.add_item(1, 10)
        self.cell_index = 0
        self.open = False
        self.sprite = InventorySprite(self)
    
    def add_item(self, id, quantity):
        thinks_left = quantity
        for item in self.space:
            if item.id == id:
                added_thinks = min(item.max_stack - item.quantity, thinks_left)
                item.quantity += added_thinks
                thinks_left -= added_thinks
        
        if len(self.space) >= self.size: return

        max_stack = items[id]['max_stack']
        n = thinks_left // max_stack

        if not thinks_left: return

        for i in range(n):
            if len(self.space) >= self.size: return
            self.space.append(impoer_item(id, max_stack))
            thinks_left -= max_stack
        
        if not thinks_left: return

        self.space.append(impoer_item(id, thinks_left))

    def remove_item(self, id, quantity):
        #{item1_id: item1_quantity}
        thinks_left = quantity
        for item in self.space:
            if item.id == id:
                removed_thinks = min(item.quantity, thinks_left)
                item.quantity -= removed_thinks
                thinks_left -= removed_thinks
        self.kill_items()

    def turn_left(self):
        self.cell_index = max(0, self.cell_index - 1)
    
    def turl_right(self):
        self.cell_index = min(self.size, self.cell_index + 1)
    
    def current_item(self):
        if self.cell_index < len(self.space): return self.space[self.cell_index]
        else: return None
    
    def get_number_of_all_item(self):
        all_items = {}
        for item in self.space:
            should_i_make_a_new_col = True
            for item_id in all_items.keys():
                if item.id == item_id:
                    all_items[item_id] += item.quantity
                    should_i_make_a_new_col = False
            
            if should_i_make_a_new_col:
                all_items[item.id] = item.quantity
            
        return all_items
        
    def kill_items(self):
        for item in self.space:
            if item.should_kill():
                self.space.remove(item)
                self.player.current_item = self.current_item()
            
    def update(self):
        self.kill_items()
        
class InventorySprite:
    def __init__(self, inventory: Inventory) -> None:
        self.inventory = inventory
        self.cell = import_graphics('map/Texture/inventory.png')
        self.pointer = import_graphics('map/Texture/inventory_pointer.png')
        self.cell.set_alpha(200)
        self.pointer.set_alpha(200)
        self.width, self.height = self.cell.get_size()
        self.font = pygame.font.Font(None, 20)
    
    def render(self, screen: pygame.Surface):
        for i in range(self.inventory.size):
            pos = pygame.Vector2(50 + i * (10 + self.width), 50)
            if  i == self.inventory.cell_index: screen.blit(self.pointer, pos)
            else: screen.blit(self.cell, pos)

        for item_index, item in enumerate(self.inventory.space):
            pos = pygame.Vector2(50 + item_index * (10 + self.width), 50)
            item.render(screen, pos, self.font)

