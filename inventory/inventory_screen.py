import itertools
import math

import pygame

from inventory.CraftInterface import CraftInterface
from inventory.InventorySlot import *
from main_functions.settings import Settings

settings = Settings()

import pygame



class InventoryScreen:
    def __init__(self, window, drop):
        self.drop = drop
        self.window = window
        self.rows = 3
        self.columns = 9
        self.create_slots()
        self.all_sprites = pygame.sprite.Group()
        self.coordinates()
        self.cur_slot: None | InventorySlot =None
        self.armor_sl=[ArmorSlot(i,0) for i in range(4)]
        self.player_fon = pygame.image.load("../assets/images/playerFon.png")
        self.player_fon = pygame.transform.scale(self.player_fon, (225, 300))
        self.interface=CraftInterface()



    def create_slots(self):
        self.slots = sum([[InventorySlot(i, j) for i in range(3)] for j in range(9)],[])
        self.my_slots = [InventorySlot(3, j) for j in range(9)]

    def coordinates(self):
        self.coordinats=[]
        for slot in self.my_slots:
            self.coordinats.append((slot.x+38,slot.y+38))
        for slot in self.slots:
            self.coordinats.append((slot.x+38,slot.y+38))

    def update_slots(self):
        for i in range(9):
            if self.drop.my_drop[i][1] != 0:
                self.my_slots[i].update(self.drop.my_drop[i][0], self.drop.my_drop[i][1])
        for sl in self.my_slots:
            if sl.count!=0:
                self.all_sprites.add(sl.image_block)


    def check_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                for sprite in self.all_sprites:
                    if sprite.rect.collidepoint(event.pos):
                        sprite.moving = not sprite.moving
                        if self.current_slot()!=None:
                            sprite.rect.x=self.current_slot()[0]+13
                            sprite.rect.y=self.current_slot()[1]+13
                            # self.cur_slot.update(sprite.name,sprite.count)
                            # self.all_sprites.add(self.cur_slot.image_block)
                        else:
                            sprite.moving = not sprite.moving
            elif event.button ==3:
                for sprite in self.all_sprites:
                    if sprite.moving==True and self.current_slot()!=None:
                        if sprite.count==1:
                            sprite.moving=False
                            sprite.rect.x = self.current_slot()[0] + 13
                            sprite.rect.y = self.current_slot()[1] + 13
                        else:
                            sprite.count-=1
                            self.cur_slot.update(sprite.name,1)
                            self.all_sprites.add(self.cur_slot.image_block)


        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Левая кнопка мыши
                for sprite in self.all_sprites:
                    if sprite.moving:  # Если спрайт движется
                        sprite.moving = True  # Продолжаем движение
        if event.type == pygame.MOUSEMOTION:
            self.current_slot()
        # print([slot.under_mouse for slot in itertools.chain(self.my_slots,self.slots)])


    def check_collide(self, tile, item):
        if tile.rect.collidepoint(*pygame.mouse.get_pos()):
            if tile.count == 0:
                item.is_dragging = False
                item.rect.x = tile.rect.x + 22
                item.rect.y = tile.rect.y + 22
                tile.value = item
    def current_slot(self):
        slots_mouse=[slot.under_mouse for slot in itertools.chain(self.my_slots,self.slots)]
        slots=[slot for slot in itertools.chain(self.my_slots,self.slots)]
        try:
            index = slots_mouse.index(True)
        except ValueError:
            self.cur_slot=None
            return None
        else:
            self.cur_slot=slots[index]
            if index>8:
                return (self.slots[index-9].x,self.slots[index-9].y)
            else:
                return (self.my_slots[index].x,self.my_slots[index].y)

    def find_nearest_point(self,rect):
        nearest_point = None
        min_distance = float('inf')

        for point in self.coordinats:
            distance = math.sqrt((rect.centerx - point[0]) ** 2 + (rect.centery - point[1]) ** 2)
            if distance < min_distance:
                min_distance = distance
                nearest_point = point

        return nearest_point


    def update(self):
        self.all_sprites.update()

    def draw(self):
        # self.update_slots()
        self.window.fill((198, 198, 198))
        self.window.blit(self.player_fon, (340, 150))
        mouse=pygame.mouse.get_pos()
        self.interface.draw(self.window, mouse)
        for slot in self.slots:
            slot.draw(self.window,mouse)
        for sl in self.armor_sl:
            sl.draw(self.window,mouse)
        for slot in self.my_slots[::-1]:
            slot.draw(self.window,mouse)

        pygame.display.flip()
