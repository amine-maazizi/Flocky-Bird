import pygame as pg
from random import randint

from utils import WIDTH, GROUND_LEVEL, MIN_GAP, MAX_GAP, PIPE_SPEED

class PipePair:
    """
    Represents a pair of pipes (top and bottom) for Flappy Bird game.

    Attributes:
        pipe_bottom_image (Surface): The image for the bottom pipe.
        pipe_top_image (Surface): The image for the top pipe, flipped.
        pipe_bottom_rect (Rect): Rect for bottom pipe.
        pipe_top_rect (Rect): Rect for top pipe.
    """
    def __init__(self) -> None:
        """Initialize the pipe pair with images and default positions."""
        self.load_images()
        self.reset()

    def load_images(self):
        """Load and set up the pipe images."""
        self.pipe_bottom_image = pg.image.load('sprites/pipe-green.png').convert_alpha()
        self.pipe_top_image = pg.transform.flip(self.pipe_bottom_image, False, True)
        self.pipe_bottom_rect = self.pipe_bottom_image.get_rect()
        self.pipe_top_rect = self.pipe_top_image.get_rect()

    def update(self) -> None:
        """
        Update the position of the pipes moving them left based on the pipe speed.
        Reset if the pipes go off screen.
        """
        self.pipe_bottom_rect.x -= PIPE_SPEED
        self.pipe_top_rect.x -= PIPE_SPEED

        if self.pipe_bottom_rect.right < 0:
            self.reset()

    def render(self, display) -> None:
        """
        Render the pipes on the given display.

        Args:
            display (Surface): The game screen where pipes will be drawn.
        """
        display.blit(self.pipe_bottom_image, self.pipe_bottom_rect)
        display.blit(self.pipe_top_image, self.pipe_top_rect)

    def reset(self) -> None:
        """
        Reset the pipes to the right of the screen with random gaps and positions.
        """
        # Set x position to the right edge of the screen
        self.pipe_bottom_rect.x = WIDTH
        self.pipe_top_rect.x = WIDTH

        # Set random positions for the pipes
        pip_tip = 60  # Minimum distance from pipe ends to the screen top/bottom
        gap = randint(MIN_GAP, MAX_GAP)  # Random gap between top and bottom pipes
        top_y = randint(pip_tip, GROUND_LEVEL - pip_tip - gap)

        self.pipe_top_rect.bottom = top_y
        self.pipe_bottom_rect.top = top_y + gap
