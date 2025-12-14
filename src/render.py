import pygame


class GameRenderer:
    def __init__(self, x_size, y_size):
        self.cell_size = 100
        self.margin = 10
        self.x_size = x_size
        self.y_size = y_size
        
        self.width = self.x_size * (self.cell_size + self.margin) + self.margin
        self.height = self.y_size * (self.cell_size + self.margin) + self.margin + 40
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Крестики-нолики")
        
        self.font = pygame.font.SysFont("Arial", 50, bold=True)
        self.info_font = pygame.font.SysFont("Arial", 28, bold=True)

    def draw(self, field, game_over, winner, current_player):
        self.screen.fill((170, 110, 70))

        for row in range(self.y_size):
            for col in range(self.x_size):
                x = self.margin + col * (self.cell_size + self.margin)
                y = self.margin + row * (self.cell_size + self.margin)
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                
                pygame.draw.rect(self.screen, (220, 160, 120), rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 3)

                symbol = field.grid[row][col].symbol
                if symbol != " ":
                    color = (255, 248, 220) if symbol == "X" else (100, 50, 40)
                    text = self.font.render(symbol, True, color)
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)
    
        panel_height = 40
        panel_y = self.height - panel_height
        pygame.draw.rect(self.screen, (250, 250, 250), (0, panel_y, self.width, panel_height))
        
        if game_over:
            if winner:
                msg = f"Победил {winner}!"
            else:
                msg = "Ничья!"
        else:
            msg = f"Ход: {current_player.name} ({current_player.symbol})"

        info = self.info_font.render(msg, True, (0, 0, 0))
        info_rect = info.get_rect(center=(self.width // 2, panel_y + panel_height // 2))
        self.screen.blit(info, info_rect)

    def get_grid_coordinates(self, mouse_pos):
        x, y = mouse_pos
        if y > self.height - 40:
            return None, None

        col = (x - self.margin) // (self.cell_size + self.margin)
        row = (y - self.margin) // (self.cell_size + self.margin)
        return row, col