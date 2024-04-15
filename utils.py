from typing import Tuple
import pygame as pg
from enum import Enum

# Type alias for a 2D vector
v2 = pg.Vector2
color = pg.Color

# Constants
WIDTH: int = 288
HEIGHT: int = 512
SCALE: int = 1.5
FPS: int = 60
BG_COLOR: color = (0, 0, 0)
GROUND_LEVEL: int = HEIGHT - 112
FLAP_SPEED: int = -5
GRAVITY: float = 0.75
MAX_GRAVITY: int = 10
PIPE_SPEED: int = 4
MIN_GAP: int = 100
MAX_GAP: int = 150
SCORE_CAP: int = 50

# Evolutionary parameters
NUMBER_GENERATION: int = 50  # Number of generations to evolve
NUM_PARENTS: int = 6        # Number of parents to select for breeding
POPULATION_SIZE: int = 200  # Total population size
MUTATION_RATE: float = 0.15 # Probability of each weight being mutated
MUTATION_SCALE: float = 0.2 # Standard deviation of the Gaussian noise added during mutation

def rotate_sprite(sprite: pg.Surface, angle: float) -> pg.Surface:
    """
    Rotates a sprite around its center without changing its dimensions.

    Args:
    sprite (pg.Surface): The sprite image to rotate.
    angle (float): The angle in degrees to rotate the sprite.

    Returns:
    pg.Surface: The rotated sprite image.
    """
    orig_rect = sprite.get_rect()
    rot_sprite = pg.transform.rotate(sprite, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_sprite.get_rect().center
    rot_sprite = rot_sprite.subsurface(rot_rect).copy()
    return rot_sprite

class Collision(Enum):
    """
    Enum for different types of collisions in the game.
    """
    PIPE = 0
    SCORE = 1
    NONE = 3
