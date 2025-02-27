import pygame
from core.settings import DIFFICULTY_LEVEL

class SettingsMenu:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.settings_bg = pygame.image.load("assets/menus/settings-menu.png").convert_alpha()
        
        self.easy_mode_rect = pygame.Rect(418, 310, 366, 98)
        self.medium_mode_rect = pygame.Rect(418, 453, 366, 98)
        self.hard_mode_rect = pygame.Rect(418, 594, 366, 98)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.easy_mode_rect.collidepoint(mouse_pos):
                    DIFFICULTY_LEVEL[0] = 0
                    self.scene_manager.set_scene("menu")

                if self.medium_mode_rect.collidepoint(mouse_pos):
                    DIFFICULTY_LEVEL[0] = 1
                    self.scene_manager.set_scene("menu")
                    
                if self.hard_mode_rect.collidepoint(mouse_pos):
                    DIFFICULTY_LEVEL[0] = 2
                    self.scene_manager.set_scene("menu")
                    

        
    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.settings_bg, (0, 0))