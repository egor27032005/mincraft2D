import pygame

from inventory.InventoryImage import InventoryImage
from inventory.inventory_screen import *
from main_functions.settings import Settings


class InternalSlot:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.under_mouse = False
        self.count = 0
        self.font = pygame.font.Font(None, 36)
        self.row = row
        self.column = column
        self.x, self.y = self.coordinates()
        self.image = pygame.image.load("../assets/images/inventary_slot.jpg")
        self.image = pygame.transform.scale(self.image, (Settings.CELL_SIZE, Settings.CELL_SIZE))
        self.rect = self.image.get_rect()
        self.image_block: InventoryImage | None = None
        self.rect.x = self.x
        self.rect.y = self.y

    def coordinates(self):
        x = Settings.CELL_SIZE * self.column + (Settings.WIDTH - Settings.CELL_SIZE * 9) // 2
        y = Settings.CELL_SIZE * self.row + 460
        if self.row == 3:
            y += 20
        return x, y

    def draw(self, window, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.under_mouse = True

            light_image = self.make_brighter(self.image)
            window.blit(light_image, (self.x, self.y))
        else:
            window.blit(self.image, (self.x, self.y))
            self.under_mouse = False

        if self.count != 0:
            self.image_block.draw(window)

    def make_brighter(self, image):
        bright_image = image.copy()
        bright_image.fill((50, 50, 50, 0), None, pygame.BLEND_RGBA_ADD)  # Добавляем цвет для осветления
        return bright_image


class InventorySlot(InternalSlot):
    def __init__(self, row, column):
        super().__init__(row, column)
        self.row = row
        self.column = column
        self.image = pygame.image.load("../assets/images/inventary_slot.jpg")
        self.image = pygame.transform.scale(self.image, (Settings.CELL_SIZE, Settings.CELL_SIZE))
        self.x, self.y = self.coordinates()
        self.image_block: InventoryImage | None = None
        self.count = 0
        self.font = pygame.font.Font(None, 36)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y
        self.under_mouse=False

    def update(self, im_bl, cou):
        self.count = cou
        self.image_block = InventoryImage(im_bl, self.x, self.y, cou)


class ArmorSlot(InternalSlot):
    def __init__(self,row, column=0):
        super().__init__(row, column)
        self.inv_sl={3:"boots.png",2:"pants.png",1:"breastplate.png",0:"helmet.png"}
        self.image = pygame.image.load("../assets/images/armor/"+self.inv_sl[self.row])
        self.image = pygame.transform.scale(self.image, (Settings.CELL_SIZE, Settings.CELL_SIZE))


    def coordinates(self):
        x = Settings.CELL_SIZE * self.column + (Settings.WIDTH - Settings.CELL_SIZE * 9) // 2
        y = Settings.CELL_SIZE * self.row+150

        return x, y

class CraftSlot(InternalSlot):
    def __init__(self,row, column):
        super().__init__(row, column)

    def coordinates(self):
        x = Settings.CELL_SIZE * self.column+Settings.WIDTH//2
        y = Settings.CELL_SIZE * self.row+Settings.HEIGHT//4+10
        return x, y

class CraftResultSlot(InternalSlot):
    def __init__(self,row=1, column=1):
        super().__init__(row, column)
    def coordinates(self):
        x = Settings.CELL_SIZE * self.column+Settings.WIDTH//2+160
        y = Settings.CELL_SIZE * self.row+Settings.HEIGHT//4+10-36
        return x, y

