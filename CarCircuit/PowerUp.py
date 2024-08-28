import pygame
import random
import math

class PowerUp:
    def __init__(self, type, duration, position, radius=20):
        self.type = type
        self.duration = duration
        self.radius = radius
        self.x, self.y = position
        self.collected = False
        self.spawn_time = pygame.time.get_ticks()
        self.active = False
        self.image = None
        self.effect_active = False
        self.effect_start_time = 0

    def set_image(self, image):
    self.image = image

    def draw(self, window):
        if not self.collected and self.image:
            rect = self.image.get_rect(center=(self.x, self.y))
            window.blit(self.image, rect.topleft)

    def collect(self, player):
        if self.is_colliding(player):
            self.collected = True
            self.effect_start_time = pygame.time.get_ticks()
            self.apply_effect(player)

    def is_colliding(self, player):
        distance = math.hypot(self.x - player.x, self.y - player.y)
        return distance < self.radius + player.image.get_width() / 2

    def apply_effect(self, player):
        if self.type == "speed":
            player.max_speed *= 1.5
        elif self.type == "invincibility":
            player.invincible = True
        elif self.type == "health":
            player.health = min(player.health + 20, player.max_health)

        self.active = True
        self.effect_active = True

    def update(self, player):
        if self.effect_active and (pygame.time.get_ticks() - self.effect_start_time) > self.duration * 1000:
            self.remove_effect(player)

    def remove_effect(self, player):
        if self.type == "speed":
            player.max_speed /= 1.5
        elif self.type == "invincibility":
            player.invincible = False

        self.effect_active = False
        self.active = False

    def respawn(self, new_position=None):
        self.collected = False
        self.active = False
        self.spawn_time = pygame.time.get_ticks()
        self.x, self.y = new_position if new_position else self.random_position()

    def random_position(self):
        width, height = pygame.display.get_surface().get_size()
        return random.randint(0, width), random.randint(0, height)

    def is_active(self):
        return self.active

def time_since_spawn(self):
    return (pygame.time.get_ticks() - self.spawn_time) / 1000

def auto_despawn(self, max_time):
    if self.time_since_spawn() > max_time:
        self.collected = True
        self.active = False

