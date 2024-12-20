from os import listdir
from os.path import isfile, join
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


class CurrentInventory:
    def __init__(self):
        self.image = pygame.image.load("assets/images/inventory_tile.png")
        self.image = pygame.transform.scale(self.image, (Settings.CELL_SIZE, Settings.CELL_SIZE))
        self.select = pygame.image.load("assets/images/selected_item.png")
        self.select = pygame.transform.scale(self.select, (Settings.CELL_SIZE+7, Settings.CELL_SIZE+7))
        self.inventory_size = 9
        self.cell_size = settings.CELL_SIZE + 3
        self.position = (0, settings.HEIGHT - self.cell_size)
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen, selected_item, current_inx):
        for i in range(self.inventory_size):
            x = self.position[0] + (i * self.cell_size) + (
                    settings.WIDTH - settings.CELL_SIZE * self.inventory_size) // 2
            y = self.position[1] - 20
            screen.blit(self.image, (x, y))
            screen.blit(self.select, self.get_select_coord(selected_item))
        for item_name in current_inx:
            block = get_drop_block(item_name)
            numb = list(current_inx).index(item_name)
            block_position = self.get_current_block(numb)
            screen.blit(block, block_position)
            if(current_inx[item_name]>1):
                text_surface = self.font.render(str(current_inx[item_name]), True, (255, 255, 255))
                text_position = (block_position[0] + 40, block_position[1] + 30)  # Смещение для текста
                screen.blit(text_surface, text_position)

    def get_select_coord(self,number):
        y=self.position[1] - 25
        x=self.position[0]+((number-1) * self.cell_size)+(settings.WIDTH - settings.CELL_SIZE * self.inventory_size) // 2-2
        return (x,y)
    def get_current_block(self,number):
        y = self.position[1] - 7
        x = self.position[0] + ((number - 1) * self.cell_size) + (
                    settings.WIDTH - settings.CELL_SIZE * self.inventory_size) // 2+92
        return (x, y)
