import pygame
from main_functions.game_function import GameFunctions
from settings import Settings


def main():
    pygame.init()
    # pg.font.init()
    settings = Settings()
    window = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    gf = GameFunctions(window)
    run=True

    while run:
        gf.update_screen()
        gf.check_events()
        # clock.tick(settings.FPS)


main()