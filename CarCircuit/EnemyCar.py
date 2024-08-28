import pygame
import math
import random


class EnemyCar:
    def __init__(self, max_speed, rotation_speed, path=[]):
        self.image = None
        self.max_speed = max_speed
        self.rotation_speed = rotation_speed
        self.path = path
        self.current_point = 0
        self.speed = max_speed
        self.angle = 0
        self.x, self.y = self.path[0] if self.path else (0, 0)
        self.acceleration = 0.1
        self.avoid_obstacles = False
        self.obstacle_avoidance_distance = 50
        self.behavior_mode = "normal"
        self.switch_behavior_interval = 5000
        self.last_behavior_switch = pygame.time.get_ticks()

    def set_image(self, image):
        self.image = image

    def draw(self, window):

        if self.image:
            rotated_image = pygame.transform.rotate(self.image, self.angle)
            rect = rotated_image.get_rect(center=(self.x, self.y))
            window.blit(rotated_image, rect.topleft)

    def move(self):

        if self.current_point >= len(self.path):
            return

        self.calculate_angle()
        self.update_path_point()
        self.apply_behavior()

        radians = math.radians(self.angle)
        vertical_velocity = math.cos(radians) * self.speed
        horizontal_velocity = math.sin(radians) * self.speed

        self.y -= vertical_velocity
        self.x -= horizontal_velocity

    def calculate_angle(self):

        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_angle_radians = math.pi / 2
        else:
            desired_angle_radians = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_angle_radians += math.pi

        angle_difference = self.angle - math.degrees(desired_angle_radians)
        if angle_difference >= 180:
            angle_difference -= 360

        if angle_difference > 0:
            self.angle -= min(self.rotation_speed, abs(angle_difference))
        else:
            self.angle += min(self.rotation_speed, abs(angle_difference))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    def check_obstacles(self, obstacles):
        for obstacle in obstacles:
            dist = math.hypot(self.x - obstacle.x, self.y - obstacle.y)
            if dist < self.obstacle_avoidance_distance:
                self.avoid_obstacles = True
                self.evade_obstacle(obstacle)
                return
        self.avoid_obstacles = False

    def evade_obstacle(self, obstacle):
        angle_to_obstacle = math.atan2(obstacle.y - self.y, obstacle.x - self.x)

        self.angle = math.degrees(escape_angle)
        self.move()
