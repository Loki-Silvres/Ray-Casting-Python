import math, pygame
from player import Player
from map import Map
from settings import *
from utils import normalizeAngle

class Ray:
    def __init__(self, angle, player: Player, map: Map):

        self.rayAngle = normalizeAngle(angle)
        self.player = player
        self.map = map
        self.wall_hit_x = None
        self.wall_hit_y = None
        self.wall_distance = None
        self.wall_color = None
        self.is_facing_left = self.rayAngle > (math.pi/2) \
                            and self.rayAngle < (3*math.pi/2)
        self.is_facing_right = not self.is_facing_left
        self.is_facing_up = self.rayAngle > (math.pi) \
                            and self.rayAngle < (2*math.pi)
        self.is_facing_down = not self.is_facing_up

    def cast(self):

        # HORIZONTAL CHECKING
        found_horizontal_wall = False
        horizontal_hit_x = None
        horizontal_hit_y = None

        first_horizontal_x = None
        first_horizontal_y = None

        if self.is_facing_up:
            first_horizontal_y = ((self.player.y) // TILESIZE) * TILESIZE - EPSILON
        elif self.is_facing_down:
            first_horizontal_y = ((self.player.y) // TILESIZE) * TILESIZE + TILESIZE

        first_horizontal_x = self.player.x + (first_horizontal_y - self.player.y) / (math.tan(self.rayAngle) + EPSILON)              

        next_horizontal_x = first_horizontal_x
        next_horizontal_y = first_horizontal_y

        delta_x = None
        delta_y = None

        if self.is_facing_up:
            delta_y = -TILESIZE 
        elif self.is_facing_down:
            delta_y = TILESIZE

        delta_x = delta_y / (math.tan(self.rayAngle) + EPSILON)

        while (     next_horizontal_x <= WINDOW_WIDTH
                and next_horizontal_y <= WINDOW_HEIGHT
                and next_horizontal_x >= 0
                and next_horizontal_y >= 0 
            ):
            if self.map.has_wall_at(next_horizontal_x,  next_horizontal_y):
                found_horizontal_wall = True
                horizontal_hit_x = next_horizontal_x
                horizontal_hit_y = next_horizontal_y
                break
            else:
                next_horizontal_x += delta_x
                next_horizontal_y += delta_y


        # VERTICAL CHECKING
        found_vertical_wall = False
        vertical_hit_x = None
        vertical_hit_y = None

        first_vertical_x = None
        first_vertical_y = None

        if self.is_facing_left:
            first_vertical_x = ((self.player.x) // TILESIZE) * TILESIZE - EPSILON
        elif self.is_facing_right:
            first_vertical_x = ((self.player.x) // TILESIZE) * TILESIZE + TILESIZE

        first_vertical_y = self.player.y + (first_vertical_x - self.player.x) * (math.tan(self.rayAngle))              

        next_vertical_x = first_vertical_x
        next_vertical_y = first_vertical_y

        delta_x = None
        delta_y = None

        if self.is_facing_left:
            delta_x = -TILESIZE 
        elif self.is_facing_right:
            delta_x = TILESIZE
        delta_y = delta_x * (math.tan(self.rayAngle))

        while (     next_vertical_x <= WINDOW_WIDTH
                and next_vertical_y <= WINDOW_HEIGHT
                and next_vertical_x >= 0
                and next_vertical_y >= 0 
            ):
            if self.map.has_wall_at(next_vertical_x,  next_vertical_y):
                found_vertical_wall = True
                vertical_hit_x = next_vertical_x
                vertical_hit_y = next_vertical_y
                break
            else:
                next_vertical_x += delta_x
                next_vertical_y += delta_y

        if found_horizontal_wall and found_vertical_wall:
            if math.dist(self.player.position, (horizontal_hit_x, horizontal_hit_y)) < math.dist(self.player.position, (vertical_hit_x, vertical_hit_y)):
                self.wall_hit_x = horizontal_hit_x
                self.wall_hit_y = horizontal_hit_y
                self.wall_distance = math.dist(self.player.position, (horizontal_hit_x, horizontal_hit_y))
                self.wall_color = WALL_MIN

            elif math.dist(self.player.position, (horizontal_hit_x, horizontal_hit_y)) > math.dist(self.player.position, (vertical_hit_x, vertical_hit_y)):
                self.wall_hit_x = vertical_hit_x
                self.wall_hit_y = vertical_hit_y
                self.wall_distance = math.dist(self.player.position, (vertical_hit_x, vertical_hit_y))
                self.wall_color = WALL_MAX
        
        else: 
            if found_horizontal_wall:
                self.wall_hit_x = horizontal_hit_x
                self.wall_hit_y = horizontal_hit_y
                self.wall_distance = math.dist(self.player.position, (horizontal_hit_x, horizontal_hit_y))
                self.wall_color = WALL_MIN
            elif found_vertical_wall:
                self.wall_hit_x = vertical_hit_x
                self.wall_hit_y = vertical_hit_y
                self.wall_distance = math.dist(self.player.position, (vertical_hit_x, vertical_hit_y))
                self.wall_color = WALL_MAX

        # Removes Fish-eye distortion
        if self.wall_distance is not None:
            self.wall_distance *= math.cos(self.player.rotationAngle - self. rayAngle)

            # Gives depth to colors
            self.wall_color = [min(255, channel * LIGHT_LEVEL / self.wall_distance) for channel in self.wall_color]
    
    def render(self, screen):
        if self.wall_hit_x is not None:
            pygame.draw.line(screen, RED, self.player.position, 
                        (self.wall_hit_x, self.wall_hit_y))
    