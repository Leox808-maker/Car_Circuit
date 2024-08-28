import pygame
import sys
from utils import blit_text_center

class CustomizationScreen:
    def __init__(self, win, width, height, car_skins, skills, player_data):
        self.win = win
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("comicsans", 36)
        self.small_font = pygame.font.SysFont("comicsans", 28)
        self.car_skins = car_skins
        self.skills = skills
        self.player_data = player_data
        self.current_skin_index = 0
        self.selected_skills = {skill: 0 for skill in skills}
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        confirm_button = Button("Confirm", self.font, (self.width // 2 - 150, self.height - 100, 300, 50),
                                (0, 128, 0), (0, 255, 0), action=self.confirm_selection)
        self.buttons.append(confirm_button)

    def confirm_selection(self):
        self.player_data['selected_skin'] = self.car_skins[self.current_skin_index]
        self.player_data['selected_skills'] = self.selected_skills
        self.player_data['screen'] = 'menu'

    def draw_customization(self):
        self.win.fill((0, 0, 0))
        blit_text_center(self.win, self.font, "Car Customization")

        skin_text = f"Selected Skin: {self.car_skins[self.current_skin_index]}"
        self.draw_text(skin_text, (255, 255, 255), (self.width // 2, self.height // 2 - 120))

        for i, skill in enumerate(self.skills):
            skill_text = f"{skill.capitalize()}: {self.selected_skills[skill]}"
            self.draw_text(skill_text, (255, 255, 255), (self.width // 2, self.height // 2 - 60 + i * 40))

        instruction_text = "Use Left/Right to change skin, Up/Down to adjust skills"
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
                    self.current_skin_index = (self.current_skin_index - 1) % len(self.car_skins)
                if event.key == pygame.K_RIGHT:
                    self.current_skin_index = (self.current_skin_index + 1) % len(self.car_skins)
                if event.key == pygame.K_UP:
                    self.adjust_skill(1)
                if event.key == pygame.K_DOWN:
                    self.adjust_skill(-1)

    def adjust_skill(self, adjustment):
        current_skill = list(self.selected_skills.keys())[self.get_current_skill_index()]
        self.selected_skills[current_skill] = max(0, self.selected_skills[current_skill] + adjustment)

    def get_current_skill_index(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            return 0
        if keys[pygame.K_2]:
            return 1
        if keys[pygame.K_3]:
            return 2
        return 0

        def run(self):
            while self.player_data['screen'] == 'customization':
                self.handle_events()
                self.draw_customization()

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