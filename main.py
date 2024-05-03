from settings import *

from stage import Stage


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(screenSize)
        pygame.display.set_caption('Space Invaders')

        self.clock = pygame.time.Clock()
        self.hiScore = 0

        self.startGame(self.hiScore)
        pygame.time.set_timer(self.alienShootEvent, 1000)

    def startGame(self, hiScore):
        if hiScore > self.hiScore:
            self.hiScore = hiScore
        self.currentStage = Stage(self.gameOver, self.hiScore)
        self.alienShootEvent = pygame.USEREVENT + 1

    def gameOver(self, score, win = False):
        self.alienShootEvent = None
        record = score > self.hiScore
        self.currentStage = EndScreen(score, self.startGame, record, win)

    def run(self):
        running = True
        while running:
            self.screen.fill('Black')
            self.clock.tick(fps)
            self.currentStage.run()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                elif event.type == self.alienShootEvent:
                    self.currentStage.alienShoot()


class EndScreen:
    def __init__(self, score, startGame, record = False, win = False):
        self.displaySurface = pygame.display.get_surface()
        self.startGame = startGame
        self.snip = mainFont.render('GAME OVER', False, 'Red')
        self.scoreSnip = mainFont.render('SCORE: ' + str(score), False, 'White')
        if win: self.recordSnip = mainFont.render('YOU WON!', False, 'Lime')
        elif record: self.recordSnip = mainFont.render('NEW RECORD!', False, 'Yellow')
        else: self.recordSnip = None
        self.continueSnip = smallFont.render('PRESS [SPACE] TO CONTINUE', False, (60, 60, 60))
        self.score = score

    def run(self):
        self.displaySurface.blit(self.snip, (screenSize[0] / 2 - self.snip.get_width() / 2, 256))
        self.displaySurface.blit(self.scoreSnip, (screenSize[0] / 2 - self.scoreSnip.get_width() / 2, 320))
        if self.recordSnip is not None:
            self.displaySurface.blit(self.recordSnip, (screenSize[0] / 2 - self.recordSnip.get_width() / 2, 360))
        self.displaySurface.blit(self.continueSnip, (screenSize[0] / 2 - self.continueSnip.get_width() / 2, 560))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.startGame(self.score)


if __name__ == '__main__':
    game = Game()
    game.run()