import pygame
import random

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500


class COLOR:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)


class SNAKE:
    def __init__(self):
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.WIDTH = 20
        self.HEIGHT = 20
        self.len_list_snake = 0
        self.list_snake = [[self.x, self.y]]
        self.VELOCITY = 5
        self.direction = 'RIGHT'
        self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def draw(self, screen):
        self.change_direction()
        self.add_to_list_snake()
        for snake in self.list_snake:
            self.x = snake[0]
            self.y = snake[1]
            self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
            pygame.draw.rect(screen, COLOR.WHITE, self.rect)

    def add_to_list_snake(self):
        head = []
        head.append(self.x)
        head.append(self.y)
        self.list_snake.append(head)
        if len(self.list_snake) > self.len_list_snake:
            del self.list_snake[0]

    def change_direction(self):
        if self.direction == 'RIGHT':
            self.x += self.VELOCITY
        if self.direction == 'LEFT':
            self.x -= self.VELOCITY
        if self.direction == 'DOWN':
            self.y += self.VELOCITY
        if self.direction == 'UP':
            self.y -= self.VELOCITY
        self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def hit_wall(self, game_status):
        if self.x > SCREEN_WIDTH:
            game_status = False
        elif self.x < 0:
            game_status = False
        elif self.y < 0:
            game_status = False
        elif self.y > SCREEN_HEIGHT:
            game_status = False
        return game_status

    def check_collision(self, apple, score):
        if apple.rect.colliderect(self.rect):
            score.current_score += 1


class APPLE:
    def __init__(self):
        self.x = -SCREEN_WIDTH / 2
        self.y = -SCREEN_HEIGHT / 2
        self.RADIUS = 10
        self.list_apple = []
        self.rect = pygame.Rect(self.x, self.y, self.RADIUS*2, self.RADIUS*2)

    def create_apple(self):
        random_x_pos = round(random.randint(20, SCREEN_WIDTH - 20) / 10.0) * 10.0
        random_y_pos = round(random.randint(20, SCREEN_HEIGHT - 20) / 10.0) * 10.0
        self.x = random_x_pos
        self.y = random_y_pos
        position_of_apple = [self.x, self.y]
        return position_of_apple

    def draw(self, screen):
        for apple in self.list_apple:
            self.x = apple[0]
            self.y = apple[1]
            self.rect = pygame.Rect(self.x, self.y, self.RADIUS*2, self.RADIUS*2)
            pygame.draw.circle(screen, COLOR.RED, (self.x, self.y), self.RADIUS)
        # If don't have this, the previous apple wont' disappear
        if len(self.list_apple) > 1:
            self.list_apple.pop(0)


class WALL:
    def __init__(self):
        self.BORDER = 10

    def draw(self, screen):
        wall_1 = pygame.rect.Rect(0, 0, SCREEN_WIDTH, self.BORDER)
        wall_2 = pygame.rect.Rect(0, 0, self.BORDER, SCREEN_HEIGHT)
        wall_3 = pygame.rect.Rect(SCREEN_WIDTH - self.BORDER, 0, self.BORDER, SCREEN_HEIGHT)
        wall_4 = pygame.rect.Rect(0, SCREEN_HEIGHT - self.BORDER, SCREEN_WIDTH, self.BORDER)
        pygame.draw.rect(screen, COLOR.WHITE, wall_1)
        pygame.draw.rect(screen, COLOR.WHITE, wall_2)
        pygame.draw.rect(screen, COLOR.WHITE, wall_3)
        pygame.draw.rect(screen, COLOR.WHITE, wall_4)


def display_text(screen, text, x, y):
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


class SCORE:
    def __init__(self):
        self.current_score = 0
        self.high_score = 0
        self.start_time = 100

    def display_score(self, screen):
        # Display YOU HIT THE WALL for a while
        if self.start_time != 0:
            display_text(screen, 'YOU HIT THE WALL!', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            self.start_time -= 1
        else:
            display_text(screen, 'Your score: ' + str(self.current_score), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
            display_text(screen, 'Press SPACE to play again', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.5)
            display_text(screen, 'Press ESC to exit', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            display_text(screen, 'High score: ' + str(self.high_score), SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100)

    def update_high_score(self):
        if self.high_score < self.current_score:
            self.high_score = self.current_score


def game_restart(snake, apple, score):
    apple.list_apple.clear()

    snake.direction = 'RIGHT'
    snake.x = SCREEN_WIDTH / 2
    snake.y = SCREEN_HEIGHT / 2
    snake.len_list_snake = 0
    snake.list_snake = [[SCREEN_WIDTH/2, SCREEN_HEIGHT/2]]

    score.current_score = 0
    score.start_time = 100
