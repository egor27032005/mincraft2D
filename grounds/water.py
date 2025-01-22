import pygame

from grounds.block import Object
from main_functions.settings import Settings
from os.path import join

pygame.init()

pygame.display.set_caption("Platformer")

settings = Settings()


def get_water_block(size, name):
    path = join("../assets", "Water", name)
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

