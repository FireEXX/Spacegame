import pygame
import random

class enemy:
    def __init__(self, x, y, screen_width):
        enemy_img = pygame.image.load("enemy_ship.png").convert_alpha()
        enemy_img = pygame.transform.scale(enemy_img, (50, 50))  # scale
        self.image = pygame.transform.rotate(enemy_img, 90)  # rotation
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        laser_img = pygame.image.load("enemy_laser.png").convert_alpha()
        laser_img = pygame.transform.scale(laser_img, (10, 50))  # scale
        self.laser_image = pygame.transform.rotate(laser_img, 90)  # rotation

        self.lasers = []
        self.speed = 3
        self.laser_speed = 10
        self.health = 3
        self.fire_delay = 1000
        self.last_shot = pygame.time.get_ticks()
        self.direction = random.choice([-self.speed, self.speed])
        self.last_direction_change = pygame.time.get_ticks()
        self.direction_change_delay = 200
        self.screen_width = screen_width

    def update(self, current_time, height, player_rect):
        if current_time - self.last_direction_change >= self.direction_change_delay:
            self.direction = random.choice([-self.speed, self.speed])
            self.last_direction_change = current_time

        self.rect.y += self.direction
        if self.rect.y <= 0:
            self.rect.y = 0
        elif self.rect.y + self.rect.height >= height:
            self.rect.y = height - self.rect.height

        if current_time - self.last_shot >= self.fire_delay:
            laser_rect = self.laser_image.get_rect()
            laser_rect.x = self.rect.x - laser_rect.width + 10 # spawn
            laser_rect.y = self.rect.y + (self.rect.height // 2) - (laser_rect.height // 2)
            self.lasers.append((self.laser_image, laser_rect))
            self.last_shot = current_time

    def handle_lasers(self, player_rect):
        for laser in self.lasers[:]:
            _, laser_rect = laser
            laser_rect.x -= self.laser_speed
            if laser_rect.x + laser_rect.width < 0:
                self.lasers.remove(laser)
            elif player_rect.colliderect(laser_rect):
                self.lasers.remove(laser)
                return True
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for laser_surf, laser_rect in self.lasers:
            screen.blit(laser_surf, laser_rect)
