import math
import time

import pygame

from block import Object
from settings import Settings
from os import listdir
from os.path import isfile, join

pygame.init()

pygame.display.set_caption("Platformer")

settings = Settings()


def get_water_block(size, name):
    path = join("assets", "Water", name)
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

class Water(Object):
    def __init__(self, x, y, size, name):
        self.name = name
        super().__init__(x * settings.BLOCK_SIZE, y * settings.BLOCK_SIZE, size, size)
        block = get_water_block(size, name)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.x = x
        self.y = y
        self.name = name

    # def draw(self, win, offset_x, offset_y):
    #     win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))



def water_player(x, y, waters, objects):
    nearest_water = [water for water in waters if abs(water.x - x) + abs(water.y - y) < 20]
    nearest_blocks = [block for block in objects if abs(block.x - x) + abs(block.y - y) < 25]
    for water in nearest_water:
        now_y = water.y
        now_x = water.x
        water_ander = [water.y for water in nearest_water if water.x == now_x]
        block_ander = [block.y for block in nearest_blocks if block.x == now_x]
        if (now_y + 1 not in water_ander and now_y + 1 not in block_ander):
            waters.append(Water(water.x, now_y + 1, settings.BLOCK_SIZE, "water_1.png"))
    return waters


def water_near_player(x, y, objects):
    near_objects = [object for object in objects if ((object.x ** 2 - x ** 2) + (object.y ** 2 - y ** 2)) < 40]
    return near_objects
