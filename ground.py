import random
from block import Block, settings
from ground_matrix import *
from Perlin import *


class Ground:
    def __init__(self):
        self.first = [22, 11, 22, 22]
        self.block_size = settings.BLOCK_SIZE
        self.matrix = Ground_Matrix(settings.WIDTH_BLOCKS, settings.HEIGHT_BLOCKS)
        self.blocks = []

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
            for _ in range(4, 20):
                self.matrix[x - settings.WIDTH_BLOCKS // 2, settings.HEIGHT_BLOCKS - _] = 24
        self.landscaping()
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
    def tran(self):
        blocks = self.zoom(self.add_Island(self.zoom(self.first)))
        for i in range(3):
            blocks = self.add_Island(blocks)
        blocks = self.remove_much_ocean(blocks)
        blocks = self.add_Island(self.remove_much_ocean(self.zoom(self.zoom(blocks))))
        blocks = self.remove_much_ocean(self.remove_much_ocean(blocks))
        for i in range(6):
            blocks = self.zoom(blocks)
        return blocks
    def cheng80(self, num):
        if random.random() < 0.7:
            return 22 if num == 11 else 11
        else:
            return num

    def landscaping(self):
        for x in range(settings.WIDTH_BLOCKS):
            for y in range(settings.HEIGHT_BLOCKS - 1, settings.HEIGHT_BLOCKS // 2, -1):
                if self.matrix[x - settings.WIDTH_BLOCKS // 2, y] == 22 and self.matrix[
                    x - settings.WIDTH_BLOCKS // 2, y - 1] == 0:
                    self.matrix[x - settings.WIDTH_BLOCKS // 2, y] = 25

    def zoom(self, first):
        second = first.copy()
        [second.insert(2 * i + 1, first[i]) for i in range(len(first))]
        return second

    def cheng(self, num):
        if random.random() < 0.5:
            return 22 if num == 11 else 11
        else:
            return num


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
            if blocks[i - 1] == 11 and blocks[i + 1] == 11 and blocks[i] == 11:
                blocks[i] = self.cheng80(blocks[i])
        return blocks

