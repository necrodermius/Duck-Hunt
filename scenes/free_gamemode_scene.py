import pygame
from entities.duck import Duck

class GameScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.ducks = [Duck(x=300, y=200)]
        # Зброя
        # Лічильники

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pass # Постріл
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.scene_manager.set_scene("pause")

    def update(self):
        for duck in self.ducks:
            duck.update()
        # Перевіряємо попадання
        pass

    def draw(self, screen):
        for duck in self.ducks:
            duck.draw(screen)
            
        # Малюємо кулі
        # Малюємо текст (бали, кількість вистрілів)
        pass
