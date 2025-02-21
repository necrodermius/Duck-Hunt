import pygame
import random
import math

class Duck:
    def __init__(self, x, y, direction="left"):
        self.x = x
        self.start_y = y  
        self.y = y 
        self.speed = 5 if direction == "left" else -3  
        self.amplitude = 30 
        self.frequency = 0.05  
        self.angle = 0  
        self.direction = direction
        
        
        if self.direction == "left":
            self.image_up = pygame.image.load("assets/targets/4.png")
            self.image_down = pygame.image.load("assets/targets/3.png")
        else:
            self.image_up = pygame.image.load("assets/targets/2.png")
            self.image_down = pygame.image.load("assets/targets/1.png")

        self.image_up = pygame.transform.scale(self.image_up, (50, 50))
        self.image_down = pygame.transform.scale(self.image_down, (50, 50))

        self.image = self.image_up
        self.width, self.height = self.image.get_size()

        
    def update(self):
        self.x += self.speed
        
        if self.direction == "left" and self.x > 900:  
            self.x = random.randint(-100, 0)
            self.start_y = random.randint(100, 500)
        elif self.direction == "right" and self.x < -100: 
            self.x = random.randint(900, 1000)
            self.start_y = random.randint(100, 500)

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