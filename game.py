from current_inventory import Drop
from inventory_screen import InventoryScreen
from main_screan import Main_Screen
import pygame as pg

class Game:
    def __init__(self, window, stats):
        self.window=window
        self.stats=stats
        self.drop=Drop()
        self.inventory_screen = InventoryScreen(window,self.drop)
        self.main_screen = Main_Screen(window,self.drop)

    def check_event(self, event):
        match self.stats.game_state:
            case 1:
                self.main_screen.check_event(event)
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_e:
                        self.inventory_screen.update_slots()
                        self.stats.game_state = 2
            case 2:
                # self.inventory_screen.check_event(event)
                if event.type == pg.MOUSEBUTTONDOWN:
                    pass
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_e:
                        self.stats.game_state = 1


    def update(self):
        match self.stats.game_state:
            case 1:
                self.main_screen.update()
            case 2:
                self.inventory_screen.update()
    def draw(self):
        match self.stats.game_state:
            case 1:
                self.main_screen.draw()
            case 2:
                self.inventory_screen.draw()