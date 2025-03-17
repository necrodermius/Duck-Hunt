import pygame
import math
import random
from core.settings import DIFFICULTY_LEVEL


class Duck:
    def __init__(self, x, y, move_angle, direction="left"):
        self.x = x
        self.y = y
        self.move_angle = math.radians(move_angle)
        self.amplitude = 30
        self.frequency = 0.1
        self.angle = 0
        self.direction = direction

        self.size = 100
        self.speed = 7

        if direction == "left":
            self.image_down = pygame.image.load("assets/targets/4.png")
            self.image_up = pygame.image.load("assets/targets/3.png")
        else:
            self.image_up = pygame.image.load("assets/targets/2.png")
            self.image_down = pygame.image.load("assets/targets/1.png")

        if (DIFFICULTY_LEVEL[0] == 0):
            self.speed = random.randint(3, 6)
            self.size = random.randint(90, 120)

        elif (DIFFICULTY_LEVEL[0] == 1):
            self.speed = random.randint(6, 9)
            self.size = random.randint(60, 90)
        elif (DIFFICULTY_LEVEL[0] == 2):
            self.speed = random.randint(9, 13)
            self.size = random.randint(30, 60)

        self.image_up = pygame.transform.scale(self.image_up,
                                               (self.size+20,
                                                self.size)
                                               )
        self.image_down = pygame.transform.scale(self.image_down,
                                                 (self.size+20,
                                                  self.size)
                                                 )
        self.image = self.image_up

        if self.direction == "right":
            self.speed *= -1

        self.dx = math.cos(self.move_angle) * self.speed
        self.dy = math.sin(self.move_angle) * self.speed

        self.base_x = self.x
        self.base_y = self.y

    def update(self):
        self.base_x += self.dx
        self.base_y += self.dy

        perpendicular_offset = self.amplitude * math.sin(self.angle)
        perp_angle = self.move_angle + math.pi / 2

        self.x = self.base_x + perpendicular_offset * math.cos(perp_angle)
        self.y = self.base_y + perpendicular_offset * math.sin(perp_angle)

        self.angle += self.frequency

        if self.dy + perpendicular_offset * math.sin(perp_angle) < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down

        if self.direction == "left" and (self.base_x > 900
                                         or self.base_y < -50
                                         or self.base_y > 600):
            self.base_x = random.randint(-100, 0)
            self.base_y = random.randint(100, 500)
        elif self.direction == "right" and (self.base_x < -100
                                            or self.base_y < -50
                                            or self.base_y > 600):
            self.base_x = random.randint(900, 1000)
            self.base_y = random.randint(100, 500)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def check_collision(self, rect):
        duck_rect = pygame.Rect(self.x, self.y, self.size+20, self.size)
        return duck_rect.colliderect(rect)

    def get_score_value(self):
        duck_speed = abs(self.speed)
        return int(1/self.size + 5 * duck_speed)
