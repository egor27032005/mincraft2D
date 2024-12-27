from django.conf.locale import tk
from current_inventory import*
from cursor import *
from ground import Ground
from ground_matrix import Ground_Matrix
from player import *
from water import *
from main_screan import *
from dropped_block import *

settings = Settings()


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []
    for i in range(settings.WIDTH // width + 1):
        for j in range(settings.HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)
    return tiles, image

def draw(window, background, bg_image, player, blocks, water, offset_x, offset_y, cursor, dropped_blocks, inventory):
    for tile in background:
        window.blit(bg_image, tile)
    for wat in water:
        wat.draw(window, offset_x, offset_y)
    for bl in blocks:
        bl.draw(window, offset_x, offset_y)
    for drObj in dropped_blocks:
        drObj.draw(window, offset_x, offset_y)
    player.draw(window, offset_x, offset_y)
    cursor.draw(window, offset_x, offset_y)
    inventory.draw(window)
    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -settings.PLAYER_VEL * 2)
    collide_right = collide(player, objects, settings.PLAYER_VEL * 2)

    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not collide_left:
        player.move_left(settings.PLAYER_VEL)
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not collide_right:
        player.move_right(settings.PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]


def update_drop(drop, blocks, matr):
    for dr in drop:
        y = get_coord(matr, dr.x, dr.y)
        for bl in blocks:
            if bl.x == dr.x and bl.y == y:
                dr.update(bl)


def block_under_cursor(cursor, ms, time, player):
    x, y = conversion(cursor, player)
    index = ms.matrix[x, y]
    if index < 20:
        return 0
    if (time == 12):
        ms.matrix[x, y] = 0
        ms.delete_block()
        if index > 20:
            return DroppedBlock(x, y, settings.DROPPED_BLOCK_SIZE, index)
        else:
            return 0
    else:
        return 0


def check_block(cursor, ms, player):
    x, y = conversion(cursor, player)
    index = ms.matrix[x, y]
    return index > 20


def conversion(cursor, player):
    x = cursor.x_coord
    y = cursor.y_coord
    return x, -int(y) + settings.HEIGHT_BLOCKS

def get_coord(matr, x, y=0):
    for i in range(y, settings.HEIGHT_BLOCKS):
        if matr[x, i] != 0:
            return i

def check_collisions(player, dropped_blocks, collected_blocks):
    for dr_block in dropped_blocks[:]:
        if pygame.sprite.collide_mask(player, dr_block):
            if dr_block.name in collected_blocks:
                collected_blocks[dr_block.name] += 1
            else:
                collected_blocks[dr_block.name] = 1
            dropped_blocks.remove(dr_block)
    return collected_blocks
def update_inventory(inventory,collected_blocks):
    inventory.update(collected_blocks)


def put_block(cursor, ms, player,inventory):
    index_of_image = {"dirt.png": 22, "bedrock.png": 23, "stone.png": 24, "grass.png": 25}
    x, y = conversion(cursor, player)
    ms_index = ms.matrix[x, y]
    if(inventory.put() and ms_index<20):
        ms.matrix[x, y] = index_of_image[inventory.put_block()]
        ms.delete_block()


def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("sky.png")
    ground = Ground()
    matr = ground.matrix_gro()
    ms = Main_Screen(matr)
    player_y_coord = get_coord(matr, settings.PLAYER_START_X)
    player = Player(settings.PLAYER_START_X, player_y_coord, 80, 80)
    inventory = CurrentInventor()
    mouse_x = 0
    mouse_y = 0
    run = True
    mouse_pressed = False
    press_start_time = 0
    dropped_blocks = []
    collected_blocks = {}
    last_update_time = pygame.time.get_ticks()
    while run:
        clock.tick(settings.FPS)
        cursor = Cursor(mouse_x, mouse_y, 0, player, matr)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.MOUSEMOTION:
                mouse_x = event.pos[0] // settings.BLOCK_SIZE
                mouse_y = event.pos[1] // settings.BLOCK_SIZE

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
                if event.key == pygame.K_ESCAPE:
                    run = False
                if pygame.K_0 <= event.key <= pygame.K_9:
                    index = event.key - pygame.K_0
                    inventory.select_index=index

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pressed = True
                    press_start_time = pygame.time.get_ticks()
                elif event.button == 3:
                    put_block(cursor, ms, player,inventory)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_pressed = False
        objects = ms.update_main_screen(int(player.x_coord), int(player.y_coord))
        water = [x for x in objects if x.name.startswith("water")]
        blocks = [x for x in objects if not x.name.startswith("water")]
        blocks = [*blocks]
        water = [*water]
        current_time = pygame.time.get_ticks()

        if current_time - last_update_time >= 1000:
            ms.update_water(player.x_coord)
            last_update_time = current_time
        player.loop(settings.FPS)
        handle_move(player, blocks)
        update_drop(dropped_blocks, blocks, matr)
        offset_x = player.rect.centerx - settings.WIDTH // 2
        offset_y = player.rect.centery - settings.HEIGHT // 2
        check_collisions(player, dropped_blocks, collected_blocks)
        update_inventory(inventory, collected_blocks)
        collected_blocks={}
        if mouse_pressed and check_block(cursor, ms, player):
            press_duration = pygame.time.get_ticks() - press_start_time
            cursor = Cursor(mouse_x, mouse_y, press_duration, player, matr)
            bool_cursor = block_under_cursor(cursor, ms, press_duration // 100, player)
            if (bool_cursor != 0):
                dropped_blocks.append(bool_cursor)
        else:
            cursor = Cursor(mouse_x, mouse_y, 0, player, matr)
        draw(window, background, bg_image, player, blocks, water, offset_x, offset_y, cursor, dropped_blocks, inventory)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)
