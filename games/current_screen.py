
from grounds.water import *
from grounds.block import *

settings = Settings()

pygame.init()

pygame.display.set_caption("Platformer")


class Current_Screen:
    index_of_image = {11: "water_1.png", 12: "water_2.png", 13: "water_3.png", 14: "water_4.png", 15: "water_5.png",
                      16: "water_6.png", 17: "water_7.png", 18: "water_8.png", 22: "dirt.png", 23: "bedrock.png",
                      24: "stone.png", 25: "grass.png"}

    def __init__(self, matrix):
        self.matrix = matrix
        self.x = settings.PLAYER_START_X
        self.y = settings.PLAYER_START_Y
        self.blocks = self.get_main_screen()

    def get_main_screen(self):
        blocks = []
        for x in range(self.x - 15, self.x + 15):
            for y in range(self.y - 7, self.y + 7, -1):
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
        self.blocks = self.get_update_main_screen(self.x, self.y)

    def update_water(self, x):
        water = [11, 12, 13, 14, 15, 16, 17, 18]
        full_water = [11, 12]
        drop_water = [13, 14, 15, 16, 17, 18]
        left_drop=[13,14]
        right_drop=[16,17]
        for x in range(x - 15, x + 15):
            for y in range(settings.HEIGHT_BLOCKS - 1, settings.HEIGHT_BLOCKS // 2, -1):
                if self.matrix[x, y] == 0 or self.matrix[x, y] in drop_water and (self.matrix[x, y - 1] in water):
                    self.matrix[x, y] = 12
                    self.delete_block()
                if (self.matrix[x, y - 1] > 20 or self.matrix[x, y - 1] == 0) and (self.matrix[x, y] == 12):
                    self.matrix[x, y] = 0
                    self.delete_block()
                if self.matrix[x, y] == 0 and self.matrix[x + 1, y] in full_water and self.matrix[x, y - 1] not in water:
                    self.matrix[x, y] = 13
                    self.delete_block()
                if self.matrix[x + 1, y] == 0 and self.matrix[x, y] in full_water and self.matrix[x + 1, y - 1] not in water:
                    self.matrix[x + 1, y] = 16
                    self.delete_block()
                if self.matrix[x, y] == 0 and self.matrix[x + 1, y] in full_water and self.matrix[x, y - 1] not in water:
                    self.matrix[x, y] = 13
                    self.delete_block()
                if self.matrix[x + 1, y] == 0 and self.matrix[x, y] in full_water and self.matrix[x + 1, y - 1] not in water:
                    self.matrix[x + 1, y] = 16
                    self.delete_block()
                if self.matrix[x,y] in left_drop and self.matrix[x-1,y]==0:
                    self.matrix[x-1,y]=self.matrix[x,y]+1
                if self.matrix[x,y] in right_drop and self.matrix[x+1,y]==0:
                    self.matrix[x+1,y]=self.matrix[x,y]+1


    def create_block(self, index, x, y):
        if index < 20:
            block = Water(x, y, settings.BLOCK_SIZE, self.index_of_image[index])
        else:
            block = Block(x, y, settings.BLOCK_SIZE, self.index_of_image[index])
        return block
