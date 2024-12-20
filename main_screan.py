from water import *
from block import *

settings = Settings()

pygame.init()

pygame.display.set_caption("Platformer")


class Main_Screen():
    index_of_image = {11: "water_1.png",12: "water_2.png", 13: "water_3.png",14: "water_4.png",15: "water_5.png",16: "water_6.png",17: "water_7.png",18: "water_8.png",22: "dirt.png", 23: "bedrock.png", 24: "stone.png", 25: "grass.png"}

    def __init__(self, matrix):
        self.matrix = matrix
        self.x = settings.PLAYER_START_X
        self.y = settings.PLAYER_START_Y
        self.blocks = self.get_main_screen()

    def get_main_screen(self):
        blocks = []
        for x in range(self.x - 15, self.x + 15):
            for y in range(self.y - 7, self.y + 7,-1):
                if self.matrix[x, y] != 0:
                    blocks.append(self.create_block(self.matrix[x, y], x, y))
        return blocks

    def get_update_main_screen(self, new_x, new_y):
        blocks = []
        for x in range(new_x - 15, new_x + 15):
            for y in range(new_y - 7, new_y + 7):
                if self.matrix[x, y] != 0:
                    blocks.append(self.create_block(self.matrix[x, y], x, y))
        return blocks

    def update_main_screen(self, new_x, new_y):
        if abs(new_x - self.x) > 2 or abs(new_y - self.y) > 2:
            self.x, self.y = new_x, new_y
            self.blocks = self.get_update_main_screen(new_x, new_y)
        return self.blocks

    def delete_block(self):
        self.blocks=self.get_update_main_screen(self.x,self.y)
    def create_block(self, index, x, y):
        if index <20:
            block = Water(x, y, settings.BLOCK_SIZE, self.index_of_image[index])
        else:
            block = Block(x, y, settings.BLOCK_SIZE, self.index_of_image[index])
        return block
