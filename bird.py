import pygame as pg
import numpy as np

from utils import WIDTH, HEIGHT, FLAP_SPEED, GRAVITY, MAX_GRAVITY, GROUND_LEVEL, PIPE_SPEED, rotate_sprite

class Bird:
    """
    Represents the player-controlled bird in the Flappy Bird game.

    Attributes:
        sprite_dict (dict): Dictionary of bird sprites for animation.
        rect (pygame.Rect): The rectangle representing the bird's position.
        nn (NeuralNet): The neural network used for decision making if AI-controlled.
        is_alive (bool): Status of the bird, alive or not.
        velocity (pygame.Vector2): The velocity of the bird in pixels per frame.
        score (int): The score the bird has achieved.
        passsed (bool): Flag to indicate if the bird has passed a pipe.
        death_counter (int): Counter to keep track for how long the bird has been dead (for animation purposes).
    """

    def __init__(self, neural_network=None) -> None:
        """Initializes the Bird object with sprites, position, and neural network if provided."""
        self.load_sprites()
        self.rect = self.sprite_dict['midflap'].get_rect(center=(WIDTH // 3, HEIGHT // 2))
        
        self.nn = neural_network

        self.is_alive = True
        self.velocity = pg.Vector2(0, 0)
        self.score = 0
        self.passed = False
        self.death_counter = 0
        
    def load_sprites(self):
        """Loads bird sprites and stores them in a dictionary for animation purposes."""
        self.sprite_dict = {
            'midflap': pg.image.load('sprites/bluebird-midflap.png').convert_alpha(),
            'downflap': pg.image.load('sprites/bluebird-downflap.png').convert_alpha(),
            'upflap': pg.image.load('sprites/bluebird-upflap.png').convert_alpha()
        }
        self.current_sprite = self.sprite_dict['midflap']

    def jump(self) -> None:
        """Makes the bird jump by setting its vertical velocity to the flap speed."""
        if self.is_alive:
            self.velocity.y = FLAP_SPEED

    def update(self, action=None, up_pipe=None, down_pipe=None) -> None:
        """Updates the bird's position and status based on the game dynamics and neural network output."""
        self.velocity.y += GRAVITY 
        self.velocity.y = min(self.velocity.y, MAX_GRAVITY)

        self.process_action(action, up_pipe, down_pipe)
        
        if not self.is_alive:
            self.velocity.x = -2 * PIPE_SPEED  # Move bird left when dead to simulate collision
            self.rect.x += self.velocity.x

        self.rect.y += self.velocity.y   
             
        self.check_boundaries()

    def process_action(self, action, up_pipe, down_pipe):
        """Processes the action based on the game state or neural network prediction."""
        if self.nn and up_pipe and down_pipe:
            state = self.get_state(up_pipe, down_pipe)
            action = self.nn.predict(state)

        if action == 1:
            self.jump()

    def check_boundaries(self):
        """Check and update the bird's alive status if it hits the boundaries."""
        if self.rect.top <= 0 or self.rect.bottom >= GROUND_LEVEL:
            self.is_alive = False

    def animate(self):
        """Updates the bird's sprite based on its velocity and orientation."""
        self.current_sprite = self.sprite_dict['upflap'] if self.velocity.y < -2 else self.sprite_dict['downflap'] if self.velocity.y > 2 else self.sprite_dict['midflap']
        rotation = min(max(-45, self.velocity.y * -2), 45)  # Rotate bird based on velocity [-45, 45]
        self.current_sprite = rotate_sprite(self.current_sprite, rotation)

    def render(self, display) -> None:
        """Renders the bird's current sprite at its current position."""
        self.animate()
        display.blit(self.current_sprite, self.rect)

    def get_state(self, up_pipe, down_pipe):
        """
        Calculates the state vector used as input to the neural network.
        
        The state vector includes:
        - Normalized horizontal distance to the next pipe: Provides the neural network
        with the relative horizontal position of the next obstacle.
        - Normalized vertical distance from the bird to the top of the bottom pipe:
        Helps the network to evaluate how much vertical space the bird has to clear the bottom pipe.
        - Normalized vertical distance from the bird to the bottom of the top pipe:
        Helps the network to evaluate how much vertical space the bird has to clear the top pipe.
        - Normalized vertical velocity of the bird: Indicates how fast the bird is moving
        vertically, which can help the network decide if the bird needs to jump or fall.
        
        Each component is normalized by the respective dimension (WIDTH or HEIGHT) or by the
        maximum velocity (MAX_GRAVITY) to maintain scale consistency and improve neural network performance.
        """
        return np.array([
            (up_pipe.x - self.rect.centerx) / WIDTH,  # Horizontal distance to the next pipe, normalized by screen width
            (down_pipe.top - self.rect.centery) / HEIGHT,  # Distance from bird to the top of the bottom pipe, normalized by screen height
            (self.rect.centery - up_pipe.bottom) / HEIGHT,  # Distance from bird to the bottom of the top pipe, normalized by screen height
            self.velocity.y / MAX_GRAVITY  # Bird's vertical velocity, normalized by maximum allowed gravity
        ])
