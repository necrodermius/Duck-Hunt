import pygame
import random
import math

class Duck:
    def __init__(self, x, y):
        self.x = x
        self.start_y = y  
        self.y = y 
        self.speed = 5 
        self.amplitude = 30 
        self.frequency = 0.05  
        self.angle = 0  

        self.image_up = pygame.image.load("assets/targets/4.png")
        self.image_down = pygame.image.load("assets/targets/3.png")

        self.image_up = pygame.transform.scale(self.image_up, (50, 50))
        self.image_down = pygame.transform.scale(self.image_down, (50, 50))

        self.image = self.image_up
        self.width, self.height = self.image.get_size()

        
    def update(self):
        self.x += self.speed
        
        if self.x > 900:
            self.x = -50

        previous_y = self.y
        self.y = self.start_y + self.amplitude * math.sin(self.angle)
        self.angle += self.frequency

        if self.y > previous_y:
            self.image = self.image_down
        else:
            self.image = self.image_up

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def check_collision(self, rect):
        duck_rect = pygame.Rect(self.x, self.y)
        return duck_rect.colliderect(rect)