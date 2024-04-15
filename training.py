from random import random, choice
import numpy as np
import os

from utils import *
from network import NeuralNet
from game import Game
from bird import Bird   
from plot import plot

def evaluate_fitness(bird):
    """
    Calculates the fitness of a bird based on its score.
    :param bird: Bird object
    :return: Fitness value as an integer score
    """
    return bird.score

def selection(population, num_parents):
    """
    Selects the top scoring birds to be parents for the next generation.
    :param population: List of Bird objects
    :param num_parents: Number of top birds to select
    :return: List of Bird objects that are selected as parents
    """
    sorted_population = sorted(population, key=evaluate_fitness, reverse=True)
    return sorted_population[:num_parents]

def crossover(parent_1, parent_2):
    """
    Performs crossover between two parent birds to produce offspring.
    :param parent_1: First parent Bird object
    :param parent_2: Second parent Bird object
    :return: Bird object as a child with mixed parameters
    """
    child_params = {}
    for param in parent_1.nn.get_params().keys():
        child_params[param] = parent_1.nn.get_params()[param] if random() > 0.5 else parent_2.nn.get_params()[param]
    return Bird(NeuralNet(params=child_params))

def mutate(bird):
    """
    Mutates a bird's neural network parameters.
    :param bird: Bird object
    :return: Bird object with mutated parameters
    """
    for param in bird.nn.get_params().keys():
        if random() < MUTATION_RATE:
            bird.nn.get_params()[param] += np.random.normal(0, MUTATION_SCALE)
    return bird

def run_evolution():
    """
    Runs the evolutionary process to train birds over multiple generations.
    """
    game = Game()
    population = [Bird(NeuralNet()) for _ in range(POPULATION_SIZE)]
    game.set_population(population)
    
    best_score = -float('inf')
    best_model = None
    
    scores_history = []
    mean_scores_history = []
    
    for generation in range(NUMBER_GENERATION):
        game.run_generation()
        
        scores = [bird.score for bird in game.birds]
        current_best_score = max(scores)
        scores_history.append(current_best_score)
        mean_score = np.mean(scores_history)
        mean_scores_history.append(mean_score)
        
        parents = selection(game.birds, NUM_PARENTS)
        
        if current_best_score > best_score:
            best_score = current_best_score
            best_model = parents[0].nn
            if not os.path.exists('models'):
                os.makedirs('models')
            best_model.save(f'models/best_model_generation_{generation+1}.pth')
            print(f"New best model saved with score: {best_score}")
        
        next_gen = [mutate(crossover(choice(parents), choice(parents))) for _ in range(POPULATION_SIZE)]
        game.reset(next_gen)
        
        plot(scores_history, mean_scores_history)
        print(f"Generation {generation + 1} completed. High Score: {best_score}")

    if best_model:
        best_model.save('models/model_exit.pth')
        print(f"Final best model saved with score: {best_score}")

