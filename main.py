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
        self.high_score = 0

    def restart(self):
        world.game_active = True
        apple.list_apple.clear()
        snake.x = SCREEN_WIDTH / 2
        snake.y = SCREEN_HEIGHT / 2
        world.direction = 'RIGHT'
        world.score = 0

    def display_text(self, text, x, y):
        # creating font object my_font
        my_font = pygame.font.SysFont('times new roman', 25)

        # creating a text surface on which text
        # will be drawn
        game_over_surface = my_font.render(text, True, COLOR.WHITE)

        # create a rectangular object for the text
        # surface object
        game_over_rect = game_over_surface.get_rect()

        # setting position of the text
        game_over_rect.midtop = (x, y)

        # blit wil draw the text on screen
        screen.blit(game_over_surface, game_over_rect)

    def display_score(self):
        self.display_text('Your score: ' + str(world.score), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        self.display_text('Press SPACE to play again', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.5)
        self.display_text('Press ESC to exit', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)        
        self.display_text('High score: ' + str(self.high_score), SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100)

    def update_high_score(self):
        if self.high_score < self.score:
            self.high_score = self.score


class SNAKE(object):
    def __init__(self):
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.WIDTH = 15
        self.HEIGHT = 15
        self.speed = 3
        self.list_snake = []
        self.position = [self.x, self.y]
        self.rect = pygame.rect.Rect((self.x, self.y, self.WIDTH, self.HEIGHT))

    def draw(self):
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
            world.game_active = False
        elif self.x < 0:
            world.game_active = False
        if self.y < 0:
            world.game_active = False
        elif self.y > SCREEN_HEIGHT:
            world.game_active = False
        return world.game_active


class APPLE(object):
    def __init__(self):
        self.WIDTH = 15
        self.HEIGHT = 15
        self.radius = 10
        self.list_apple = []
        self.rect = pygame.rect.Rect((-SCREEN_WIDTH/2, -SCREEN_HEIGHT/2, self.WIDTH, self.HEIGHT))
        self.position = [-SCREEN_WIDTH/2, -SCREEN_HEIGHT/2]

    def create_apple(self):
        random_x_pos = random.randint(20, SCREEN_WIDTH - snake.WIDTH)
        random_y_pos = random.randint(20, SCREEN_HEIGHT - snake.HEIGHT)
        x = random_x_pos
        y = random_y_pos
        self.position = [x, y]
        # Update apple rect
        self.rect = pygame.rect.Rect((x, y, self.WIDTH, self.HEIGHT))
        return self.position

    def draw(self, list_apple):
        for apple_ in list_apple:
            pygame.draw.circle(screen, COLOR.RED, apple_, self.radius)
            # pygame.draw.rect(screen, COLOR.RED, self.rect)

        # If don't have this, the previous apple wont' disappear
        if len(list_apple) > 1:
            list_apple.pop(0)


class WALL(object):
    def __init__(self):
        self.list_wall = []

    def draw(self):
        wall_1 = pygame.rect.Rect(0, 0, SCREEN_WIDTH, 10)
        wall_2 = pygame.rect.Rect(0, 0, 10, SCREEN_HEIGHT)
        wall_3 = pygame.rect.Rect(SCREEN_WIDTH - 10, 0, 10, SCREEN_HEIGHT)
        wall_4 = pygame.rect.Rect(0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 10)
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
    running = True
    while running:
        screen.fill(COLOR.BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if world.game_active:             
                    if event.key == pygame.K_RIGHT:
                        world.direction = 'RIGHT'
                    if event.key == pygame.K_LEFT:
                        world.direction = 'LEFT'
                    if event.key == pygame.K_DOWN:
                        world.direction = 'DOWN'
                    if event.key == pygame.K_UP:
                        world.direction = 'UP'
                else:
                    # Press SPACE to restart
                    if event.key == pygame.K_SPACE:
                        world.restart()
                    # Press Esc to exit
                    if event.key == pygame.K_ESCAPE:
                        running = False
            # To create list of apple
            if event.type == spawn_apple:
                apple.list_apple.append(apple.create_apple())

        # Draw wall around 
        wall.draw()

        if world.game_active:
            # Find snake direction
            snake.x, snake.y = snake.change_direction()
       
            # Draw snake
            snake.draw()

            # Draw apple
            apple.draw(apple.list_apple)

            # Check collision
            if apple.rect.colliderect(snake.rect):
                world.score += 1

            # Check if the snake hit the wall, game over
            world.game_active = snake.hit_wall()
        else:
            world.update_high_score()
            world.display_score()

        pygame.display.update()
        world.clock.tick(world.fps_number)


if __name__ == "__main__":
    main()
        