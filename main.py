import sys

import pygame

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))

class COLOR:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

class WORLD(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.game_active = True

class BLOCK(WORLD):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.WIDTH = 50
        self.HEIGHT = 10
        self.block = (self.x, self.y, self.WIDTH, self.HEIGHT)

    def move_block(self):
        self.x += 5


# Object init
world = WORLD()
block = (0, 0, 50, 10)
def main():
    while world.game_active:
        screen.fill(COLOR.BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    world.game_active = False
        pygame.draw.rect(screen, COLOR.WHITE, block)
        pygame.display.flip()


if __name__ == "__main__":
    main()

        