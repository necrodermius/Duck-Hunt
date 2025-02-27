import pygame
import math
import random

class Duck:
    def __init__(self, x, y, move_angle, direction="left"):
        self.x = x
        self.start_y = y
        self.y = y
        self.move_angle = math.radians(move_angle)
        self.speed = random.randint(4, 7)

        self.amplitude = 30
        self.frequency = 0.05
        self.angle = 0
        self.direction = direction

        if direction == "left":
            self.image_down = pygame.image.load("assets/targets/4.png")  
            self.image_up = pygame.image.load("assets/targets/3.png")  
        else:
            self.image_up = pygame.image.load("assets/targets/2.png")  
            self.image_down = pygame.image.load("assets/targets/1.png")  

        self.image_up = pygame.transform.scale(self.image_up, (50, 50))
        self.image_down = pygame.transform.scale(self.image_down, (50, 50))
        self.image = self.image_up

        self.direction = direction
        if self.direction == "right":
            self.speed *= -1

        self.dx = math.cos(self.move_angle) * self.speed
        self.dy = math.sin(self.move_angle) * self.speed

        self.base_x = self.x
        self.base_y = self.start_y
        self.angle = 0

    def update(self):
        self.base_x += self.dx
        self.base_y += self.dy

        perpendicular_offset = self.amplitude * math.sin(self.angle)
        perp_angle = self.move_angle + math.pi / 2

        self.x = self.base_x + perpendicular_offset * math.cos(perp_angle)
        self.y = self.base_y + perpendicular_offset * math.sin(perp_angle)

        perpendicular_offset = self.amplitude * math.sin(self.angle)
        perp_angle = self.move_angle + math.pi / 2
        self.x = self.base_x + perpendicular_offset * math.cos(perp_angle)
        self.y = self.base_y + perpendicular_offset * math.sin(perp_angle)

        self.angle += self.frequency

        if self.dy + perpendicular_offset * math.sin(perp_angle) < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down

        if self.direction == "left" and (self.base_x > 900 or self.base_y < -50 or self.base_y > 650):
            self.base_x = random.randint(-100, 0)
            self.base_y = random.randint(100, 500)
        elif self.direction == "right" and (self.base_x < -100 or self.base_y < -50 or self.base_y > 650):
            self.base_x = random.randint(900, 1000)
            self.base_y = random.randint(100, 500)

        self.angle += self.frequency

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def check_collision(self, rect):
        duck_rect = pygame.Rect(self.x, self.y, 50, 50)
        return duck_rect.colliderect(rect)

    def get_score_value(self):
        duck_speed = abs(self.speed)
        return int(10 + 5 * duck_speed)
