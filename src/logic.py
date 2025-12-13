# logic.py
import json
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