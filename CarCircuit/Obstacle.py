import pygame
import random
import math
from utils import scale_image, blit_rotate_center

class Obstacle:
    def __init__(self, image_path, scale_factor, spawn_area, velocity_range):
        self.img = scale_image(pygame.image.load(image_path), scale_factor)
        self.width, self.height = self.img.get_width(), self.img.get_height()
        self.x, self.y = self.random_spawn(spawn_area)
        self.angle = random.randint(0, 360)
        self.velocity = random.uniform(*velocity_range)
        self.spawn_area = spawn_area
        self.rotation_speed = random.uniform(1, 3)
        self.active = True

    def random_spawn(self, spawn_area):
        spawn_x = random.randint(spawn_area[0][0], spawn_area[0][1])
        spawn_y = random.randint(spawn_area[1][0], spawn_area[1][1])
        return spawn_x, spawn_y

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.velocity
        horizontal = math.sin(radians) * self.velocity
        self.y += vertical
        self.x += horizontal

        if self.out_of_bounds():
            self.active = False

    def out_of_bounds(self):
        return (self.x < 0 or self.x > self.spawn_area[0][1] or
                self.y < 0 or self.y > self.spawn_area[1][1])

    def rotate(self):
        self.angle = (self.angle + self.rotation_speed) % 360

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def collide(self, mask, x=0, y=0):
        obstacle_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(obstacle_mask, offset)
        return poi

    def handle_collision(self, player_car):
        if self.collide(pygame.mask.from_surface(player_car.img), player_car.x, player_car.y):
            player_car.bounce()
            self.active = False

    def reset(self):
        self.x, self.y = self.random_spawn(self.spawn_area)
        self.angle = random.randint(0, 360)
        self.velocity = random.uniform(1, 5)
        self.active = True

class ObstacleManager:
    def __init__(self, spawn_interval, max_obstacles, obstacle_image, scale_factor, spawn_area, velocity_range):
        self.obstacles = []
        self.spawn_interval = spawn_interval
        self.max_obstacles = max_obstacles
        self.obstacle_image = obstacle_image
        self.scale_factor = scale_factor
        self.spawn_area = spawn_area
        self.velocity_range = velocity_range
        self.last_spawn_time = pygame.time.get_ticks()

    def spawn_obstacle(self):
        if len(self.obstacles) < self.max_obstacles:
            new_obstacle = Obstacle(self.obstacle_image, self.scale_factor, self.spawn_area, self.velocity_range)
            self.obstacles.append(new_obstacle)

    def update_obstacles(self, player_car):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_interval:
            self.spawn_obstacle()
            self.last_spawn_time = current_time

        for obstacle in self.obstacles:
            if obstacle.active:
                obstacle.move()
                obstacle.rotate()
                obstacle.handle_collision(player_car)
            else:
                self.obstacles.remove(obstacle)

    def draw_obstacles(self, win):
        for obstacle in self.obstacles:
            if obstacle.active:
                obstacle.draw(win)

    def reset(self):
        self.obstacles.clear()