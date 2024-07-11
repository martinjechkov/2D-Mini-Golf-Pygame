import pygame
import sys
from game import Game

if __name__ == "__main__":
    starting_level_number = 1 # 1-based index
    window_width = 800
    window_height = 600
    game = Game('levels.json', 1, window_width, window_height)
    game.run()

    pygame.quit()
    sys.exit()
