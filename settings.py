import pygame
from enum import Enum

class ItemType(Enum):
    Hoe = 0
    Axe = 1
    Sickle =2
    Seeds = 3
    Material = 4

class Status(Enum):
    Up = 'Up'
    Down = 'Down'
    Left = 'Left'
    Right = 'Right'

layers = {
    'ground': 1,
    'soil': 2,
    'plants': 3,
    'shadow': 4,
    'player': 5,
    'tree': 6
}

TILE_SIZE = 64
WINDOW_SIZE = (1920, 1080)
WINDOW_WIDTH, WINDOW_HEIGHT = WINDOW_SIZE

items = [
    {'id': 0, 'item type': ItemType.Hoe, 'max_stack': 1, 'durability': 20},
    {'id': 1, 'item type': ItemType.Seeds, 'max_stack': 32, 'type': 'wheat'},
    {'id': 2, 'item type': ItemType.Material, 'max_stack': 32},
    {'id': 3, 'item type': ItemType.Sickle, 'max_stack': 1, 'durability': 20},
    {'id': 4, 'item type': ItemType.Material, 'max_stack': 32},
    {'id': 5, 'item type': ItemType.Axe, 'max_stack': 1, 'durability': 20},
]

#(id of crafted item, quantity of crafted item): [(id of material1, quantity of material1), (id of material2, quantity of material2) ... ])
crafting_recipies = {
    (0, 1): [(2, 3), (4, 2)],
    (3, 1): [(2, 3), (0, 1), (4, 4)],
    (1, 2): [(2, 1)],
    (5, 1): [(2, 4), (0, 1), (4, 4)],
}