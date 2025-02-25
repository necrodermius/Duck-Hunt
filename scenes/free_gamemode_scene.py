import pygame
from entities.duck import Duck
import random

class GameScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.ducks = []  
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_interval = 2000
        # Зброя
        # Лічильники

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pass # Постріл
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.scene_manager.set_scene("pause")

    def update(self):
        current_time = pygame.time.get_ticks()
        if len(self.ducks) < 15 and current_time - self.last_spawn_time > self.spawn_interval:
            if random.choice([True, False]):
                new_duck = Duck(x=random.randint(-200, -50), y=random.randint(100, 500), move_angle=random.randint(-30, 30), direction="left")
            else:
                new_duck = Duck(x=random.randint(900, 1000), y=random.randint(100, 500), move_angle=random.randint(-30, 30), direction="right")
            
            self.ducks.append(new_duck)
            self.last_spawn_time = current_time

        for duck in self.ducks:
            duck.update()

    def draw(self, screen):
        for duck in self.ducks:
            duck.draw(screen)
            
        # Малюємо кулі
        # Малюємо текст (бали, кількість вистрілів)
        pass
