import sys
import random
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
                # Set fps
        self.clock = pygame.time.Clock()
        self.fps_number = 90

class SNAKE(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        WIDTH = 10
        HEIGHT = 10
        self.rect = pygame.rect.Rect((self.x, self.y, WIDTH, HEIGHT))

    def handle_keys(self):
        key = pygame.key.get_pressed()
        dist = 1
        if key[pygame.K_LEFT]:
           self.rect.move_ip(-1, 0)
        if key[pygame.K_RIGHT]:
           self.rect.move_ip(1, 0)
        if key[pygame.K_UP]:
           self.rect.move_ip(0, -1)
        if key[pygame.K_DOWN]:
           self.rect.move_ip(0, 1)

    def draw(self):
        pygame.draw.rect(screen, COLOR.WHITE, self.rect)

class APPLE(object):
    def __init__(self):
        random_x_pos = random.randint(0,SCREEN_WIDTH)
        random_y_pos = random.randint(0,SCREEN_HEIGHT)
        self.x = random_x_pos
        self.y = random_y_pos
        WIDTH = 10
        HEIGHT = 10
        self.rect = pygame.rect.Rect((self.x, self.y, WIDTH, HEIGHT))
    def draw(self):
        pygame.draw.rect(screen, COLOR.WHITE, self.rect)           

# Object init
world = WORLD()
snake = SNAKE()
apple = APPLE()
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
        snake.draw()
        snake.handle_keys()

        apple.draw()

        pygame.display.update()
        world.clock.tick(world.fps_number)


if __name__ == "__main__":
    main()

        