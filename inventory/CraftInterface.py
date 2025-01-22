import itertools

import pygame

from inventory.InventorySlot import CraftSlot, CraftResultSlot
from main_functions.settings import Settings


class CraftInterface:
    def __init__(self):
        self.craft_slot = [CraftSlot(a[0], a[1]) for a in list(itertools.product([0, 1], [0, 1]))]
        self.result=CraftResultSlot()
        self.arrow = pygame.image.load("../assets/images/strelka.png")
        self.arrow = pygame.transform.scale(self.arrow, (Settings.CELL_SIZE, Settings.CELL_SIZE))
        self.creature= pygame.image.load("../assets/images/creature.png")
        # self.creature = pygame.transform.scale(self.creature, (Settings.CELL_SIZE, Settings.CELL_SIZE))
        self.arrow_x = Settings.WIDTH//2+155
        self.arrow_y = Settings.HEIGHT//3-20
        self.creature_x = Settings.WIDTH // 2 -3
        self.creature_y = Settings.HEIGHT // 3 - 110

    def draw(self,window,mouse):
        for slot in self.craft_slot:
            slot.draw(window,mouse)
        self.result.draw(window,mouse)
        window.blit(self.arrow,(self.arrow_x,self.arrow_y))
        window.blit(self.creature,(self.creature_x,self.creature_y))