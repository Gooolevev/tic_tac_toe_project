import random
import json
import pygame
import sys
import os

class Cell:
    def __init__(self, symbol=" "):
        self.symbol = symbol

    def draw(self):
        return self.symbol

    def is_empty(self):
        return self.symbol == " "

    def set_symbol(self, new_symbol):
        if self.is_empty():
            self.symbol = new_symbol
            return True
        return False


class Display:  
    @staticmethod 
    def draw(content): 
        print(f'{content}')



class Field:
    def __init__(self,y_size = 3,x_size = 3):
        self.y_size = y_size
        self.x_size = x_size
        self.grid = [[Cell() for _ in range(self.x_size)] for _ in range(self.y_size)]

    def make_move(self, position, player):
        total_cells = self.x_size * self.y_size
        if position < 1 or position > total_cells:
            return False
        
        pos = position - 1
        row = pos // self.x_size
        col = pos % self.x_size

        if row >= self.y_size or col >= self.x_size:
            return False

        cell = self.grid[row][col]
        if cell.set_symbol(player):
            return True
        else:
            return False

    def has_winner(self, player):
        n = self.x_size
        m = self.y_size

        for row in self.grid:
            if all(cell.symbol == player for cell in row):
                return True

        for col in range(n):
            if all(self.grid[row][col].symbol == player for row in range(m)):
                return True

        if n == m:
            if all(self.grid[i][i].symbol == player for i in range(n)):
                return True
            if all(self.grid[i][n - 1 - i].symbol == player for i in range(n)):
                return True

        return False

    def is_draw(self):
        for row in self.grid:
            for cell in row:
                if cell.is_empty():
                    return False
        return True

    def get_config(self, p1_name, p1_sym, p2_name, p2_sym, current_p):
        return {
            'x_size': self.x_size,
            'y_size': self.y_size,
            'grid': [[cell.symbol for cell in row] for row in self.grid],
            'player1': {'name': p1_name, 'symbol': p1_sym},
            'player2': {'name': p2_name, 'symbol': p2_sym},
            'current_player': current_p
        }

    def save_config(self, p1_name, p1_sym, p2_name, p2_sym, current_p, filename="game_state.json"):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.get_config(p1_name, p1_sym, p2_name, p2_sym, current_p), f, indent=2, ensure_ascii=False)
        except Exception as e:
            return False

    def load_config(self, filename="game_state.json"):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                config = json.load(f)

            self.x_size = config['x_size']
            self.y_size = config['y_size']
            self.grid = [[Cell(config['grid'][i][j]) for j in range(self.x_size)] for i in range(self.y_size)]

            return (
                config['player1']['name'], config['player1']['symbol'],
                config['player2']['name'], config['player2']['symbol'],
                config['current_player']
            )
        except FileNotFoundError:
            return False
        except Exception as e:
            return None


class Player:
    def __init__(self, name, symbol):
        self.symbol = symbol
        self.name = name

    def get_name(self):
        return self.name

    def get_symbol(self):
        return self.symbol

    def get_move(self, field):
        raise NotImplementedError("Метод должен быть реализован в подклассах")

    def draw_info(self):
        Display.draw(f"Игрок: {self.name} ({self.symbol})")



class HumanPlayer(Player):
    def __init__(self, name, symbol):
        super().__init__(name, symbol)
    
    def get_move(self, field):
        return None



class BotPlayer(Player):
    def get_move(self, field):
        free_positions = []
        total_cells = field.x_size * field.y_size
        for pos in range(1, total_cells + 1):
            row = (pos - 1) // field.x_size
            col = (pos - 1) % field.x_size
            if field.grid[row][col].symbol == " ":
                free_positions.append(pos)
        return random.choice(free_positions) if free_positions else 1



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


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
