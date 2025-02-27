import pygame
import math
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Gun:
    def __init__(self):
        self.gun_image = pygame.transform.scale(pygame.image.load("assets/gun/gun.png").convert_alpha(), (200, 200))
        self.shot_image = pygame.image.load("assets/gun/shot.png") 
        self.shot_image = pygame.transform.scale(self.shot_image, (25, 25))
        self.gun_point = (SCREEN_WIDTH / 2 , SCREEN_HEIGHT - 200)

        pygame.mixer.init()
        self.shot_sound = pygame.mixer.Sound("assets/sounds/shot.wav")
        self.shot_sound.set_volume(0.1)  
        self.shot_triggered = False

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        clicks = pygame.mouse.get_pressed()

        if mouse_pos[0] != self.gun_point[0]:
            slope = (mouse_pos[1] - self.gun_point[1]) / (mouse_pos[0] - self.gun_point[0])
        else:
            slope = -100000

        angle = math.atan(slope)
        rotation = math.degrees(angle)

        if mouse_pos[0] < SCREEN_WIDTH / 2:
            flipped_image = pygame.transform.flip(self.gun_image, True, False)

            if mouse_pos[1] < 600:
                rotated_image = pygame.transform.rotate(flipped_image, 90 - rotation)
                screen.blit(rotated_image, (SCREEN_WIDTH / 2 - 90, SCREEN_HEIGHT - 350))

                if clicks[0] and not self.shot_triggered:
                    self.shot_triggered = True
                    shot_x = mouse_pos[0] - self.shot_image.get_width() // 2
                    shot_y = mouse_pos[1] - self.shot_image.get_height() // 2
                    screen.blit(self.shot_image, (shot_x, shot_y))

                    self.shot_sound.stop()
                    self.shot_sound.play()

        else:
            if mouse_pos[1] < 600:
                rotated_image = pygame.transform.rotate(self.gun_image, 270 - rotation)
                screen.blit(rotated_image, (SCREEN_WIDTH / 2 - 30, SCREEN_HEIGHT - 350))

                if clicks[0] and not self.shot_triggered:
                    self.shot_triggered = True
                    shot_x = mouse_pos[0] - self.shot_image.get_width() // 2
                    shot_y = mouse_pos[1] - self.shot_image.get_height() // 2
                    screen.blit(self.shot_image, (shot_x, shot_y))

                    self.shot_sound.stop()
                    self.shot_sound.play()

        if not clicks[0]:
                self.shot_triggered = False
