import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

# ================= WINDOW =================
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game")

clock = pygame.time.Clock()

# ================= LOAD IMAGES =================
car_img = pygame.image.load("assets/car.png").convert_alpha()
enemy_img = pygame.image.load("assets/enemy.png").convert_alpha()

car = pygame.transform.scale(car_img, (50, 90))
enemy = pygame.transform.scale(enemy_img, (50, 90))

car_w, car_h = car.get_size()

# ================= MASKS (PIXEL PERFECT) =================
car_mask = pygame.mask.from_surface(car)
enemy_mask = pygame.mask.from_surface(enemy)

# ================= LOAD SOUNDS =================
engine_sound = pygame.mixer.Sound("assets/engine.wav")
crash_sound = pygame.mixer.Sound("assets/crash.wav")

engine_sound.set_volume(0.4)
crash_sound.set_volume(0.8)

engine_sound.play(-1)   # loop engine sound

# ================= ROAD =================
road_x = 100
road_width = 200
road_y = 0
road_speed = 5

# ================= PLAYER =================
car_x = WIDTH // 2 - car_w // 2
car_y = HEIGHT - car_h - 20
car_speed = 6

# ================= ENEMY =================
lanes = [
    road_x + 30,
    road_x + road_width - car_w - 30
]
enemy_x = random.choice(lanes)
enemy_y = -150
enemy_speed = 5

# ================= SCORE & LEVEL =================
score = 0
level = 1
font = pygame.font.SysFont(None, 32)
big_font = pygame.font.SysFont(None, 48)

game_over = False

# ================= GAME LOOP =================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                score = 0
                level = 1
                enemy_speed = 5
                road_speed = 5
                enemy_y = -150
                enemy_x = random.choice(lanes)
                car_x = WIDTH // 2 - car_w // 2
                game_over = False
                engine_sound.play(-1)

    if not game_over:
        # ================= INPUT =================
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_x > road_x:
            car_x -= car_speed
        if keys[pygame.K_RIGHT] and car_x < road_x + road_width - car_w:
            car_x += car_speed

        # ================= ROAD MOVE =================
        road_y += road_speed
        if road_y >= 40:
            road_y = 0

        # ================= ENEMY MOVE =================
        enemy_y += enemy_speed
        if enemy_y > HEIGHT:
            enemy_y = -150
            enemy_x = random.choice(lanes)
            score += 1

            # LEVEL UP every 5 points
            if score % 5 == 0:
                level += 1
                enemy_speed += 1
                road_speed += 0.7

        # ================= MASK COLLISION =================
        offset = (enemy_x - car_x, enemy_y - car_y)
        if car_mask.overlap(enemy_mask, offset):
            game_over = True
            engine_sound.stop()
            crash_sound.play()

    # ================= DRAW =================
    screen.fill((0, 150, 0))

    pygame.draw.rect(screen, (50, 50, 50), (road_x, 0, road_width, HEIGHT))

    for i in range(0, HEIGHT, 40):
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (road_x + road_width // 2 - 5, i + road_y, 10, 20)
        )

    screen.blit(car, (car_x, car_y))
    screen.blit(enemy, (enemy_x, enemy_y))

    # ================= UI =================
    screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10, 10))
    screen.blit(font.render(f"Level: {level}", True, (255,255,255)), (10, 40))

    if game_over:
        over = big_font.render("GAME OVER", True, (255, 0, 0))
        restart = font.render("Press R to Restart", True, (255,255,255))
        screen.blit(over, (WIDTH//2 - 120, HEIGHT//2 - 40))
        screen.blit(restart, (WIDTH//2 - 140, HEIGHT//2 + 10))

    pygame.display.update()
    clock.tick(60)