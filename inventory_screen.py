import pygame

from settings import Settings

settings = Settings()


class InventorySlot:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.image = pygame.image.load("assets/images/inventary_slot.jpg")
        self.image = pygame.transform.scale(self.image, (Settings.CELL_SIZE, Settings.CELL_SIZE))
        self.x, self.y = self.coordinates()
        self.image_block=0
        self.count=0
        self.font = pygame.font.Font(None, 36)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

    def coordinates(self):
        x = settings.CELL_SIZE * self.column + (settings.WIDTH - settings.CELL_SIZE * 9) // 2
        y = settings.CELL_SIZE * self.row + 460
        if self.row == 3:
            y += 20
        return x, y
    def update(self,im_bl,cou):
        self.count=cou
        self.image_block=im_bl

    def draw(self, window):
        if self.count!=0:
            window.blit(self.image, (self.x, self.y))
            window.blit(self.image_block, (self.x + 13, self.y + 12))
            text_surface = self.font.render(str(self.count), True, (255, 255, 255))
            text_position = (self.x + 53, self.y + 42)
            window.blit(text_surface, text_position)

        else:
            window.blit(self.image, (self.x, self.y))


class InventoryScreen:
    def __init__(self, window, drop):
        self.drop=drop
        self.window = window
        self.rows = 3
        self.columns = 9
        self.create_slots()

    def create_slots(self):
        self.slots = [[InventorySlot(i, j) for i in range(3)] for j in range(9)]
        self.my_slots = [InventorySlot(3, j) for j in range(9)]
    def update_slots(self):
        for i in range(9):
            self.my_slots[i].update(self.drop.my_drop[i][0],self.drop.my_drop[i][1])

    def check_event(self, event):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                for item in self.my_slots:
                    if item.rect.collidepoint(*event.pos):
                        item.is_dragging = True
                        for tile in self.my_slots + self.slots:
                            if tile.value == item:
                                tile.value = None
            case pygame.MOUSEBUTTONUP:
                for item in self.items:
                    if item.is_dragging:
                        for tile in self.slots + self.my_slots:
                            self.check_collide(tile, item)
    def check_collide(self, tile, item):
        if tile.rect.collidepoint(*pygame.mouse.get_pos()):
            if tile.count==0:
                item.is_dragging = False
                item.rect.x = tile.rect.x + 22
                item.rect.y = tile.rect.y + 22
                tile.value = item
    def update(self):
        return 1

    def draw(self):
        # self.update_slots()
        self.window.fill((198, 198, 198))
        for slot in sum(self.slots, []):
            slot.draw(self.window)
        for slot in self.my_slots:
            slot.draw(self.window)

        pygame.display.flip()

