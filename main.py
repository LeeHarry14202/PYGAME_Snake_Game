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
        # Set direction
        self.direction = 'RIGHT'


class SNAKE(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.WIDTH = 100 / 4
        self.HEIGHT = 100 / 4
        self.speed = 3
        self.list_snake = []
        self.rect = pygame.rect.Rect((self.x, self.y, self.WIDTH, self.HEIGHT))

    def draw(self, x, y):
        if x != self.x or y != self.y:
            self.x = x
            self.y = y
        self.rect = pygame.rect.Rect((self.x, self.y, self.WIDTH, self.HEIGHT))
        pygame.draw.rect(screen, COLOR.WHITE, self.rect)

    def change_direction(self):
        if world.direction == 'RIGHT':     
            self.x += self.speed
        elif world.direction == 'LEFT':
            self.x -= self.speed
        elif world.direction == 'UP':
            self.y -= self.speed
        elif world.direction == 'DOWN':
            self.y += self.speed
        return self.x, self.y

    def reset_snake(self):
        if self.x >= SCREEN_WIDTH:
            self.x = 0
        elif self.x <= 0:
            self.x = SCREEN_WIDTH
        if self.y <= 0:
            self.y = SCREEN_HEIGHT
        elif self.y >= SCREEN_HEIGHT:
            self.y = 0
        return self.x, self.y


class APPLE(object):
    def __init__(self):
        random_x_pos = random.randint(0, SCREEN_WIDTH)
        random_y_pos = random.randint(0, SCREEN_HEIGHT)
        self.x = random_x_pos
        self.y = random_y_pos
        WIDTH = 100 / 4
        HEIGHT = 100 / 4
        self.radius = 20
        self.rect = pygame.rect.Rect((self.x, self.y, WIDTH, HEIGHT))

    def draw(self):
        pygame.draw.circle(screen, COLOR.RED, (self.x, self.y), self.radius)


# Set timer for apple
spawn_apple = pygame.USEREVENT
spawn_apple_time = 1200
pygame.time.set_timer(spawn_apple, spawn_apple_time)

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
                if event.key == pygame.K_RIGHT:
                    world.direction = 'RIGHT'
                if event.key == pygame.K_LEFT:
                    world.direction = 'LEFT'
                if event.key == pygame.K_DOWN:
                    world.direction = 'DOWN'
                if event.key == pygame.K_UP:
                    world.direction = 'UP'

        snake.x, snake.y = snake.change_direction()
        snake.x, snake.y = snake.reset_snake()        
        snake.draw(snake.x, snake.y)

        apple.draw()

        if apple.rect.colliderect(snake.rect):
            print('touch')

        pygame.display.update()
        world.clock.tick(world.fps_number)


if __name__ == "__main__":
    main()

        