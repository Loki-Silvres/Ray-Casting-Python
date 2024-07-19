import pygame
from settings import *
from map import Map
from player import Player
from ray_caster import RayCaster

if __name__ == "__main__":
    map = Map()
    player = Player(map)
    screen = pygame.display.set_mode((WINDOW_WIDTH * 2, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    ray_caster = RayCaster(player, map)

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        player.update()
        ray_caster.castAllRays()
        screen.fill(BLACK)
        map.render(screen)
        player.render(screen)
        ray_caster.render(screen)
        pygame.display.update()
