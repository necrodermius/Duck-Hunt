import pygame

class ScoreScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.score_bg = pygame.image.load("assets/menus/score-menu.png").convert_alpha()

        self.main_menu_rect = pygame.Rect(225, 552, 420, 95)

        self.final_time = 0
        self.score = 0
        self.hits_count = 0
        self.shots_count = 0

    def set_stats(self, time_sec, score, hits_count, shots_count):
        self.final_time = time_sec
        self.score = score
        self.hits_count = hits_count
        self.shots_count = shots_count

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if self.main_menu_rect.collidepoint(mouse_pos):
                    self.scene_manager.scenes["game"].restart()
                    self.scene_manager.scenes["ammo"].restart()
                    self.scene_manager.scenes["time"].restart()
                    self.scene_manager.set_scene("menu")

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.score_bg, (0, 0))

        font = pygame.font.Font("assets/font/PT-Serif-Bold-Italic.ttf", 60)

        time_surface = font.render(f"{self.final_time:.1f}", True, '#50757c')
        score_surface = font.render(f"{self.score}", True, '#50757c')
        hits_surface = font.render(f"{self.hits_count}", True, '#50757c')
        shots_surface = font.render(f"{self.shots_count}", True, '#50757c')

        screen.blit(score_surface, (282, 158))
        screen.blit(hits_surface, (378, 240))
        screen.blit(shots_surface, (277, 321))
        screen.blit(time_surface, (155, 403))

