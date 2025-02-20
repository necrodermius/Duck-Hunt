import pygame
import random
import math

class Duck:
    def __init__(self, x, y):
        self.x = x
        self.start_y = y  
        self.y = y 
        self.speed = 2

        self.image_down = pygame.image.load("assets/targets/4.png")
        self.image_down = pygame.transform.scale(self.image_down, (50, 50))

        self.image = self.image_down
        self.width, self.height = self.image.get_size()
        
    def update(self):
        self.x += self.speed
        if self.x > 900:
            self.x = -50

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def check_collision(self, rect):
        duck_rect = pygame.Rect(self.x, self.y)
        return duck_rect.colliderect(rect)