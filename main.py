import pygame
import sys
import My_Class

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))
clock = pygame.time.Clock()


# Set timer for apple
spawn_apple = pygame.USEREVENT
spawn_apple_time = 2000
pygame.time.set_timer(spawn_apple, spawn_apple_time)

# Set timer for snake length
spawn_snake = pygame.USEREVENT + 1
spawn_snake_time = 1000
pygame.time.set_timer(spawn_snake, spawn_snake_time)

# Object init
snake = My_Class.SNAKE()
apple = My_Class.APPLE()
wall = My_Class.WALL()
score = My_Class.SCORE()
running = True
while True:
    screen.fill(My_Class.COLOR.BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if running:
                if event.key == pygame.K_RIGHT:
                    snake.direction = 'RIGHT'
                if event.key == pygame.K_LEFT:
                    snake.direction = 'LEFT'
                if event.key == pygame.K_DOWN:
                    snake.direction = 'DOWN'
                if event.key == pygame.K_UP:
                    snake.direction = 'UP'
            else:
                if event.key == pygame.K_SPACE:
                    My_Class.game_restart(snake, apple, score)
                    running = True
                # Press Esc to exit
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == spawn_apple and running:
            apple.list_apple.append(apple.create_apple())
        if event.type == spawn_snake and running:
            snake.len_list_snake += 1

    if running:
        # Draw apple
        apple.draw(screen)

        # Draw snake
        snake.draw(screen)

        # Draw wall
        wall.draw(screen)

        # If snake hit the wall stop running
        running = snake.hit_wall(running)

        # Check collision
        snake.check_collision(apple, score)
    else:
        score.update_high_score()
        score.display_score(screen)

    pygame.display.update()
    clock.tick(90)
