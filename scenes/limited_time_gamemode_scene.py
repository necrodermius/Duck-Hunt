import pygame
import random
from entities.gun import Gun
from entities.duck import Duck

class LimitedTimeGameModeScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager

        self.pause_rect = pygame.Rect(670, 630, 210, 55)
        self.restart_rect = pygame.Rect(670, 708, 210, 55)

        self.game_bg = pygame.image.load("assets/bgs/free-play-bg.png").convert_alpha()
        self.game_bn = pygame.image.load("assets/banners/free-play-banner.png").convert_alpha()

        self.ducks = []
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_interval = 2000

        self.gun = Gun()

        self.score = 0
        self.hits_count = 0
        self.shots_count = 0

        self.start_time = pygame.time.get_ticks()
        self.time_limit = 30000 

        self.pause_start = None

    def restart(self):
        self.score = 0
        self.hits_count = 0
        self.shots_count = 0
        self.ducks.clear()
        self.start_time = pygame.time.get_ticks()

    def handle_events(self, events):
        for event in events:
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.restart_rect.collidepoint(mouse_pos):
                    self.restart()
                elif self.pause_rect.collidepoint(mouse_pos):
                    self.scene_manager.scenes["pause"].previous_scene_name = "time"
                    self.pause_start = pygame.time.get_ticks()
                    self.go_to_score_scene()
                    self.scene_manager.set_scene("pause")
                else:
                    self.shots_count += 1
                    bullet_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)
                    for duck in self.ducks[:]:
                        if duck.check_collision(bullet_rect):
                            self.ducks.remove(duck)
                            self.hits_count += 1
                            self.score += duck.get_score_value()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.pause_start = pygame.time.get_ticks()
                self.scene_manager.scenes["pause"].previous_scene_name = "time"
                self.go_to_score_scene()
                self.scene_manager.set_scene("pause")

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time

        if elapsed >= self.time_limit:
            self.go_to_score_scene(flag=True)
            return

        if len(self.ducks) < 15 and current_time - self.last_spawn_time > self.spawn_interval:
            if random.choice([True, False]):
                new_duck = Duck(
                    x=random.randint(-200, -50),
                    y=random.randint(100, 500),
                    move_angle=random.randint(-30, 30),
                    direction="left"
                )
            else:
                new_duck = Duck(
                    x=random.randint(900, 1000),
                    y=random.randint(100, 500),
                    move_angle=random.randint(-30, 30),
                    direction="right"
                )
            self.ducks.append(new_duck)
            self.last_spawn_time = current_time

        for duck in self.ducks:
            duck.update()

    def draw(self, screen):
        screen.blit(self.game_bg, (0, 0))
        self.gun.draw(screen)
        for duck in self.ducks:
            duck.draw(screen)
        screen.blit(self.game_bn, (0, 600))

        current_time_ms = pygame.time.get_ticks() - self.start_time
        current_time_sec = current_time_ms / 1000.0
        remaining_time_sec = max(0, (self.time_limit - current_time_ms) / 1000.0)

        font = pygame.font.Font("assets/font/PT-Serif-Bold-Italic.ttf", 31)

        remaining_surface = font.render(f"{remaining_time_sec:.1f}", True, 'white')
        total_shots_surface = font.render(f"{self.shots_count}", True, 'white')
        hits_surface = font.render(f"{self.hits_count}", True, 'white')
        score_surface = font.render(f"{self.score}", True, 'white')

        screen.blit(score_surface, (377, 622))
        screen.blit(remaining_surface, (360, 659))
        screen.blit(total_shots_surface, (439, 697))
        screen.blit(hits_surface, (488, 738))


    def go_to_score_scene(self, flag = False):
        current_time_ms = pygame.time.get_ticks() - self.start_time
        current_time_sec = current_time_ms / 1000.0

        score_scene = self.scene_manager.scenes["score"]
        score_scene.set_stats(
            time_sec=current_time_sec,
            score=self.score,
            hits_count=self.hits_count,
            shots_count=self.shots_count
        )
        if flag:
            self.scene_manager.set_scene("score")
