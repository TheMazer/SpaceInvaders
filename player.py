from settings import *

from laser import Laser


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.image = pygame.image.load('assets/images/player.png')
        self.rect = self.image.get_rect(midbottom = (x, y))

        # Movement
        self.direction = pygame.Vector2()
        self.speed = 4

        # Shooting
        self.cooldown = 0
        self.lasers = pygame.sprite.Group()

    def shoot(self):
        laser = Laser(self.rect.midtop, self.lasers)
        self.lasers.add(laser)

    def constraintsCheck(self):
        if self.rect.right >= screenSize[0]:
            self.rect.right = screenSize[0]
        elif self.rect.left <= 0:
            self.rect.left = 0

    def getInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if self.cooldown > 0:
            self.cooldown -= 1
        elif keys[pygame.K_w]:
            self.shoot()
            self.cooldown = 30

    def update(self):
        self.getInput()
        self.rect.topleft += self.direction * self.speed
        self.constraintsCheck()