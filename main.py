# main.py
import pygame
import sys
from src.game import Game
if __name__ == "__main__":
    pygame.init() 
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        pygame.quit()
        sys.exit()