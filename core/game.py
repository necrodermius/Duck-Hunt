import pygame
from core.settings import SCREEN_HEIGHT, SCREEN_WIDTH, FPS, BG_COLOR
from core.scene_manager import SceneManager

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("CI/CD Duck Hunt")

        self.scene_manager = SceneManager()

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