import pygame
import random
import csv

# Initialize pygame
pygame.init()

# Screen size
WIDTH = 600
HEIGHT = 400

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock
clock = pygame.time.Clock()

# Snake settings
snake_block = 10
snake_speed = 15

font = pygame.font.SysFont(None, 35)

# Display score
def show_score(score):
    value = font.render(
        "Score: " + str(score),
        True,
        WHITE
    )
    screen.blit(value, [10, 10])

# Draw snake
def draw_snake(block, snake_list):
    for x in snake_list:
        pygame.draw.rect(
            screen,
            GREEN,
            [x[0], x[1], block, block]
        )

# Save score to CSV
def save_score(score):

    with open(
        'scores.csv',
        mode='a',
        newline=''
    ) as file:

        writer = csv.writer(file)
        writer.writerow([score])

# Game loop
def game_loop():

    game_over = False

    x = WIDTH / 2
    y = HEIGHT / 2

    x_change = 0
    y_change = 0

    snake_list = []
    snake_length = 1

    food_x = round(
        random.randrange(0, WIDTH - snake_block)
        / 10.0
    ) * 10.0

    food_y = round(
        random.randrange(0, HEIGHT - snake_block)
        / 10.0
    ) * 10.0

    while not game_over:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    x_change = -snake_block
                    y_change = 0

                elif event.key == pygame.K_RIGHT:
                    x_change = snake_block
                    y_change = 0

                elif event.key == pygame.K_UP:
                    y_change = -snake_block
                    x_change = 0

                elif event.key == pygame.K_DOWN:
                    y_change = snake_block
                    x_change = 0

        x += x_change
        y += y_change

        # Game over conditions
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_over = True

        screen.fill(BLACK)

        pygame.draw.rect(
            screen,
            RED,
            [food_x, food_y, snake_block, snake_block]
        )

        snake_head = []
        snake_head.append(x)
        snake_head.append(y)

        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        # Snake collision
        for block in snake_list[:-1]:
            if block == snake_head:
                game_over = True

        draw_snake(
            snake_block,
            snake_list
        )

        show_score(snake_length - 1)

        pygame.display.update()

        # Food collision
        if x == food_x and y == food_y:

            food_x = round(
                random.randrange(
                    0,
                    WIDTH - snake_block
                ) / 10.0
            ) * 10.0

            food_y = round(
                random.randrange(
                    0,
                    HEIGHT - snake_block
                ) / 10.0
            ) * 10.0

            snake_length += 1

        clock.tick(snake_speed)

    # Save final score
    save_score(snake_length - 1)

    pygame.quit()

# Run game
game_loop()
