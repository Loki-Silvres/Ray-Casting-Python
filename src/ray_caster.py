import pygame, math
from settings import *
from ray import Ray
from player import Player
from map import Map

class RayCaster:
    def __init__(self, player: Player, map: Map):
        self.rays = []
        self.player = player
        self.map = map

    def castAllRays(self):
        self.rays = []
        rayAngle = (self.player.rotationAngle - FOV/2)
        for i in range(NUM_RAYS):
            ray = Ray(rayAngle, self.player, self.map)
            ray.cast()

            self.rays.append(ray)

            rayAngle += FOV / NUM_RAYS

    def render(self, screen):

        wall_counter = 0
        for ray in self.rays:
            ray.render(screen)

            line_height = (TILESIZE / ray.wall_distance) * WINDOW_HEIGHT / (math.tan(FOV/2) + EPSILON)
            draw_begin = (WINDOW_HEIGHT / 2) - (line_height / 2)
            draw_end = line_height

            pygame.draw.rect(screen, ray.wall_color, (wall_counter * RES + WINDOW_WIDTH, draw_begin, RES, draw_end))
            wall_counter += 1