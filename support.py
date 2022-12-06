import pygame

def get_surface(size, color):
    surface = pygame.Surface(size)
    surface.fill(color)
    return surface

def import_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale2x(surface)

def import_cut_graphicks(path, size):
    surface = import_graphics(path)
    size_x, size_y = size
    tile_num_x = int(surface.get_size()[0] // size_x)
    tile_num_y = int(surface.get_size()[1] // size_y)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * size_x
            y = row * size_y
            new_surf = pygame.Surface((size_x, size_y), flags = pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, size_x, size_y))
            cut_tiles.append(new_surf)
    return cut_tiles

def get_crop_id(type):
    if type == 'wheat':
        return 2