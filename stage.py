import random

import pygame

from settings import *


from player import Player
from alien import Alien
from random import choice
from laser import Laser


class Stage:
    def __init__(self, gameOver, hiScore = 0):
        self.displaySurface = pygame.display.get_surface()
        self.gameOver = gameOver
        pygame.mouse.set_visible(False)

        # Groups
        self.mainGroup = pygame.sprite.Group()
        self.alienGroup = pygame.sprite.Group()

        # Player & Aliens
        self.ship = Player(screenSize[0] / 2, screenSize[1] - 32, self.mainGroup)
        self.createAliens(6, 8)
        self.alienDirection = 1
        self.alienStep = 0
        self.alienLasers = pygame.sprite.Group()

        # Gui
        self.score = 0
        self.hiScore = hiScore
        self.lives = 3
        self.wonSnip = mainFont.render('YOU WON!', False, 'Lime')

        # Bg
        self.stars = pygame.sprite.Group()
        for i in range(random.randint(64, 256)):
            star = Star(
                random.randint(0, screenSize[0]),
                random.randint(0, screenSize[0] - 3)
            )
            self.stars.add(star)

    def createAliens(self, rows, cols, xDist = 60, yDist = 60):
        for rowIndex, row in enumerate(range(rows)):
            for colIndex, col in enumerate(range(cols)):
                x = colIndex * xDist + 250
                y = rowIndex * yDist + 120
                if rowIndex < 2: color = 'red'
                elif rowIndex < 4: color = 'purple'
                else: color = 'green'
                Alien(x, y, color, (self.mainGroup, self.alienGroup))

    def moveAlien(self):
        self.alienStep += 1
        if self.alienStep >= 2:
            self.alienStep = 0
            for alien in self.alienGroup.sprites():
                if alien.rect.right > screenSize[0] - 128 and self.alienDirection > 0:
                    alien.rect.right = screenSize[0] - 128
                    self.alienDirection = -1
                    self.moveRows()
                elif alien.rect.left < 128 and self.alienDirection < 0:
                    alien.rect.left = 128
                    self.alienDirection = 1
                    self.moveRows()

                alien.rect.x += self.alienDirection

    def moveRows(self):
        for alien in self.alienGroup.sprites():
            alien.rect.y += 32
            if alien.rect.y >= screenSize[1] - 128:
                self.gameOver(self.score)

    def alienShoot(self):
        if self.alienGroup.sprites():
            attacker = choice(self.alienGroup.sprites())
            Laser(attacker.rect.midbottom, self.alienLasers, -4)

    def impactCheck(self):
        # Player Lasers
        for laser in self.ship.lasers:
            collidedAliens = pygame.sprite.spritecollide(laser, self.alienGroup, True)
            if collidedAliens:
                laser.kill()
                for alien in collidedAliens:
                    self.score += alien.value

        # Alien Lasers
        for laser in self.alienLasers:
            if self.ship.rect.colliderect(laser.rect):
                self.lives -= 1
                laser.kill()
                if self.lives <= 0:
                    self.gameOver(self.score)

    def drawGui(self):
        scoreTip = mainFont.render('SCORE: ', False, (255, 100, 20))
        scoreSnip = mainFont.render(str(self.score), False, 'White')
        self.displaySurface.blit(scoreTip, (64, 64))
        self.displaySurface.blit(scoreSnip, (64 + scoreTip.get_width() - 8, 64))

        hiScoreTip = mainFont.render('HI-SCORE: ', False, (255, 255, 20))
        hiScoreSnip = mainFont.render(str(self.hiScore), False, 'White')
        self.displaySurface.blit(hiScoreTip, (512, 64))
        self.displaySurface.blit(hiScoreSnip, (512 + hiScoreTip.get_width() - 8, 64))

        livesTip = mainFont.render('LIVES: ', False, (220, 20, 20))
        livesSnip = mainFont.render(str(self.lives), False, 'White')
        self.displaySurface.blit(livesTip, (64, 96))
        self.displaySurface.blit(livesSnip, (64 + scoreTip.get_width() - 8, 96))

        if not self.alienGroup.sprites():
            self.gameOver(self.score, win = True)

    def run(self):
        self.stars.update()
        self.stars.draw(self.displaySurface)
        self.moveAlien()
        self.impactCheck()
        self.ship.lasers.update()
        self.ship.lasers.draw(self.displaySurface)
        self.alienLasers.update()
        self.alienLasers.draw(self.displaySurface)
        self.mainGroup.update()
        self.mainGroup.draw(self.displaySurface)
        self.drawGui()