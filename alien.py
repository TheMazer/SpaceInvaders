from settings import *


class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, color, group):
        super().__init__(group)
        self.image = pygame.image.load('assets/images/' + color + '.png')
        self.rect = self.image.get_rect(topleft = (x, y))

        if color == 'green': self.value = 100
        elif color == 'purple': self.value = 200
        elif color == 'red': self.value = 300