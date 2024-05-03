from settings import *


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, group, speed = 12):
        super().__init__(group)
        self.image = pygame.Surface((4, 20))
        self.image.fill('White' if speed > 0 else 'Red')
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed

    def checkTop(self):
        if self.rect.bottom >= screenSize[1]:
            self.kill()

    def update(self):
        self.rect.y -= self.speed
        self.checkTop()