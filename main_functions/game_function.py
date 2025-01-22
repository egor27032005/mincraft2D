import pygame as pg

from main_functions.game import Game
from stats import Stats

class GameFunctions:
    def __init__(self, window):
        self.screen = window
        self.stats = Stats()
        self.game = Game(window, self.stats)

    def check_events(self):
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    exit()
                case pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE and self.stats.game_state == 1:
                        exit()
            self.game.check_event(event)

    def update_screen(self):
        self.game.update()
        self.game.draw()
