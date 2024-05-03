import random

import pygame
pygame.init()

# Screen Setup
screenSize = (960, 840)

# Game Properties
fps = 120

# Fonts
mainFont = pygame.font.Font('assets/fonts/PressStart2P.ttf', 20)
smallFont = pygame.font.Font('assets/fonts/PressStart2P.ttf', 16)


class Star(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        size = random.randint(1, 3)
        self.image = pygame.Surface((size, size))
        self.image.fill('White')
        self.image.set_alpha(random.randint(20, 200))
        self.rect = self.image.get_rect(center = (x, y))
        self.step = random.randint(2, 8)
        self.currentStep = 0

    def update(self):
        self.currentStep += 1
        if self.currentStep >= self.step:
            self.currentStep = 0
            self.rect.y += 1
            if self.rect.top >= screenSize[1]:
                self.rect.bottom = 0