import pygame


class InventoryImage(pygame.sprite.Sprite):
    def __init__(self, name,x,y,count):
        super(InventoryImage, self).__init__()
        self.name = name
        self.x=x
        self.y=y
        self.image = pygame.image.load('../assets/Terrain/' + self.name)
        self.image=pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x+12, self.y+12)  # Установить начальное положение спрайта
        self.dragging = False
        self.font = pygame.font.Font(None, 36)
        self.count=count
        self.moving = False

    def update(self):
        if self.moving:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.rect.center = (mouse_x, mouse_y)

    def draw(self, window):
        window.blit(self.image, self.rect)
        text_surface = self.font.render(str(self.count), True, (255,255,255))  # Черный цвет текста
        text_rect = text_surface.get_rect(
            topleft=(self.rect.right-5, self.rect.centery - text_surface.get_height() // 2+10))
        window.blit(text_surface, text_rect)