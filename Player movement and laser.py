import pygame
import sys

pygame.init()

# constants
width, height = 800, 600
player_speed = 5
enemy_speed = 3
laser_speed = 10
enemy_fire_delay = 3000  # 3 seconds
player_fire_delay = 3000 # 3 seconds

# setup
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("laser battle")
clock = pygame.time.Clock()

# colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

# player and enemy
player = pygame.Rect(50, height // 2 - 25, 20, 50)
enemy = pygame.Rect(width - 70, height // 2 - 25, 20, 50)
player_lasers = []
enemy_lasers = []

player_health = 3
enemy_health = 5

last_enemy_fire = pygame.time.get_ticks()
player_last_shot = 0
enemy_direction = enemy_speed

# game loop
running = True
while running:
    screen.fill(black)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # time tracking
    current_time = pygame.time.get_ticks()

    # player movement
    if keys[pygame.K_w] and player.top > 0:
        player.y -= player_speed
    if keys[pygame.K_s] and player.bottom < height:
        player.y += player_speed

    # player shooting cooldown
    if keys[pygame.K_SPACE] and current_time - player_last_shot >= player_fire_delay:
        player_lasers.append(pygame.Rect(player.right, player.centery - 2, 10, 4))
        player_last_shot = current_time

    # enemy movement
    enemy.y += enemy_direction
    if enemy.top <= 0 or enemy.bottom >= height:
        enemy_direction *= -1  # bounce off top/bottom

    # enemy shooting cooldown
    if current_time - last_enemy_fire >= enemy_fire_delay:
        enemy_lasers.append(pygame.Rect(enemy.left - 10, enemy.centery - 2, 10, 4))
        last_enemy_fire = current_time

    # move player lasers
    for laser in player_lasers[:]:
        laser.x += laser_speed
        if laser.x > width:
            player_lasers.remove(laser)
        elif enemy.colliderect(laser):
            player_lasers.remove(laser)
            enemy_health -= 1

    # move enemy lasers
    for laser in enemy_lasers[:]:
        laser.x -= laser_speed
        if laser.x < 0:
            enemy_lasers.remove(laser)
        elif player.colliderect(laser):
            enemy_lasers.remove(laser)
            player_health -= 1

    # draw player and enemy
    pygame.draw.rect(screen, green, player)
    pygame.draw.rect(screen, red, enemy)

    # draw lasers
    for laser in player_lasers:
        pygame.draw.rect(screen, green, laser)
    for laser in enemy_lasers:
        pygame.draw.rect(screen, red, laser)

    # draw health
    font = pygame.font.SysFont(None, 30)
    screen.blit(font.render(f"player hp: {player_health}", True, white), (10, 10))
    screen.blit(font.render(f"enemy hp: {enemy_health}", True, white), (width - 150, 10))

    # check for win/loss
    if player_health <= 0:
        screen.blit(font.render("enemy wins!", True, red), (width // 2 - 60, height // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        break
    elif enemy_health <= 0:
        screen.blit(font.render("player wins!", True, green), (width // 2 - 60, height // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        break

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
