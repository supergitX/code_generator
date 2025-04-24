import pygame
import random

pygame.init()

# Screen dimensions
width = 600
height = 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Floppy Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)

# Bird properties
bird_x = 100
bird_y = height // 2
bird_radius = 20
bird_velocity = 0
gravity = 0.5
flap_strength = -10

# Pipe properties
pipe_width = 80
pipe_gap = 200
pipe_velocity = 5
pipes = []

# Score
score = 0
font = pygame.font.Font(None, 50)

# Game states
game_over = False

def create_pipe():
    pipe_height = random.randint(100, height - 100 - pipe_gap)
    return {
        "top": {"x": width, "y": 0, "width": pipe_width, "height": pipe_height},
        "bottom": {"x": width, "y": pipe_height + pipe_gap, "width": pipe_width, "height": height - pipe_height - pipe_gap},
    }

def move_pipes():
    for pipe in pipes:
        pipe["top"]["x"] -= pipe_velocity
        pipe["bottom"]["x"] -= pipe_velocity

def draw_pipes():
    for pipe in pipes:
        pygame.draw.rect(screen, green, (pipe["top"]["x"], pipe["top"]["y"], pipe["top"]["width"], pipe["top"]["height"]))
        pygame.draw.rect(screen, green, (pipe["bottom"]["x"], pipe["bottom"]["y"], pipe["bottom"]["width"], pipe["bottom"]["height"]))

def check_collision():
    global game_over
    if bird_y < 0 or bird_y > height:
        game_over = True
        return

    for pipe in pipes:
        if bird_x + bird_radius > pipe["top"]["x"] and bird_x - bird_radius < pipe["top"]["x"] + pipe["top"]["width"]:
            if bird_y - bird_radius < pipe["top"]["height"] or bird_y + bird_radius > pipe["bottom"]["y"]:
                game_over = True
                return

def draw_score():
    text = font.render("Score: " + str(score), True, black)
    screen.blit(text, (10, 10))

def reset_game():
    global bird_y, bird_velocity, pipes, score, game_over
    bird_y = height // 2
    bird_velocity = 0
    pipes = []
    score = 0
    game_over = False

# Game loop
running = True
clock = pygame.time.Clock()
pipe_spawn_time = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_velocity = flap_strength
            if event.key == pygame.K_SPACE and game_over:
                reset_game()


    if not game_over:
        # Bird movement
        bird_velocity += gravity
        bird_y += bird_velocity

        # Pipe generation
        if pygame.time.get_ticks() - pipe_spawn_time > 1500:
            pipes.append(create_pipe())
            pipe_spawn_time = pygame.time.get_ticks()

        # Pipe movement
        move_pipes()

        # Collision detection
        check_collision()

        # Score increment
        for pipe in pipes:
            if pipe["top"]["x"] + pipe["top"]["width"] < bird_x and not pipe.get("passed", False):
                score += 1
                pipe["passed"] = True

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe["top"]["x"] > -pipe_width]


    # Drawing
    screen.fill(white)
    pygame.draw.circle(screen, black, (bird_x, int(bird_y)), bird_radius)
    draw_pipes()
    draw_score()

    if game_over:
        game_over_text = font.render("Game Over! Press SPACE to restart", True, black)
        text_rect = game_over_text.get_rect(center=(width // 2, height // 2))
        screen.blit(game_over_text, text_rect)

    pygame.display.update()
    clock.tick(60)

pygame.quit()