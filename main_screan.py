import pygame
import tkinter as tk
from current_inventory import *
from cursor import *
from ground import Ground
from current_screen import *
from ground_matrix import Ground_Matrix
from player import *
from water import *
from dropped_block import *

settings = Settings()

class Main_Screen:
    def __init__(self, window,drop):
        self.drop=drop
        self.window = window
        self.clock = pygame.time.Clock()
        self.background, self.bg_image = self.get_background("sky.png")
        self.ground = Ground()
        self.matr = self.ground.matrix_gro()
        self.ms = Current_Screen(self.matr)
        self.player_y_coord = self.get_coord(self.matr, settings.PLAYER_START_X)
        self.player = Player(settings.PLAYER_START_X, self.player_y_coord, 80, 80)
        self.inventory = CurrentInventor(self.drop)
        self.mouse_x = 0
        self.mouse_y = 0
        self.run = True
        self.mouse_pressed = False
        self.press_start_time = 0
        self.dropped_blocks = []
        self.collected_blocks = {}
        self.last_update_time = pygame.time.get_ticks()
        self.tk_window = None

    def get_background(self, name):
        image = pygame.image.load(join("assets", "Background", name))
        _, _, width, height = image.get_rect()
        tiles = []
        for i in range(settings.WIDTH // width + 1):
            for j in range(settings.HEIGHT // height + 1):
                pos = (i * width, j * height)
                tiles.append(pos)
        return tiles, image


    def draw(self):
        for tile in self.background:
            self.window.blit(self.bg_image, tile)
        for wat in self.water:
            wat.draw(self.window, self.offset_x, self.offset_y)
        for bl in self.blocks:
            bl.draw(self.window, self.offset_x, self.offset_y)
        # for bl in self.ms.blocks:
        #     bl.draw(self.window, self.offset_x, self.offset_y)
        for drObj in self.dropped_blocks:
            drObj.draw(self.window, self.offset_x, self.offset_y)
        self.player.draw(self.window, self.offset_x, self.offset_y)
        self.cursor.draw(self.window, self.offset_x, self.offset_y)
        self.inventory.draw(self.window)
        pygame.display.update()

    def handle_vertical_collision(self, dy):
        collided_objects = []
        for obj in self.blocks:
            if pygame.sprite.collide_mask(self.player, obj):
                if dy > 0:
                    self.player.rect.bottom = obj.rect.top
                    self.player.landed()
                elif dy < 0:
                    self.player.rect.top = obj.rect.bottom
                    self.player.hit_head()
                collided_objects.append(obj)
        return collided_objects

    def collide(self, dx):
        self.player.move(dx, 0)
        self.player.update()
        collided_object = None
        for obj in self.blocks:
            if pygame.sprite.collide_mask(self.player, obj):
                collided_object = obj
                break
        self.player.move(-dx, 0)
        self.player.update()
        return collided_object

    def handle_move(self):
        keys = pygame.key.get_pressed()
        self.player.x_vel = 0
        collide_left = self.collide(-settings.PLAYER_VEL * 2)
        collide_right = self.collide(settings.PLAYER_VEL * 2)

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not collide_left:
            self.player.move_left(settings.PLAYER_VEL)
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not collide_right:
            self.player.move_right(settings.PLAYER_VEL)

        vertical_collide = self.handle_vertical_collision(self.player.y_vel)
        to_check = [collide_left, collide_right, *vertical_collide]

    def update_drop(self):
        for dr in self.dropped_blocks:
            y = self.get_coord(self.matr, dr.x, dr.y)
            for bl in self.ms.blocks:
                if bl.x == dr.x and bl.y == y:
                    dr.update(bl)

    def block_under_cursor(self, time):
        x, y = self.conversion()
        index = self.ms.matrix[x, y]
        if index < 20:
            return 0
        if time == 12:
            self.ms.matrix[x, y] = 0
            self.ms.delete_block()
            if index > 20:
                return DroppedBlock(x, y, settings.DROPPED_BLOCK_SIZE, index)
            else:
                return 0
        else:
            return 0

    def check_block(self):
        x, y = self.conversion()
        index = self.ms.matrix[x, y]
        return index > 20

    def conversion(self):
        x = self.cursor.x_coord
        y = self.cursor.y_coord
        return x, -int(y) + settings.HEIGHT_BLOCKS

    def get_coord(self, matr, x, y=0):
        for i in range(y, settings.HEIGHT_BLOCKS):
            if matr[x, i] != 0:
                return i

    def check_collisions(self):
        for dr_block in self.dropped_blocks[:]:
            if pygame.sprite.collide_mask(self.player, dr_block):
                if dr_block.name in self.collected_blocks:
                    self.collected_blocks[dr_block.name] += 1
                else:
                    self.collected_blocks[dr_block.name] = 1
                self.dropped_blocks.remove(dr_block)
        return self.collected_blocks

    def update_inventory(self):
        self.inventory.update(self.collected_blocks)

    def put_block(self):
        index_of_image = {"dirt.png": 22, "bedrock.png": 23, "stone.png": 24, "grass.png": 25}
        x, y = self.conversion()
        ms_index = self.ms.matrix[x, y]
        if self.inventory.put() and ms_index < 20:
            self.ms.matrix[x, y] = index_of_image[self.inventory.put_block()]
            self.ms.delete_block()
    def check_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.mouse_x = event.pos[0] // settings.BLOCK_SIZE
            self.mouse_y = event.pos[1] // settings.BLOCK_SIZE
        if event.type == pygame.QUIT:
            self.run = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.player.jump_count < 2:
                self.player.jump()
            if event.key == pygame.K_ESCAPE:
                self.run = False
            if pygame.K_0 <= event.key <= pygame.K_9:
                index = event.key - pygame.K_0
                self.inventory.select_index = index

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.mouse_pressed = True
                self.press_start_time = pygame.time.get_ticks()
            elif event.button == 3:
                self.put_block()

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_pressed = False


    def update(self):
        self.clock.tick(settings.FPS)
        self.cursor = Cursor(self.mouse_x, self.mouse_y, 0, self.player, self.matr)
        objects = self.ms.update_main_screen(int(self.player.x_coord), int(self.player.y_coord))
        self.water = [x for x in objects if x.name.startswith("water")]
        self.blocks = [x for x in objects if not x.name.startswith("water")]
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time >= 1000:
            self.ms.update_water(self.player.x_coord)
            self.last_update_time = current_time

        self.player.loop(settings.FPS)
        self.handle_move()
        self.update_drop()
        self.offset_x = self.player.rect.centerx - settings.WIDTH // 2
        self.offset_y = self.player.rect.centery - settings.HEIGHT // 2
        self.check_collisions()
        self.update_inventory()
        self.collected_blocks = {}
        if self.mouse_pressed and self.check_block():
            press_duration = pygame.time.get_ticks() - self.press_start_time
            self.cursor = Cursor(self.mouse_x, self.mouse_y, press_duration, self.player, self.matr)
            bool_cursor = self.block_under_cursor(press_duration // 100)
            if bool_cursor != 0:
                self.dropped_blocks.append(bool_cursor)
        else:
            self.cursor = Cursor(self.mouse_x, self.mouse_y, 0, self.player, self.matr)
        # self.draw()

        # pygame.quit()
        # quit()

