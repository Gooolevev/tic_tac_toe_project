import pygame
from .logic import Field
from .players import HumanPlayer, BotPlayer
import sys
import os
from .render import GameRenderer
import json


class ConfigLoader:
    def __init__(self, filename="config.json"):
        self.config = self._load_config(filename)

    def _load_config(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Ошибка: Файл конфигурации '{filename}' не найден.")
            sys.exit()
        except json.JSONDecodeError:
            print(f"Ошибка: Некорректный формат JSON в файле '{filename}'.")
            sys.exit()

    def get_field_size(self):
        settings = self.config.get("field_settings", {})
        return settings.get("y_size", 3), settings.get("x_size", 3)

    def get_player_data(self, player_key):
        return self.config.get(player_key, {})

    def get_starting_player_symbol(self):
        return self.config.get("starting_player_symbol", "X")



class Game:
    def __init__(self, load_saved=False):
        # 1. Загрузка конфигурации
        config_loader = ConfigLoader()
        
        y_size, x_size = config_loader.get_field_size()
        p1_data = config_loader.get_player_data("player1_settings")
        p2_data = config_loader.get_player_data("player2_settings")
        
        default_p1_name, default_p1_sym = p1_data.get('name', 'Игрок 1'), p1_data.get('symbol', 'X')
        default_p2_name, default_p2_sym = p2_data.get('name', 'БОТ'), p2_data.get('symbol', 'O')
        default_p2_type = p2_data.get('type', 'bot').lower()
        
        curr_p = config_loader.get_starting_player_symbol()
        
        if load_saved and os.path.exists("game_state.json"):
            self.field = Field()
            loaded = self.field.load_config()
            if loaded:
                p1_name, p1_sym, p2_name, p2_sym, curr_p = loaded
            else:
                self.field = Field(y_size, x_size)
                p1_name, p1_sym = default_p1_name, default_p1_sym
                p2_name, p2_sym = default_p2_name, default_p2_sym
        else:
            self.field = Field(y_size, x_size)
            p1_name, p1_sym = default_p1_name, default_p1_sym
            p2_name, p2_sym = default_p2_name, default_p2_sym

        self.player1 = HumanPlayer(p1_name, p1_sym)
        
        if default_p2_type == "bot":
            self.player2 = BotPlayer(p2_name, p2_sym)
        elif default_p2_type == "human":
            self.player2 = HumanPlayer(p2_name, p2_sym)
        else:
            self.player2 = HumanPlayer(p2_name, p2_sym) 

        self.current_player = self.player1 if curr_p == p1_sym else self.player2

        self.game_over = False
        self.winner = None

        self.renderer = GameRenderer(self.field.x_size, self.field.y_size)

    def switch_player(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def check_game_state(self):
        if self.field.has_winner(self.current_player.symbol):
            self.game_over = True
            self.winner = self.current_player.name
        elif self.field.is_draw():
            self.game_over = True
            self.winner = None 

    def handle_click(self, mouse_pos):
        row, col = self.renderer.get_grid_coordinates(mouse_pos)

        if row is None or col is None:
            return

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

            self.renderer.draw(self.field, self.game_over, self.winner, self.current_player)
            
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()