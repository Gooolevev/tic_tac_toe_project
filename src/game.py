import pygame
from .logic import Field
from .players import HumanPlayer, BotPlayer
import sys
import os

class Game:
    def __init__(self):
        self.field = Field()
        loaded = self.field.load_config()

        if loaded:
            p1_name, p1_sym, p2_name, p2_sym, curr_p = loaded
        else:
            self.field = Field(3, 3)
            p1_name, p1_sym = "Игрок", "X"
            p2_name, p2_sym = "БОТ", "O"
            curr_p = "X"

        self.player1 = HumanPlayer(p1_name, p1_sym)
        if p2_name == "БОТ":
            self.player2 = BotPlayer(p2_name, p2_sym)
        else:
            self.player2 = HumanPlayer(p2_name, p2_sym)

        self.current_player = self.player1 if curr_p == p1_sym else self.player2


        self.game_over = False
        self.winner = None
        self.cell_size = 100
        self.margin = 10
        self.width = self.field.x_size * (self.cell_size + self.margin) + self.margin
        self.height = self.field.y_size * (self.cell_size + self.margin) + self.margin + 40
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Крестики-нолики")
        self.font = pygame.font.SysFont("Arial", 50, bold=True)
        self.info_font = pygame.font.SysFont("Arial", 28, bold=True)
    

    def switch_player(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def handle_click(self, mouse_pos):
        x, y = mouse_pos
        if y > self.height - 40:
            return

        col = (x - self.margin) // (self.cell_size + self.margin)
        row = (y - self.margin) // (self.cell_size + self.margin)

        if row < 0 or row >= self.field.y_size or col < 0 or col >= self.field.x_size:
            return

        position = row * self.field.x_size + col + 1

        if self.field.make_move(position, self.current_player.symbol):
            self.check_game_state()
            if not self.game_over:
                self.switch_player()
                self.field.save_config(
                self.player1.name, self.player1.symbol,
                self.player2.name, self.player2.symbol,
                self.current_player.symbol
            )
                if isinstance(self.current_player, BotPlayer):
                    pygame.time.set_timer(pygame.USEREVENT, 500)
            

    def make_bot_move(self):
        move = self.current_player.get_move(self.field)
        self.field.make_move(move, self.current_player.symbol)
        self.check_game_state()
        if not self.game_over:
            self.switch_player()
            self.field.save_config(
            self.player1.name, self.player1.symbol,
            self.player2.name, self.player2.symbol,
            self.current_player.symbol
        )

    def run(self):
        if isinstance(self.current_player, BotPlayer):
            self.make_bot_move()

        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if not self.game_over and event.type == pygame.MOUSEBUTTONDOWN:
                    if isinstance(self.current_player, HumanPlayer):
                        self.handle_click(event.pos)

                if event.type == pygame.USEREVENT:
                    pygame.time.set_timer(pygame.USEREVENT,0)
                    if not self.game_over and isinstance(self.current_player,BotPlayer):
                        self.make_bot_move() 
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        if os.path.exists("game_state.json"):
                            os.remove("game_state.json")
                        new_game = Game()
                        new_game.run()
                        return

            self.draw()
            pygame.display.flip() #показать всё, что нарисовал
            clock.tick(60)

        pygame.quit()
        sys.exit()

    def check_game_state(self):
        if self.field.has_winner(self.current_player.symbol):
            self.game_over = True
            self.winner = self.current_player.name
        elif self.field.is_draw():
            self.game_over = True
            self.winner = None 

    def draw(self):
        self.screen.fill((170, 110, 70))

        for row in range(self.field.y_size):
            for col in range(self.field.x_size):
                x = self.margin + col * (self.cell_size + self.margin)
                y = self.margin + row * (self.cell_size + self.margin)
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (220, 160, 120), rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 3)

                symbol = self.field.grid[row][col].symbol
                if symbol != " ":
                    color = (255, 248, 220) if symbol == "X" else (100, 50, 40)
                    text = self.font.render(symbol, True, color)
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)
    
        panel_height = 40
        panel_y = self.height - panel_height
        pygame.draw.rect(self.screen, (250, 250, 250), (0, panel_y, self.width, panel_height))
        if self.game_over:
            if self.winner:
                msg = f"Победил {self.winner}!"
            else:
                msg = "Ничья!"
        else:
            msg = f"Ход: {self.current_player.name} ({self.current_player.symbol})"

        info = self.info_font.render(msg, True, (0, 0, 0))
        info_rect = info.get_rect(center=(self.width // 2, panel_y + panel_height // 2))
        self.screen.blit(info, info_rect)