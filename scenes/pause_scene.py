import pygame

class PauseScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.pause_bg = pygame.image.load("assets/menus/pause-menu.png").convert_alpha()

        self.return_rect = pygame.Rect(410, 417, 390, 73)
        self.score_menu_rect = pygame.Rect(510, 560, 395, 70)

        self.previous_scene_name = "game"

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if self.return_rect.collidepoint(mouse_pos):
                    self.resume_previous_scene()
                elif self.score_menu_rect.collidepoint(mouse_pos):
                    self.scene_manager.set_scene("score")

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.pause_bg, (0, 0))

    def resume_previous_scene(self):
        prev_scene = self.scene_manager.scenes[self.previous_scene_name]

        if hasattr(prev_scene, 'pause_start') and prev_scene.pause_start is not None:
            paused_duration = pygame.time.get_ticks() - prev_scene.pause_start
            prev_scene.start_time += paused_duration
            prev_scene.pause_start = None

        self.scene_manager.set_scene(self.previous_scene_name)