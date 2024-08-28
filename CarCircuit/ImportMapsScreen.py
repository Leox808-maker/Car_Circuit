import pygame
import os
import sys
from utils import blit_text_center

class ImportMapsScreen:
    def __init__(self, win, width, height, map_directory, player_data):
        self.win = win
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("comicsans", 36)
        self.small_font = pygame.font.SysFont("comicsans", 28)
        self.map_directory = map_directory
        self.maps = self.get_maps()
        self.player_data = player_data
        self.current_map_index = 0
        self.buttons = []
        self.create_buttons()

    def get_maps(self):
        maps = [f for f in os.listdir(self.map_directory) if f.endswith('.png')]
        return maps

    def create_buttons(self):
        import_button = Button("Import", self.font, (self.width // 2 - 150, self.height - 100, 300, 50),
                               (0, 128, 0), (0, 255, 0), action=self.import_map)
        back_button = Button("Back to Menu", self.font, (self.width // 2 - 150, self.height - 50, 300, 50),
                             (128, 0, 0), (255, 0, 0), action=self.go_back_to_menu)
        self.buttons.append(import_button)
        self.buttons.append(back_button)

    def import_map(self):
        selected_map = self.maps[self.current_map_index]
        self.player_data['imported_maps'].append(selected_map)

    def go_back_to_menu(self):
        self.player_data['screen'] = 'menu'

    def draw_import_screen(self):
        self.win.fill((0, 0, 0))
        blit_text_center(self.win, self.font, "Import New Maps")

        if len(self.maps) == 0:
            self.draw_text("No maps available for import.", (255, 0, 0), (self.width // 2, self.height // 2))
        else:
            selected_map = self.maps[self.current_map_index]
            map_text = f"Map: {selected_map}"

            self.draw_text(map_text, (255, 255, 255), (self.width // 2, self.height // 2 - 60))
            instruction_text = "Use Left/Right to change map"
            self.draw_text(instruction_text, (255, 255, 255), (self.width // 2, self.height // 2 + 60), font=self.small_font)

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
                if event.key == pygame.K_LEFT and len(self.maps) > 0:
                    self.current_map_index = (self.current_map_index - 1) % len(self.maps)
                if event.key == pygame.K_RIGHT and len(self.maps) > 0:
                    self.current_map_index = (self.current_map_index + 1) % len(self.maps)

    def run(self):
        while self.player_data['screen'] == 'import_maps':
            self.handle_events()
            self.draw_import_screen()


class Button:
    def __init__(self, text, font, rect, color_idle, color_hover, action=None):
        self.text = text
        self.font = font
        self.rect = pygame.Rect(rect)
        self.color_idle = color_idle
        self.color_hover = color_hover
        self.action = action
        self.hovered = False
        self.text_surf = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, win):
        if self.hovered:
            pygame.draw.rect(win, self.color_hover, self.rect)
        else:
            pygame.draw.rect(win, self.color_idle, self.rect)
        win.blit(self.text_surf, self.text_rect)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

    def click(self):
        if self.hovered and self.action:
            self.action()