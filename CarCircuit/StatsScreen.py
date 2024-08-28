import pygame
import sys
from utils import blit_text_center

class StatsScreen:
    def __init__(self, win, width, height, stats):
        self.win = win
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("comicsans", 36)
        self.stats = stats
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        back_button = Button("Back to Menu", self.font, (self.width // 2 - 150, self.height - 100, 300, 50),
                             (0, 128, 0), (0, 255, 0), action=self.go_back_to_menu)
        self.buttons.append(back_button)

    def go_back_to_menu(self):
        self.stats['screen'] = 'menu'

    def draw_stats(self):
        self.win.fill((0, 0, 0))
        blit_text_center(self.win, self.font, "Game Statistics")

        played_text = f"Games Played: {self.stats['games_played']}"
        won_text = f"Games Won: {self.stats['games_won']}"
        lost_text = f"Games Lost: {self.stats['games_lost']}"

        self.draw_text(played_text, (255, 255, 255), (self.width // 2, self.height // 2 - 60))
        self.draw_text(won_text, (0, 255, 0), (self.width // 2, self.height // 2))
        self.draw_text(lost_text, (255, 0, 0), (self.width // 2, self.height // 2 + 60))

        for button in self.buttons:
            button.draw(self.win)

        pygame.display.update()

    def draw_text(self, text, color, position):
        text_surf = self.font.render(text, True, color)
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

    def run(self):
        while self.stats['screen'] == 'stats':
            self.handle_events()
            self.draw_stats()

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
            pygame.draw.rect(win, self.color_idle, self.rect)A
        win.blit(self.text_surf, self.text_rect)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

    def click(self):
        if self.hovered and self.action:
            self.action()
