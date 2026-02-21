import pygame
import random
import sys

pygame.init()

# ================= SCREEN =================
WIDTH = 600
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird game New Edition by ARYAN")

clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 32)

# ================= IMAGES =================
bg_img = pygame.image.load("bg.png").convert()
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

bird_img = pygame.image.load("bird.png").convert_alpha()
bird_img = pygame.transform.scale(bird_img, (40, 30))

enemy_img = pygame.transform.flip(bird_img, True, False)

tree_img = pygame.image.load("tree.png").convert_alpha()
tree_img = pygame.transform.scale(tree_img, (80, 160))

wire_img = pygame.image.load("wire.png").convert_alpha()
wire_img = pygame.transform.scale(wire_img, (WIDTH, 25))

# ================= PLAYER BIRD =================
bird_x = 100
bird_y = HEIGHT // 2
bird_vel = 0
gravity = 0.5
jump_power = -8

# ================= GAME SPEED =================
speed = 4

# ================= TREES (MULTIPLE) =================
trees = []
for i in range(2):
    x = WIDTH + i * 300
    y = HEIGHT - 160
    trees.append(pygame.Rect(x, y, 80, 160))

# ================= ENEMY BIRDS =================
enemies = []

def spawn_enemy():
    x = WIDTH + random.randint(200, 400)
    y = random.randint(50, HEIGHT - 100)
    enemies.append(pygame.Rect(x, y, 40, 30))

enemy_timer = 0

# ================= WIRE =================
wire_x = 0
wire_y = 0

# ================= SCORE =================
score = 0

def draw_text(text, x, y):
    img = FONT.render(text, True, (255, 255, 255))
    screen.blit(img, (x, y))

def reset_game():
    global bird_y, bird_vel, score, speed, trees, enemies
    bird_y = HEIGHT // 2
    bird_vel = 0
    score = 0
    speed = 4
    enemies.clear()
    trees.clear()
    for i in range(2):
        trees.append(pygame.Rect(WIDTH + i * 300, HEIGHT - 160, 80, 160))

# ================= GAME LOOP =================
while True:
    screen.blit(bg_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_vel = jump_power

    # -------- Bird Physics --------
    bird_vel += gravity
    bird_y += bird_vel

    bird_rect = pygame.Rect(bird_x, bird_y, 40, 30)

    # -------- Move Trees --------
    for tree in trees:
        tree.x -= speed
        if tree.x < -80:
            tree.x = WIDTH + random.randint(200, 300)
            score += 1
            speed += 0.1  # game gets harder

    # -------- Enemy Birds --------
    enemy_timer += 1
    if enemy_timer > 120:
        spawn_enemy()
        enemy_timer = 0

    for enemy in enemies[:]:
        enemy.x -= speed + 1
        if enemy.x < -40:
            enemies.remove(enemy)

    # -------- Wire --------
    wire_x -= speed
    if wire_x <= -WIDTH:
        wire_x = 0

    wire_rect = pygame.Rect(0, 0, WIDTH, 25)

    # -------- Collisions --------
    if bird_rect.colliderect(wire_rect):
        reset_game()

    for tree in trees:
        if bird_rect.colliderect(tree):
            reset_game()

    for enemy in enemies:
        if bird_rect.colliderect(enemy):
            reset_game()

    if bird_y < 0 or bird_y > HEIGHT:
        reset_game()

    # -------- Draw --------
    # Trees
    for tree in trees:
        screen.blit(tree_img, tree.topleft)

    # Enemies
    for enemy in enemies:
        screen.blit(enemy_img, enemy.topleft)

    # Continuous wire
    screen.blit(wire_img, (wire_x, wire_y))
    screen.blit(wire_img, (wire_x + WIDTH, wire_y))

    # Player bird
    screen.blit(bird_img, (bird_x, bird_y))

    draw_text(f"Score: {score}", 10, 10)

    pygame.display.update()
    clock.tick(60) 
