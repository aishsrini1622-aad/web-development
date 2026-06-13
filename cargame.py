import pygame
import random

# Initialize pygame
pygame.init()

# Screen size
WIDTH = 500
HEIGHT = 700

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (50, 50, 50)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game")

# Clock
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont(None, 40)

# Player car
car_width = 50
car_height = 100

player_x = WIDTH // 2 - car_width // 2
player_y = HEIGHT - 120

player_speed = 7

# Enemy car
enemy_width = 50
enemy_height = 100

enemy_x = random.randint(50, WIDTH - 100)
enemy_y = -100

enemy_speed = 6

# Score
score = 0

# Road lines
line_y = 0

# Game loop
running = True

while running:

    clock.tick(60)

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # Key controls
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= player_speed

    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Boundary check
    if player_x < 0:
        player_x = 0

    if player_x > WIDTH - car_width:
        player_x = WIDTH - car_width

    # Enemy movement
    enemy_y += enemy_speed

    # Respawn enemy
    if enemy_y > HEIGHT:

        enemy_y = -100
        enemy_x = random.randint(50, WIDTH - 100)

        score += 1

        # Increase difficulty
        enemy_speed += 0.2

    # Background
    screen.fill(GRAY)

    # Road lines animation
    line_y += 10

    if line_y > HEIGHT:
        line_y = 0

    for i in range(0, HEIGHT, 80):

        pygame.draw.rect(
            screen,
            WHITE,
            (WIDTH//2 - 5, i + line_y, 10, 40)
        )

    # Draw player car
    pygame.draw.rect(
        screen,
        BLUE,
        (player_x, player_y, car_width, car_height)
    )

    # Draw enemy car
    pygame.draw.rect(
        screen,
        RED,
        (enemy_x, enemy_y, enemy_width, enemy_height)
    )

    # Collision detection
    player_rect = pygame.Rect(
        player_x,
        player_y,
        car_width,
        car_height
    )

    enemy_rect = pygame.Rect(
        enemy_x,
        enemy_y,
        enemy_width,
        enemy_height
    )

    if player_rect.colliderect(enemy_rect):

        game_over = font.render(
            "GAME OVER",
            True,
            WHITE
        )

        screen.blit(
            game_over,
            (WIDTH//2 - 100, HEIGHT//2)
        )

        pygame.display.update()

        pygame.time.delay(3000)

        running = False

    # Score display
    score_text = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.update()

# Quit game
pygame.quit()
