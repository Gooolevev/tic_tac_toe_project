# players.py
import random
from .logic import Display

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