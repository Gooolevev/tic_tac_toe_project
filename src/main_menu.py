import pygame
import sys
import os

class MainMenu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((340, 380))
        pygame.display.set_caption("Крестики-нолики — Меню")

        self.title_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.menu_font = pygame.font.SysFont("Arial", 24, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 14,bold=True)

        self.menu_items = ["Новая игра", "Продолжить", "Правила", "Выход"]
        self.continue_true = os.path.exists("game_state.json")

    def show_rules(self):
        rules = [
            "Правила игры:",
            "",
            "1. Игроки по очереди ставят символ (X или O)",
            "",
            "2. Нажмите R для перезапуска после игры",
            "",
            "Нажмите где угодно, чтобы закрыть"
        ]

        running = True
        while running:
            self.screen.fill((170, 110, 70))
            y = 50
            for line in rules:
                text = self.small_font.render(line, True, (255, 255, 255))
                x = self.screen.get_width() // 2 - text.get_width() // 2
                self.screen.blit(text, (x, y))
                y += 30

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.QUIT):
                    running = False
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.screen.fill((170, 110, 70))

            title = self.title_font.render("Крестики-нолики", True, (255, 255, 255))
            self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 30))

            item_rects = []
            for i, item in enumerate(self.menu_items):
                color = (150, 150, 150) if (i == 1 and not self.continue_true) else (255, 255, 255)
                text = self.menu_font.render(item, True, color)
                x = self.screen.get_width() // 2 - text.get_width() // 2
                y = 120 + i * 60
                self.screen.blit(text, (x, y))

                rect = text.get_rect(topleft=(x, y))
                rect.height = 40
                item_rects.append(rect)

            panel_height = 40
            pygame.draw.rect(self.screen, (255, 255, 255), (0, 340, 340, panel_height))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for i, rect in enumerate(item_rects):
                        if i == 1 and not self.continue_true:
                            continue
                        if rect.collidepoint(mouse_pos):
                            if i == 0:
                                if os.path.exists("game_state.json"):
                                    os.remove("game_state.json")
                                return "new"
                            elif i == 1:
                                return "continue"
                            elif i == 2:
                                self.show_rules()
                                break
                            elif i == 3:
                                pygame.quit()
                                sys.exit()

            clock.tick(60)
