import pygame
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class MenuScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.menu_bg = pygame.image.load("assets/menus/main-menu.png").convert_alpha()

        self.settings_button_rect = pygame.Rect(460, 59, 360, 85)
        self.free_mode_rect = pygame.Rect(100, 345, 360, 85)
        self.limited_ammo_rect = pygame.Rect(100, 490, 360, 85)
        self.limited_time_rect = pygame.Rect(100, 635, 360, 85)

#        self.font = pygame.font.SysFont(None, 48)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.settings_button_rect.collidepoint(mouse_pos):
                    print("Налаштування (покищо заглушка)")
                elif self.free_mode_rect.collidepoint(mouse_pos):
                    self.scene_manager.set_scene("game")
                elif self.limited_ammo_rect.collidepoint(mouse_pos):
                    self.scene_manager.set_scene("ammo")
                elif self.limited_time_rect.collidepoint(mouse_pos):
                    print("Обмежений час (покищо заглушка)")

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.menu_bg, (0, 0))

