import pygame
import math
from settings import *
from map import Map
from utils import normalizeAngle

class Player:
    def __init__(self, map: Map):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        self.radius = PLAYER_RADIUS
        self.rotationAngle = 0
        self.turnDirection = 0 # 1:RIGHT, -1:LEFT, 0:NONE
        self.walkDirection = 0 # 1:FORWARD, -1:BACKWARD, 0:STOP
        self.moveSpeed = WALK_SPEED
        self.rotationSpeed = ROTATION_SPEED
        self.directionLength = PLAYER_DIRECTION_LENGTH
        self.map = map
    
    @property
    def position(self):
        return [self.x, self.y]
    
    def update(self):

        keys = pygame.key.get_pressed()

        self.turnDirection = 0
        self.walkDirection = 0

        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.turnDirection = 1
        elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.turnDirection = -1
        
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.walkDirection = 1
        elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            self.walkDirection = -1

        self.rotationAngle += self.turnDirection * self.rotationSpeed
        self.rotationAngle = normalizeAngle(self.rotationAngle)
        
        moveStep = self.walkDirection * self.moveSpeed

        next_x = self.x
        next_y = self.y
        next_x += math.cos(self.rotationAngle) * moveStep
        next_y += math.sin(self.rotationAngle) * moveStep
        
        if not self.map.has_wall_at(next_x, next_y):
            self.x = next_x
            self.y = next_y

        
    def render(self, screen):
        pygame.draw.circle(screen, RED, self.position, self.radius) 
        # pygame.draw.line(screen, RED, 
        #                    self.position, 
        #     (self.x + self.directionLength * math.cos(self.rotationAngle), 
        #      self.y + self.directionLength * math.sin(self.rotationAngle)))