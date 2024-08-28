import pygame
import sys
from utils import blit_text_center


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


class GameMenu:
    def __init__(self, win, width, height):
        self.win = win
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("comicsans", 48)
        self.menu_active = True
        self.options_active = False
        self.buttons = []
        self.options_buttons = []
        self.current_screen = "main_menu"

        self.create_buttons()
        self.create_options_buttons()

    def create_buttons(self):
        play_button = Button("Play", self.font, (self.width // 2 - 100, self.height // 2 - 50, 200, 50),
                             (0, 128, 0), (0, 255, 0), action=self.start_game)
        options_button = Button("Options", self.font, (self.width // 2 - 100, self.height // 2 + 20, 200, 50),
                                (0, 128, 128), (0, 255, 255), action=self.open_options)
        quit_button = Button("Quit", self.font, (self.width // 2 - 100, self.height // 2 + 90, 200, 50),
                             (128, 0, 0), (255, 0, 0), action=self.quit_game)
        self.buttons.extend([play_button, options_button, quit_button])

    def create_options_buttons(self):
        back_button = Button("Back", self.font, (self.width // 2 - 100, self.height // 2 + 90, 200, 50),
                             (128, 128, 0), (255, 255, 0), action=self.back_to_menu)
        self.options_buttons.append(back_button)

    def start_game(self):
        self.menu_active = False
        self.options_active = False

    def open_options(self):
        self.current_screen = "options_menu"
        self.options_active = True

    def back_to_menu(self):
        self.current_screen = "main_menu"
        self.options_active = False

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def draw_menu(self):
        self.win.fill((0, 0, 0))
        blit_text_center(self.win, self.font, "Main Menu")
        for button in self.buttons:
            button.draw(self.win)
        pygame.display.update()

    def draw_options(self):
        self.win.fill((0, 0, 0))
        blit_text_center(self.win, self.font, "Options")
        for button in self.options_buttons:
            button.draw(self.win)
        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()

            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                if self.current_screen == "main_menu":
                    for button in self.buttons:
                        button.check_hover(pos)
                elif self.current_screen == "options_menu":
                    for button in self.options_buttons:
                        button.check_hover(pos)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.current_screen == "main_menu":
                    for button in self.buttons:
                        button.click()
                elif self.current_screen == "options_menu":
                    for button in self.options_buttons:
                        button.click()

    def run(self):
        while self.menu_active:
            self.handle_events()
            if self.current_screen == "main_menu":
                self.draw_menu()
            elif self.current_screen == "options_menu":
                self.draw_options()
