from os import listdir
from os.path import isfile, join
import sys
import pygame

from settings import Settings

pygame.init()

pygame.display.set_caption("Platformer")

settings = Settings()


def get_drop_block(name):
    path = join("assets", "Drop", name)
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((settings.DROPPED_BLOCK_SIZE, settings.DROPPED_BLOCK_SIZE), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, settings.DROPPED_BLOCK_SIZE, settings.DROPPED_BLOCK_SIZE)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


class Slot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("assets/images/inventory_tile.png")
        self.image = pygame.transform.scale(self.image, (Settings.CELL_SIZE, Settings.CELL_SIZE))
        self.empty = True
        self.count = 0
        self.block = 0
        self.stack = False
        self.font = pygame.font.Font(None, 36)

    def completion(self, name, count):
        self.image_block = get_drop_block(name)
        self.block = name
        self.count = count
        self.empty = False

    def update(self, a):
        ret = 0
        if self.count + a <= 64:
            self.count += a
        else:
            ret = self.count + a - 64
            self.count = 64
            self.stack = True
        return ret

    def put(self):
        self.count -= 1
        if self.count == 0:
            self.empty = True
            self.block = 0
        if self.count == 63:
            self.stack = False

    def draw(self, window):
        if not self.empty:
            window.blit(self.image, (self.x, self.y))
            window.blit(self.image_block, (self.x + 13, self.y + 12))
            text_surface = self.font.render(str(self.count), True, (255, 255, 255))
            text_position = (self.x + 53, self.y + 42)
            window.blit(text_surface, text_position)

        else:
            window.blit(self.image, (self.x, self.y))


class CurrentInventor:
    def __init__(self):
        self.cell_size = settings.CELL_SIZE + 3
        self.position = (0, settings.HEIGHT - self.cell_size)
        self.slots = [Slot(self.get_slot_coord_x(i), self.get_slot_coord_y()) for i in range(10)]
        self.select = pygame.image.load("assets/images/selected_item.png")
        self.select = pygame.transform.scale(self.select, (Settings.CELL_SIZE + 7, Settings.CELL_SIZE + 7))
        self.select_index = 1
        self.blocks = [self.slots[i].block for i in range(10)]

    def update(self, current_inventory):
        cur_invent = list(current_inventory)
        for el in cur_invent:
            if el in self.blocks:
                ind = self.blocks.index(el)
                self.slots[ind].update(current_inventory[el])
            else:
                self.slots[self.first_free()].completion(el, current_inventory[el])
                self.blocks = [self.slots[i].block for i in range(10)]

    def put(self):
        if (not self.slots[self.select_index - 1].empty):
            return True
        else:
            return False

    def put_block(self):
        block=self.slots[self.select_index - 1].block
        self.slots[self.select_index - 1].put()
        return block

    def get_select_coord(self, number):
        x = self.slots[number - 1].x
        y = self.slots[number - 1].y
        return (x - 5, y - 3)

    def first_free(self):
        self.blocks=[self.slots[i].block for i in range(10)]
        return self.blocks.index(0)

    def get_slot_coord_x(self, number):
        return self.position[0] + (number * self.cell_size) + (
                settings.WIDTH - settings.CELL_SIZE * 9) // 2 + 53

    def get_slot_coord_y(self):
        return self.position[1] - 17

    def draw(self, window):
        for i in range(0, 8):
            self.slots[i].draw(window)
        window.blit(self.select, self.get_select_coord(self.select_index))

