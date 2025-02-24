import pygame
import math
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Gun:
    def __init__(self):
        self.gun_image = pygame.image.load("assets/gun/gun.png").convert_alpha()
        self.gun_point = (SCREEN_WIDTH / 2 , SCREEN_HEIGHT - 200)

    def draw(self, screen):
      pass
