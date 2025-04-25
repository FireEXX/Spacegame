import pygame


pygame.init()


width, height = 800, 600
black = (0, 0, 0)
white = (255, 255, 255)


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invader")


font = pygame.font.SysFont(None, 55)
small_font = pygame.font.SysFont(None, 18)


menu_options = ["Start Game", "Quit"]

def draw_menu(selected):
    screen.fill(black)


    title_text = font.render("Space Invader", True, white)
    creators_text = small_font.render("Created By Khristian Hamilton, Demetrice Alexander, Harsh Findoliya, Aydin Ayhan Rick Sanchez", True, white)

    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 4 - 50))
    screen.blit(creators_text, (width // 2 - creators_text.get_width() // 2, height // 4))


    for i, option in enumerate(menu_options):
        if i == selected:
            color = (255, 0, 0)
        else:
            color = white
        text = font.render(option, True, color)
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 + i * 60))

    pygame.display.flip()

def main():
    selected_option = 0
    while True:
        draw_menu(selected_option)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        print("Start Game selected")
                        # K. Hamilton can you add the game loop to be called here? This is where it should go under the elfif option i think?
                    elif selected_option == 1:
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    main()