import pygame as pg
from utils import *

class GUI:
    """Handles the graphical user interface for displaying scores in the game."""
    
    def __init__(self):
        """Initializes the GUI components including loading number sprites for displaying scores."""
        self.reset()
        self.num_sprite_dict = self.load_number_sprites()

    def load_number_sprites(self):
        """Loads number sprites from files and returns a dictionary mapping digits to their corresponding sprites."""
        num_sprite_dict = {}
        for num in range(10):
            num_sprite_dict[str(num)] = pg.image.load(f'sprites/{num}.png').convert_alpha()
        return num_sprite_dict

    def increment_score(self):
        """Increments the current score by one."""
        self.score += 1

    def set_score(self, score):
        """Sets the current score to the specified value."""
        self.score = score

    def set_highscore(self, highscore):
        """Sets the high score to the specified value if it is greater than the current high score."""
        self.highscore = max(self.highscore, highscore)

    def render(self, display):
        """Renders the current score at a fixed position on the display."""
        score_digits = [int(d) for d in str(self.score)[::-1]]
        for i, digit in enumerate(score_digits):
            display.blit(self.num_sprite_dict[str(digit)], (WIDTH // 2 - 24 * (i), 36))

    def reset(self):
        """Resets the score to zero."""
        self.score = 0
        self.highscore = 0
        