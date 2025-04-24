import pygame
from player import player
from enemy import enemy
from highscore import highscore


pygame.init()

width, height = 800, 600
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
timer = highscore()


# Displaying health
font = pygame.font.SysFont(None, 30)

# player and enemy
player = player(0, height // 2 - 25)
enemy = enemy(width - 50, height // 2 - 100, width)

# game loop
running = True
while running:
    screen.fill(black)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = pygame.time.get_ticks()

    player.update(keys, current_time, height)
    enemy.update(current_time, height, player.rect)

    # lasers
    if player.handle_lasers(enemy.rect, width):
        enemy.health -= 1
    if enemy.handle_lasers(player.rect):
        player.health -= 1

    # draw player and enemy
    player.draw(screen)
    enemy.draw(screen)

    # display health
    screen.blit(font.render(f"player hp: {player.health}", True, white), (10, 10))
    screen.blit(font.render(f"enemy hp: {enemy.health}", True, white), (width - 150, 10))

    # win/loss conditions
    if player.health <= 0:
        screen.blit(font.render("enemy wins!", True, (255, 0, 0)), (width // 2 - 60, height // 2))
        pygame.display.flip()
        pygame.time.delay(2000)

        break
    if enemy.health <= 0:
        time = timer.stop()
        timer.save_highscore()
        highscore = timer.load_highscore()
        win_text = f"player wins! Time: {time:.2f}s"
        if highscore is not None:
            win_text += f" | Best: {highscore:.2f}s"
        screen.blit(font.render(win_text, True, (0, 255, 0)), (width // 2 - 150, height // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        break

    pygame.display.flip()
    clock.tick(60)
