import pygame
import time

class TutorialScreen:
    def __init__(self, win, font, steps, images=None, skip_enabled=True):
        self.win = win
        self.font = font
        self.steps = steps
        self.images = images if images else []
        self.current_step = 0
        self.started = False
        self.finished = False
        self.step_start_time = 0
        self.background_color = (30, 30, 30)
        self.skip_enabled = skip_enabled
        self.objectives = [False] * len(steps)
        self.skip_text = font.render("Premi ESC per saltare", True, (200, 200, 200))

    def start(self):
        self.started = True
        self.step_start_time = time.time()
        self.display_step()

    def display_step(self):
        current_text = self.steps[self.current_step]["text"]
        self.blit_text_center(current_text)

        if self.images and self.current_step < len(self.images):
            self.display_image(self.images[self.current_step])

        if self.skip_enabled:
            self.win.blit(self.skip_text, (self.win.get_width() - self.skip_text.get_width() - 20,
                                           self.win.get_height() - self.skip_text.get_height() - 20))
        pygame.display.update()

    def blit_text_center(self, text):
        rendered_text = self.font.render(text, True, (200, 200, 200))
        self.win.blit(rendered_text, (self.win.get_width() / 2 - rendered_text.get_width() / 2,
                                      self.win.get_height() / 2 - rendered_text.get_height() / 2))

    def display_image(self, image):
        image_rect = image.get_rect(center=(self.win.get_width() // 2, self.win.get_height() // 2 + 100))
        self.win.blit(image, image_rect.topleft)

    def next_step(self):
        self.current_step += 1
        if self.current_step >= len(self.steps):
            self.finished = True
        else:
            self.display_step()
            self.step_start_time = time.time()

    def complete_objective(self):
        self.objectives[self.current_step] = True
        self.next_step()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.started and not self.finished:
            if self.skip_enabled and event.key == pygame.K_ESCAPE:
                self.finished = True
            elif event.key == pygame.K_RETURN:
                self.complete_objective()

    def update(self):
        if not self.started or self.finished:
            return

        if self.steps[self.current_step].get("wait_for_input", False):
            return

        elapsed_time = time.time() - self.step_start_time
        if elapsed_time >= self.steps[self.current_step]["duration"]:
            self.next_step()

    def draw(self):
        if self.started and not self.finished:
            self.win.fill(self.background_color)
            self.display_step()

    def run_tutorial(self):
        clock = pygame.time.Clock()
        running = True
        self.start()

        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_event(event)

            self.update()
            self.draw()

        pygame.quit()

pygame.init()
WINDOW = pygame.display.set_mode((800, 600))
FONT = pygame.font.SysFont("comicsans", 44)

# img per tut
tutorial_images = [
    pygame.image.load("imgs/tutorial_step1.png"),
    pygame.image.load("imgs/tutorial_step2.png"),
    pygame.image.load("imgs/tutorial_step3.png"),
]

tutorial_steps = [
    {"text": "Benvenuto nel Tutorial!", "duration": 3},
    {"text": "Usa i tasti freccia per muoverti", "duration": 4, "wait_for_input": True},
    {"text": "Premi W per accelerare", "duration": 4, "wait_for_input": True},
    {"text": "Premi S per frenare", "duration": 4, "wait_for_input": True},
    {"text": "Tutorial completato!", "duration": 3},
]

tutorial = TutorialScreen(WINDOW, FONT, tutorial_steps, images=tutorial_images, skip_enabled=True)
tutorial.run_tutorial()