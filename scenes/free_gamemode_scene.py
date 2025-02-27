import pygame
from entities.gun import Gun
from entities.duck import Duck
import random

class GameScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager

        self.pause_rect = pygame.Rect(670, 630, 210, 55)
        self.menu_rect = pygame.Rect(670, 708, 210, 55)

        self.game_bg = pygame.image.load("assets/bgs/free-play-bg.png").convert_alpha()
        self.game_bn = pygame.image.load("assets/banners/free-play-banner.png").convert_alpha()

        self.ducks = []  
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_interval = 2000
        
        self.gun = Gun()
        self.hits_count = 0
        self.shots_count = 0
        self.start_time = pygame.time.get_ticks()


    def handle_events(self, events):
        for event in events:
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_rect.collidepoint(mouse_pos):
                    self.scene_manager.set_scene("menu")
                elif self.pause_rect.collidepoint(mouse_pos):
                    self.scene_manager.set_scene("pause")
                else:
                    self.shots_count += 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.scene_manager.set_scene("pause")



    def update(self):
        current_time = pygame.time.get_ticks()
        if len(self.ducks) < 15 and current_time - self.last_spawn_time > self.spawn_interval:
            y_pos = random.randint(50, 500) 
            if random.choice([True, False]):
                new_duck = Duck(x=random.randint(-200, -50), y=y_pos, move_angle=random.randint(-20, 20), direction="left")
            else:
                new_duck = Duck(x=random.randint(900, 1000), y=y_pos, move_angle=random.randint(-20, 20), direction="right")
            self.ducks.append(new_duck)
            self.last_spawn_time = current_time

        for duck in self.ducks:
            duck.update()

    def draw(self, screen):
        screen.blit(self.game_bg, (0, 0))

        for duck in self.ducks:
            duck.draw(screen)

        self.gun.draw(screen)
        screen.blit(self.game_bn, (0, 600))

        current_time_ms = pygame.time.get_ticks() - self.start_time
        current_time_sec = current_time_ms / 1000.0


        font = pygame.font.SysFont("Times New Roman", 36)
        time_surface = font.render(f"Час: {current_time_sec:.1f}", True, (255, 255, 255))
        total_shots_surface = font.render(f"Постірілів відбулося: {self.shots_count}", True, (255, 255, 255))
        screen.blit(time_surface, (290, 615))
        screen.blit(total_shots_surface, (290, 645))
            
        pass
