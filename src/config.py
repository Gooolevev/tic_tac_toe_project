# game.py
# 1. Standard Library Imports
import os
import sys

# 2. Third-party Imports
import pygame

# 3. Local/Application Imports
from logic import Field
from players import BotPlayer, HumanPlayer 
# from config import CELL_SIZE, MARGIN, WIDTH, HEIGHT

CELL_SIZE = 100