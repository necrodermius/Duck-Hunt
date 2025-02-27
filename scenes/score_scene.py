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
                mouse_pos = pygame.mouse.get_pos()
                if self.main_menu_rect.collidepoint(mouse_pos):
                    self.scene_manager.scenes["game"].restart()
                    self.scene_manager.scenes["ammo"].restart()
                    self.scene_manager.set_scene("menu")

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.score_bg, (0, 0))

        # Приклад відображення тексту
        font = pygame.font.SysFont('Times New Roman', 30)

        # Формуємо інформацію
        time_surface = font.render(f"Час: {self.final_time:.1f} сек", True, 'white')
        score_surface = font.render(f"Очки: {self.score}", True, 'white')
        hits_surface = font.render(f"Збиті качки: {self.hits_count}", True, 'white')
        shots_surface = font.render(f"Загальна кількість пострілів: {self.shots_count}", True, 'white')

        # Виводимо текст (позиції можна налаштовувати)
        screen.blit(time_surface, (300, 300))
        screen.blit(score_surface, (300, 340))
        screen.blit(hits_surface, (300, 380))
        screen.blit(shots_surface, (300, 420))

        # Тут можна додати надпис на кнопці повернення у меню (заглушка)
        # font.render("Меню", True, 'white'), ...
        # Але зараз маємо лише прямокутник + handle_events()

