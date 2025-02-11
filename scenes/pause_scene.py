import pygame

class PauseScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.pause_bg = pygame.image.load("assets/menus/pause-menu.png").convert_alpha()

        self.return_rect = pygame.Rect(410, 417, 390, 73)
        self.main_menu_rect = pygame.Rect(510, 560, 395, 70)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.return_rect.collidepoint(mouse_pos):
                    self.scene_manager.set_scene("game")
                elif self.main_menu_rect.collidepoint(mouse_pos):
                    self.scene_manager.set_scene("menu")


    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.pause_bg, (0, 0))
