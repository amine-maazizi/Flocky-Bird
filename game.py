import pygame as pg
from pygame.locals import *
import sys


from utils import *
from gui import GUI
from bird import Bird
from pipe import PipePair


class Game:
    def __init__(self, population=None):
        """Initializes the game with an optional population of birds."""
        pg.init()
        pg.display.set_caption('Flocky Bird')
        self.display = pg.display.set_mode([SCALE * WIDTH, SCALE * HEIGHT])
        self.clock = pg.time.Clock()
        self.overlay_display = pg.Surface((WIDTH, HEIGHT))

        # Load images
        self.background_image = pg.image.load('sprites/background-day.png').convert_alpha()
        self.ground_image = pg.image.load('sprites/base.png').convert_alpha()
        self.ground_x = 0

        # Game state
        self.gameover = False
        self.death_counter = 0
        self.birds = population or []
        self.pipe = PipePair()
        self.gui = GUI()

    def handle_collisions(self):
        """Checks and handles collisions between birds and pipes."""
        collision_results = {}
        for bird in self.birds:
            if self.pipe.pipe_bottom_rect.colliderect(bird.rect) or self.pipe.pipe_top_rect.colliderect(bird.rect):
                bird.is_alive = False
                collision_results[bird] = Collision.PIPE
            elif not bird.passed and self.pipe.pipe_bottom_rect.right < bird.rect.left:
                bird.score += 1
                self.gui.set_score(bird.score)
                bird.passed = True
                collision_results[bird] = Collision.SCORE
            else:
                collision_results[bird] = Collision.NONE

            # Reset pipe pass status if all birds have passed or are dead
            if bird.passed and self.pipe.pipe_bottom_rect.right > bird.rect.left:
                bird.passed = False

        return collision_results

    def run_generation(self):
        """Runs the game simulation for one generation."""
        while any(bird.death_counter < 50 for bird in self.birds) and all(bird.score <= SCORE_CAP for bird in self.birds if bird.is_alive):
            self.overlay_display.fill(BG_COLOR)
            self.overlay_display.blit(self.background_image, (0, 0))

            for event in pg.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pg.quit()
                    sys.exit()

            for bird in self.birds:
                bird.render(self.overlay_display)
                bird.update(action=None, up_pipe=self.pipe.pipe_top_rect, down_pipe=self.pipe.pipe_bottom_rect)
                if not bird.is_alive:
                    bird.death_counter += 1
            
            self.pipe.update()
            self.handle_collisions()
            
            self.pipe.render(self.overlay_display)
            self.overlay_display.blit(self.ground_image, (self.ground_x, GROUND_LEVEL))
            self.overlay_display.blit(self.ground_image, (self.ground_x + WIDTH, GROUND_LEVEL))
            
            self.ground_x = (self.ground_x - 2) % -WIDTH

            self.gui.render(self.overlay_display)
            self.display.blit(pg.transform.scale(self.overlay_display, (SCALE * WIDTH, SCALE * HEIGHT)), (0, 0))
            pg.display.update()
            self.clock.tick(FPS)

    def reset(self, population=None):
        """Resets the game to a fresh state with a new population of birds."""
        self.pipe.reset()
        self.gui.reset()
        self.birds = population or []

    def set_population(self, population):
        """Sets the population of birds for the game."""
        self.birds = population
