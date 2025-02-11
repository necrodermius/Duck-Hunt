import pygame
from core.settings import SCREEN_HEIGHT, SCREEN_WIDTH, FPS, BG_COLOR
from core.scene_manager import SceneManager
from scenes.menu_scene import MenuScene
from scenes.free_gamemode_scene import GameScene
from scenes.pause_scene import PauseScene

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("CI/CD Duck Hunt")

        self.scene_manager = SceneManager()
        self.scene_manager.add_scene("menu", MenuScene(self.scene_manager))
        self.scene_manager.add_scene("pause", PauseScene(self.scene_manager))
        self.scene_manager.add_scene("game", GameScene(self.scene_manager))
        self.scene_manager.set_scene("menu")

        self.clock = pygame.time.Clock()
        self.running = True
    
    def run(self):
        while self.running:
            self.clock.tick(FPS)

            events = pygame.event.get()
        
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.scene_manager.update(events)

            self.screen.fill(BG_COLOR)
            self.scene_manager.draw(self.screen)
            pygame.display.flip()
            
        pygame.quit()