import pygame
import pygame as pg

from main_functions.settings import Settings

settings = Settings()


class Cursor():
    def __init__(self, x, y, time, player, matrix):
        self.rect = pygame.Rect(x * settings.BLOCK_SIZE, y * settings.BLOCK_SIZE, settings.BLOCK_SIZE,
                                settings.BLOCK_SIZE)
        self.image = pygame.Surface((settings.BLOCK_SIZE, settings.BLOCK_SIZE), pygame.SRCALPHA)
        self.x = x
        self.y = y
        self.images = []
        for i in range(0, 11):
            self.images.append(pg.image.load(f'../assets/images/cursor/{i}.PNG'))
        self.time = time // 100
        self.player = player
        self.x_coord, self.y_coord = self.case_switch()
        self.matrix = matrix

    def case_switch(self):
        y = self.player.y_coord + 4 - self.y -2*self.player.y_shift
        x= self.player.x_coord - 7 + self.x
        return x, y

    def draw(self, win, offset_x, offset_y):
        win.blit(self.images[self.time % 11], (self.rect.x - offset_x % settings.BLOCK_SIZE+settings.BLOCK_SIZE, self.rect.y - offset_y % settings.BLOCK_SIZE+settings.BLOCK_SIZE))