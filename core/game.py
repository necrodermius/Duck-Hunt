import pygame
from core.settings import SCREEN_HEIGHT, SCREEN_WIDTH, FPS, BG_COLOR

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("CI/CD Duck Hunt")

        self.clock = pygame.time.Clock()
        self.running = True
    
    def run(self):
        while self.running:
            self.clock.tick(FPS)

            events = pygame.event.get()
        
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

        pygame.quit()