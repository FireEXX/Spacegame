import pygame
from player import player
from enemy import enemy
from highscore import highscore

pygame.init()

width, height = 800, 600
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invader")
clock = pygame.time.Clock()
timer = highscore()

space_image = pygame.image.load('space.png')
space_image = pygame.transform.scale(space_image, (width, height))
hit_sound = pygame.mixer.Sound("hit_sound.mp3")

font = pygame.font.SysFont(None, 55)
small_font = pygame.font.SysFont(None, 18)
health_font = pygame.font.SysFont(None, 30)

menu_options = ["Start Game", "Quit"]

def draw_menu(selected_option):
    screen.fill(black)
    title_text = font.render("Space Invader", True, white)
    creators_text = small_font.render("Created By Khristian Hamilton, Demetrice Alexander, Harsh Findoliya", True, white)

    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 4 - 50))
    screen.blit(creators_text, (width // 2 - creators_text.get_width() // 2, height // 4))

    for i, option in enumerate(menu_options):
        color = (255, 0, 0) if i == selected_option else white
        text = font.render(option, True, color)
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 + i * 60))

    pygame.display.flip()

def show_menu():
    selected_option = 0
    while True:
        draw_menu(selected_option)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        return  # Start Game
                    elif selected_option == 1:
                        pygame.quit()

# Show menu first
show_menu()

# Setup game objects
player = player(0, height // 2 - 25)
enemy = enemy(width - 50, height // 2 - 100, width)

# Game loop
running = True
while running:
    screen.fill(black)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(space_image, (0, 0))
    current_time = pygame.time.get_ticks()


    player.update(keys, current_time, height)
    enemy.update(current_time, height, player.rect)

    if player.handle_lasers(enemy.rect, width):
        enemy.health -= 1
        hit_sound.play()
    if enemy.handle_lasers(player.rect):
        player.health -= 1
        hit_sound.play()


    player.draw(screen)
    enemy.draw(screen)

    screen.blit(health_font.render(f"player hp: {player.health}", True, white), (10, 10))
    screen.blit(health_font.render(f"enemy hp: {enemy.health}", True, white), (width - 150, 10))

    # Win/Loss
    if player.health <= 0:
        screen.blit(health_font.render("Enemy wins!", True, (255, 0, 0)), (width // 2 - 60, height // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        break

    if enemy.health <= 0:
        time = timer.stop()
        timer.save_highscore()
        final_time = timer.load_highscore()
        win_text = f"Player wins! Time: {time}s"
        if final_time is not None:
            win_text += f" | Best: {final_time}s"
        screen.blit(health_font.render(win_text, True, (0, 0, 255)), (width // 2 - 170, height // 2))
        pygame.display.flip()
        pygame.time.delay(5000)
        break

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

