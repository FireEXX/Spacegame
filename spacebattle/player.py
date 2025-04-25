import pygame

class player:
    def __init__(self, x, y):
        original_image = pygame.image.load("player_ship.png").convert_alpha()
        original_image = pygame.transform.scale(original_image, (50, 50)) # scale
        self.image = pygame.transform.rotate(original_image, -90)  # rotation
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        base_laser_image = pygame.image.load("player_laser.png").convert_alpha()
        base_laser_image = pygame.transform.scale(base_laser_image, (10, 50))  # scale
        self.laser_image = pygame.transform.rotate(base_laser_image, -90)  # rotation
        self.lasers = [] # (surface, rect)
        self.speed = 5
        self.laser_speed = 10
        self.health = 3
        self.fire_delay = 300
        self.last_shot = 0
        self.shoot_sound = pygame.mixer.Sound("laser_shoot.mp3")

    def update(self, keys, current_time, height):
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.top > 0:
            self.rect.y -= self.speed
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.bottom < height:
            self.rect.y += self.speed

        if keys[pygame.K_SPACE] and current_time - self.last_shot >= self.fire_delay:
            laser_rect = self.laser_image.get_rect()
            # laser pos
            laser_rect.x = self.rect.x
            laser_rect.y = self.rect.y + (self.rect.height // 2) - (laser_rect.height // 2)
            self.shoot_sound.play()

            self.lasers.append((self.laser_image, laser_rect))
            self.last_shot = current_time

    def handle_lasers(self, enemy_rect, screen_width):
        i = 0
        while i < len(self.lasers):
            laser_surface, laser_rect = self.lasers[i]
            laser_rect.x += self.laser_speed
            if laser_rect.x > screen_width:
                del self.lasers[i]
            elif enemy_rect.colliderect(laser_rect):
                del self.lasers[i]
                return True
            else:
                i += 1
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for laser_surf, laser_rect in self.lasers:
            screen.blit(laser_surf, laser_rect)

