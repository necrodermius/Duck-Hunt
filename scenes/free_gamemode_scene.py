import pygame
from entities.gun import Gun

class GameScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.pause_rect = pygame.Rect(670, 630, 210, 55)
        self.menu_rect = pygame.Rect(670, 708, 210, 55)

        self.game_bg = pygame.image.load("assets/bgs/free-play-bg.png").convert_alpha()
        self.game_bn = pygame.image.load("assets/banners/free-play-banner.png").convert_alpha()
        # Список качок
        self.gun = Gun()
        # Лічильники

    def handle_events(self, events):
        for event in events:
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_rect.collidepoint(mouse_pos):
                    self.scene_manager.set_scene("menu")
                elif self.pause_rect.collidepoint(mouse_pos):
                    self.scene_manager.set_scene("pause")
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.scene_manager.set_scene("pause")



    def update(self):
        # Оновлення качок
        # Перевіряємо попадання
        pass

    def draw(self, screen):
        screen.blit(self.game_bg, (0, 0))
        screen.blit(self.game_bn, (0, 600))
        # Малюємо качок
        self.gun.draw(screen)
        # Малюємо кулі
        # Малюємо текст (бали, кількість вистрілів)
        pass
