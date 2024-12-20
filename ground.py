import random
from block import Block, settings
from ground_matrix import *
import numpy


class Ground:
    def __init__(self):
        self.first = [22, 11, 22, 11]
        self.block_size = settings.BLOCK_SIZE
        self.matrix = Ground_Matrix(settings.WIDTH_BLOCKS, settings.HEIGHT_BLOCKS)
        self.blocks = []

    def tran(self):
        blocks = self.zoom(self.add_Island(self.zoom(self.first)))
        for i in range(3):
            blocks = self.add_Island(blocks)
        blocks = self.remove_much_ocean(blocks)
        blocks = self.add_Island(self.remove_much_ocean(self.zoom(self.zoom(blocks))))
        for i in range(6):
            blocks = self.zoom(blocks)
        return blocks

    def matrix_gro(self):
        blocks = self.tran()
        self.create_bedrock()
        for x in range(settings.WIDTH_BLOCKS):
            self.matrix[x - settings.WIDTH_BLOCKS // 2, settings.HEIGHT_BLOCKS - 20] = blocks[x]
            self.matrix[x - settings.WIDTH_BLOCKS // 2, settings.HEIGHT_BLOCKS - 21] = blocks[x]
            self.matrix[x - settings.WIDTH_BLOCKS // 2, settings.HEIGHT_BLOCKS - 22] = blocks[x]
            self.matrix[x - settings.WIDTH_BLOCKS // 2, settings.HEIGHT_BLOCKS - 23] = blocks[x]
            self.matrix[x - settings.WIDTH_BLOCKS // 2, settings.HEIGHT_BLOCKS - 24] = blocks[x]
        for x in range(settings.WIDTH_BLOCKS):
            for _ in range(4,20):
                self.matrix[x - settings.WIDTH_BLOCKS // 2, settings.HEIGHT_BLOCKS - _] = 24
                # self.matrix[x - settings.WIDTH_BLOCKS // 2, settings.HEIGHT_BLOCKS - 7] = 4
                # self.matrix[x - settings.WIDTH_BLOCKS // 2, settings.HEIGHT_BLOCKS - 6] = 4
                # self.matrix[x - settings.WIDTH_BLOCKS // 2, settings.HEIGHT_BLOCKS - 5] = 4
                # self.matrix[x - settings.WIDTH_BLOCKS // 2, settings.HEIGHT_BLOCKS - 4] = 4
        self.landscaping()
        return self.matrix

    def matrix_gro2(self):
        for x in range(settings.WIDTH_BLOCKS):
            for y in range(settings.HEIGHT_BLOCKS - 1, settings.HEIGHT_BLOCKS // 2, -1):
                self.matrix[x - settings.WIDTH_BLOCKS // 2, y] = 24
        return self.matrix

    def create_bedrock(self):
        for x in range(settings.WIDTH_BLOCKS):
            r = random.choice([2, 3])
            self.matrix[x - settings.WIDTH_BLOCKS // 2, settings.HEIGHT_BLOCKS - 1] = 23
            self.matrix[x - settings.WIDTH_BLOCKS // 2, settings.HEIGHT_BLOCKS - 2] = 23
            if r == 3:
                self.matrix[x - settings.WIDTH_BLOCKS // 2, settings.HEIGHT_BLOCKS - 3] = 23
            else:
                self.matrix[x - settings.WIDTH_BLOCKS // 2, settings.HEIGHT_BLOCKS - 3] = 24

    def landscaping(self):
        for x in range(settings.WIDTH_BLOCKS):
            for y in range(settings.HEIGHT_BLOCKS - 1, settings.HEIGHT_BLOCKS // 2, -1):
               if self.matrix[x - settings.WIDTH_BLOCKS // 2, y] ==22 and self.matrix[x - settings.WIDTH_BLOCKS // 2, y-1] ==0:
                   self.matrix[x - settings.WIDTH_BLOCKS // 2, y] = 25

    def zoom(self, first):
        second = first.copy()
        [second.insert(2 * i + 1, first[i]) for i in range(len(first))]
        return second

    def cheng(self, number):
        a = random.choice([0, 1])
        if (a == 1):
            if number == 11:
                number= 22
            else:
                number = 11
        return number

    def add_Island(self, blocks):
        if (blocks[0] == blocks[1]):
            blocks[0] = self.cheng(blocks[0])
        for i in range(1, len(blocks) - 1):
            if blocks[i - 1] == blocks[i] or blocks[i + 1] == blocks[i]:
                blocks[i] = self.cheng(blocks[i])
        if (blocks[-1] == blocks[-2]):
            blocks[-1] = self.cheng(blocks[-1])
        return blocks

    def remove_much_ocean(self, blocks):
        for i in range(1, len(blocks) - 1):
            if (blocks[i - 1] == 11 and blocks[i + 1] == 11) and blocks[i] == 22:
                blocks[i] = self.cheng(blocks[i])
        return blocks

    def get_block_by_coordinates(self, x_coord, y_coord):
        for blocks in self.blocks:
            if blocks.x == x_coord:
                if blocks.y == y_coord:
                    return blocks
        return None


if __name__ == "__main__":
    x = Ground()
    print(x.matrix_gro())
    x.matrix_gro()
