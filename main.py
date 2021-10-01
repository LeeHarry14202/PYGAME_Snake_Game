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
        # Set score
        self.score = 0

    def restart(self):
        world.game_active = True
        apple.list_apple.clear()
        snake.x = SCREEN_WIDTH / 2
        snake.y = SCREEN_HEIGHT / 2
        world.direction = 'RIGHT'


class SNAKE(object):
    def __init__(self):
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.WIDTH = 10
        self.HEIGHT = 10
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

    def hit_wall(self):
        if self.x > SCREEN_WIDTH:
            # self.x = 0
            world.game_active = False
        elif self.x < 0:
            # self.x = SCREEN_WIDTH
            world.game_active = False
        if self.y < 0:
            # self.y = SCREEN_HEIGHT
            world.game_active = False
        elif self.y > SCREEN_HEIGHT:
            # self.y = 0
            world.game_active = False
        # return self.x, self.y
        return world.game_active


class APPLE(object):
    def __init__(self):
        self.WIDTH = 20
        self.HEIGHT = 20
        self.radius = 10
        self.list_apple = []
        self.rect = pygame.rect.Rect((-SCREEN_WIDTH/2, -SCREEN_HEIGHT/2, self.WIDTH, self.HEIGHT))
  
    def create_apple(self):
        random_x_pos = random.randint(20, SCREEN_WIDTH - snake.WIDTH)
        random_y_pos = random.randint(20, SCREEN_HEIGHT - snake.HEIGHT)
        x = random_x_pos
        y = random_y_pos
        position = (x, y)
        # Update apple rect
        self.rect = pygame.rect.Rect((x, y, self.WIDTH, self.HEIGHT))
        return position

    def draw(self, list_apple):
        for apple_ in list_apple:
            pygame.draw.circle(screen, COLOR.RED, apple_, self.radius)
        # If don't have this, the previous apple wont' disappear
        if len(list_apple) > 1:
            list_apple.pop(0)


class WALL(object):
    def __init__(self):
        self.list_wall = []

    def draw(self):
        wall_1 = pygame.rect.Rect(0, 0, SCREEN_WIDTH, 10)
        wall_2 = pygame.rect.Rect(0, 0, 10, SCREEN_HEIGHT)
        wall_3 = pygame.rect.Rect(SCREEN_WIDTH - snake.WIDTH, 0, 10, SCREEN_HEIGHT)
        wall_4 = pygame.rect.Rect(0, SCREEN_HEIGHT - snake.HEIGHT, SCREEN_WIDTH, 10)
        pygame.draw.rect(screen, COLOR.WHITE, wall_1)
        pygame.draw.rect(screen, COLOR.WHITE, wall_2)
        pygame.draw.rect(screen, COLOR.WHITE, wall_3)
        pygame.draw.rect(screen, COLOR.WHITE, wall_4)


# Set timer for apple
spawn_apple = pygame.USEREVENT
spawn_apple_time = 2000
pygame.time.set_timer(spawn_apple, spawn_apple_time)

# Object init
world = WORLD()
snake = SNAKE()
apple = APPLE()
wall = WALL()


def main():
    while True:
        screen.fill(COLOR.BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if world.game_active:             
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
                # Press SPACE to restart
                if event.key == pygame.K_SPACE and world.game_active is False:
                    world.restart()
            # To create list of apple
            if event.type == spawn_apple:
                apple.list_apple.append(apple.create_apple())

        # Draw wall around 
        wall.draw()

        if world.game_active:
            # Find snake direction
            snake.x, snake.y = snake.change_direction()
       
            # Draw snake
            snake.draw(snake.x, snake.y)

            # Draw apple
            apple.draw(apple.list_apple)

            # Check collision
            if apple.rect.colliderect(snake.rect):
                print('Touched')
            # Check if the snake hit the wall, game over
            world.game_active = snake.hit_wall()

        pygame.display.update()
        world.clock.tick(world.fps_number)


if __name__ == "__main__":
    main()
        