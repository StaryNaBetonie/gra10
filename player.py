import pygame
from tile import Tile
from support import *
from item import *
from inventory import Inventory
from settings import *

class Player(Tile):
    def __init__(self, groups, pos, z) -> None:
        self.frame_index = 0
        self.animation_speed = 0.07
        self.graphics = self.import_graphics()
        self.status = 'right'

        super().__init__(groups = groups, image = self.graphics[self.status][self.frame_index], hitbox_offset=(0.2, 0.6), z = z, topleft = pos)
        self.direction = pygame.Vector2()
        self.speed = 5

        self.inventory = Inventory(self)
        self.current_item = self.inventory.current_item()
        self.target_point_offset = (48, 16)
    
    def import_graphics(self):
        path = 'map/Texture/player/'
        space = {'up': [], 'down': [], 'left': [], 'right': [],
                'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': []}
        for key in space.keys():
            space[key] = import_cut_graphicks(f'{path}{key}.png', (56, 64))
        return space
    
    def set_status(self):
        if self.direction.magnitude(): return
        self.status = self.status.split('_')[0] + '_idle'

    def get_direction(self, events: dict):
        if self.direction.y == 0:
            if events['a'] is True:
                self.target_point_offset = (-48, 16)
                self.direction.x = -1
                self.status = 'left'
            elif events['d'] is True:
                self.target_point_offset = (48, 16)
                self.direction.x = 1
                self.status = 'right'
            else: self.direction.x = 0

        if self.direction.x == 0:
            if events['w'] is True:
                self.target_point_offset = (0, -48)
                self.direction.y = -1
                self.status = 'up'
            elif events['s'] is True:
                self.target_point_offset = (0, 48)
                self.direction.y = 1
                self.status = 'down'
            else: self.direction.y = 0

        self.set_status()

    def move(self, game):
        if self.direction.magnitude() != 0: self.direction.normalize()
        self.hitbox.x += self.direction.x * self.speed
        self.hitbox.y += self.direction.y * self.speed
        self.collision(game)
        self.rect.center = self.hitbox.center
    
    def use_item(self, game):
        if self.current_item is None: return
        x_offset, y_offset = self.target_point_offset
        target_point = (self.hitbox.centerx + x_offset, self.hitbox.centery + y_offset)
        self.current_item.use(target_point, game)
    
    def change_item(self, direction):
        if direction:
            self.inventory.turn_left()
        else:
            self.inventory.turl_right()
        self.current_item = self.inventory.current_item()
    
    def render(self, screen: pygame.Surface):
        x, y = screen.get_size()
        pygame.draw.circle(screen, 'black', (x // 2 + self.target_point_offset[0], y // 2 + self.target_point_offset[1]), 3)
    
    def collision(self, game):
        collision_objects = game.obsticle_sprites.sprites()
        for tile in collision_objects:
            if self.hitbox.colliderect(tile.hitbox):
                if self.direction.x > 0:
                    self.hitbox.right = tile.hitbox.left
                elif self.direction.x < 0:
                    self.hitbox.left = tile.hitbox.right
                elif self.direction.y < 0:
                    self.hitbox.top = tile.hitbox.bottom
                elif self.direction.y > 0:
                    self.hitbox.bottom = tile.hitbox.top
    
    def update(self, game):
        self.animate()
        self.get_direction(game.events)
        self.inventory.update()
        self.move(game)
    
    def animate(self):
        self.frame_index += self.animation_speed
        self.frame_index %= len(self.graphics[self.status])
        self.image = self.graphics[self.status][int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
