import pygame
from Settings import *

class Alien(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        file_path = "Sprites/" + color + ".png"
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x, y))
    
        if color == "red": self.value = SCORE_RED
        elif color == "green": self.value = SCORE_GREEN
        else: self.value = SCORE_YELLOW

    def update(self, direction):
        self.rect.x += direction

class Extra(pygame.sprite.Sprite):
    def __init__(self, side, screen_width):
        super().__init__()
        self.image = pygame.image.load("Sprites\extra.png").convert_alpha()

        if side == "right":
            x = screen_width + 50
            self.speed = -EXTRA_SPEED
        else:
            x = -50
            self.speed = EXTRA_SPEED

        self.rect = self.image.get_rect(topleft = (x, 80))

    def update(self):
        self.rect.x += self.speed