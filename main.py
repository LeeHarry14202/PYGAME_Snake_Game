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

    def reset(self):

        world.direction = 'RIGHT'
        world.game_active = True

        apple.list_apple.clear()

        snake.x = SCREEN_WIDTH / 2
        snake.y = SCREEN_HEIGHT / 2
        snake.len_list_snake = 0
        snake.list_snake = [[SCREEN_WIDTH/2, SCREEN_HEIGHT/2]]

        score.score_ = 0
        score.start_time = 100

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


class SCORE(object):
    def __init__(self):
        self.score_ = 0
        self.high_score = 0
        self.start_time = 100

    def display_score(self):
        if score.start_time != 0:
            world.display_text('YOU HIT THE WALL!', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            score.start_time -= 1
        else:
            world.display_text('Your score: ' + str(self.score_), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
            world.display_text('Press SPACE to play again', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.5)
            world.display_text('Press ESC to exit', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)        
            world.display_text('High score: ' + str(self.high_score), SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100)

    def update_high_score(self):
        if self.high_score < self.score_:
            self.high_score = self.score_


class SNAKE(object):
    def __init__(self):
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.WIDTH = 20
        self.HEIGHT = 20
        self.speed = 3
        self.list_snake = [[self.x, self.y]]
        self.len_list_snake = 0
        self.rect = pygame.rect.Rect((self.x, self.y, self.WIDTH, self.HEIGHT))
    
    def draw(self):
        # Press to change snake direction
        self.change_direction()

        self.add_to_list_snake()

        for snake_ in self.list_snake:
            self.x = snake_[0]
            self.y = snake_[1]
            pygame.draw.rect(screen, COLOR.WHITE, [self.x, self.y, self.WIDTH, self.HEIGHT])

    def change_direction(self):
        x_change = 0
        y_change = 0
        if world.direction == 'RIGHT':     
            x_change = self.speed
            y_change = 0
        elif world.direction == 'LEFT':
            x_change = - self.speed
            y_change = 0
        elif world.direction == 'UP':
            x_change = 0
            y_change = - self.speed
        elif world.direction == 'DOWN':
            x_change = 0
            y_change = self.speed
        self.x += x_change
        self.y += y_change
        # return x, y

    def add_to_list_snake(self):
        head = []
        head.append(snake.x)
        head.append(snake.y)
        snake.list_snake.append(head)
        if len(snake.list_snake) > snake.len_list_snake:
            del snake.list_snake[0]

    def hit_wall(self):
        if self.x > SCREEN_WIDTH:
            world.game_active = False
        elif self.x < 0:
            world.game_active = False
        elif self.y < 0:
            world.game_active = False
        elif self.y > SCREEN_HEIGHT:
            world.game_active = False

    def check_collision(self):
        for snake_ in snake.list_snake:
            snake_rect = pygame.rect.Rect((snake_[0], snake_[1], self.WIDTH, self.HEIGHT))
            if snake_rect.colliderect(apple.rect):
                score.score_ += 1 


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

# # # Set timer for 
spawn_snake = pygame.USEREVENT + 1
spawn_snake_time = 1000
pygame.time.set_timer(spawn_snake, spawn_snake_time)

# Object init
world = WORLD()
snake = SNAKE()
apple = APPLE()
wall = WALL()
score = SCORE()


def main():
    running = True
    # x_change = 0
    # y_change = 0
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
                        world.reset()
                    # Press Esc to exit
                    if event.key == pygame.K_ESCAPE:
                        running = False
            # To create list of apple
            if event.type == spawn_apple:
                apple.list_apple.append(apple.create_apple())
            if event.type == spawn_snake and world.game_active:
                snake.len_list_snake += 1

        # Draw wall around 
        wall.draw()

        if world.game_active:

            # Draw snake
            snake.draw()

            # Draw apple
            apple.draw(apple.list_apple)

            # Check collision
            snake.check_collision()

            # Check if the snake hit the wall, game over
            snake.hit_wall()
        else:
            score.update_high_score()
            score.display_score()

        pygame.display.update()
        world.clock.tick(world.fps_number)


if __name__ == "__main__":
    main()
        