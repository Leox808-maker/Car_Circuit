import pygame
import sys
from utils import blit_text_center

class UnlockCarsScreen:
    def __init__(self, win, width, height, cars, player_data):
        self.win = win
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("comicsans", 36)
        self.small_font = pygame.font.SysFont("comicsans", 28)
        self.cars = cars  # List of cars with unlock requirements
        self.player_data = player_data  # Player progress data (points, levels, etc.)
        self.current_car_index = 0
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        unlock_button = Button("Unlock", self.font, (self.width // 2 - 150, self.height - 100, 300, 50),
                               (0, 128, 0), (0, 255, 0), action=self.unlock_car)
        back_button = Button("Back to Menu", self.font, (self.width // 2 - 150, self.height - 50, 300, 50),
                             (128, 0, 0), (255, 0, 0), action=self.go_back_to_menu)
        self.buttons.append(unlock_button)
        self.buttons.append(back_button)

    def unlock_car(self):
        car = self.cars[self.current_car_index]
        if self.player_data['points'] >= car['unlock_points']:
            if car['name'] not in self.player_data['unlocked_cars']:
                self.player_data['unlocked_cars'].append(car['name'])
                self.player_data['points'] -= car['unlock_points']

    def go_back_to_menu(self):
        self.player_data['screen'] = 'menu'

    def draw_unlock_screen(self):
        self.win.fill((0, 0, 0))
        blit_text_center(self.win, self.font, "Unlock New Cars")

        car = self.cars[self.current_car_index]
        car_text = f"Car: {car['name']}"
        points_text = f"Unlock Points: {car['unlock_points']}"
        unlocked_text = "Unlocked!" if car['name'] in self.player_data['unlocked_cars'] else "Locked"

        self.draw_text(car_text, (255, 255, 255), (self.width // 2, self.height // 2 - 120))
        self.draw_text(points_text, (255, 255, 255), (self.width // 2, self.height // 2 - 60))
        self.draw_text(unlocked_text, (255, 255, 255), (self.width // 2, self.height // 2))

        instruction_text = "Use Left/Right to change car"
        self.draw_text(instruction_text, (255, 255, 255), (self.width // 2, self.height // 2 + 120), font=self.small_font)

        for button in self.buttons:
            button.draw(self.win)

        pygame.display.update()

    def draw_text(self, text, color, position, font=None):
        if font is None:
            font = self.font
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=position)
        self.win.blit(text_surf, text_rect)


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    button.check_hover(pos)

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.click()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.current_car_index = (self.current_car_index - 1) % len(self.cars)
                if event.key == pygame.K_RIGHT:
                    self.current_car_index = (self.current_car_index + 1) % len(self.cars)

    def run(self):
        while self.player_data['screen'] == 'unlock_cars':
            self.handle_events()
            self.draw_unlock_screen()