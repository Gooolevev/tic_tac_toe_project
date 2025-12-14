# main.py
import pygame
import sys
from src.game import Game
from src.main_menu import MainMenu
if __name__ == "__main__":
    menu = MainMenu()
    choice = menu.run()

    if choice == "new":
        game = Game(load_saved=False)
    elif choice == "continue":
        game = Game(load_saved=True)
    else:
        pygame.quit()
        sys.exit()

    game.run()