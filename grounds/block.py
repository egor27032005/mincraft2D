from os.path import join
import pygame

from main_functions.settings import Settings

pygame.init()

pygame.display.set_caption("Platformer")

settings = Settings()


def get_block(name):
    path = join("../assets", "Terrain", name)
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((settings.BLOCK_SIZE, settings.BLOCK_SIZE), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, settings.BLOCK_SIZE, settings.BLOCK_SIZE)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

class Object(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name
        self.x=x
        self.y=y


    def draw(self, win, offset_x, offset_y):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))


class Block(Object):
    blocks = {"bedrock.png": 1, "turf.png": 0.3, "stone.png": 0.6, "grass.png": 0.3, "dirt.png": 0.4}
    def __init__(self, x, y, size, name):
        self.name = name
        super().__init__(x*settings.BLOCK_SIZE, y*settings.BLOCK_SIZE, size, size)
        block = get_block(name)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.hardness = self.blocks[name]
        self.x = x
        self.y = y
        self.name=name

