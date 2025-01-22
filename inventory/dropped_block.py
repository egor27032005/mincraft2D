from os.path import join
import pygame

from grounds.block import Object
from main_functions.settings import Settings

pygame.init()

pygame.display.set_caption("Platformer")

settings = Settings()


def get_drop_block(name):
    path = join("../assets", "Drop", name)
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((settings.DROPPED_BLOCK_SIZE, settings.DROPPED_BLOCK_SIZE), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, settings.DROPPED_BLOCK_SIZE, settings.DROPPED_BLOCK_SIZE)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


class DroppedBlock(Object):
    blocks = {"bedrock.png": 1, "turf.png": 0.3, "stone.png": 0.6, "grass.png": 0.3, "dirt.png": 0.4}
    index_of_image = {11: "water_1.png",12: "water_2.png", 13: "water_3.png",14: "water_4.png",15: "water_5.png",16: "water_6.png",17: "water_7.png",18: "water_8.png",22: "dirt.png", 23: "bedrock.png", 24: "stone.png", 25: "grass.png"}
    def __init__(self, x, y, size, index):
        super().__init__(x * settings.BLOCK_SIZE + 25, y * settings.BLOCK_SIZE+21, size, size)
        self.name = self.index_of_image[index]
        block = get_drop_block(str(self.name))
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.hardness = self.blocks[self.name]
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.run = True

    def update(self, block):
        if (not self.rect.colliderect(block)):
            self.velocity_y -= settings.GRAVITY_BLOCK
            self.rect.y += 5
        else:
            self.velocity_y = 0
