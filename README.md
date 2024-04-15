# Flocky Bird

Flocky Bird is an implementation of the classic Flappy Bird game enhanced with a genetic algorithm to autonomously train the game to play itself. The project utilizes a simple fully connected neural network to simulate evolutionary strategies that improve gameplay over generations.

## Explanation

### Game Implementation

"Flocky Bird" is a Pygame implementation of the popular game Flappy Bird. In this game, a bird navigates through a series of obstacles by flying between gaps in vertical pipes. The player controls the bird's vertical movement by initiating jumps, which counteract gravitational pull.

### Approach to Problem Solving

The core challenge was to develop an AI that could learn to play the game autonomously. To achieve this, a genetic algorithm was employed, which simulates a process of natural selection by creating, evolving, and selecting generations of AI "birds".

1. **Neural Network Architecture**: Each bird in the game is controlled by a simple fully connected neural network, which decides whether to jump based on its current state. The state includes positions relative to the next pipe, the bird's vertical speed, and other environmental variables.

2. **Genetic Algorithm**: This algorithm starts with a randomly initialized population of neural networks. Birds play the game, and each bird's fitness is assessed based on its score in the game. Higher-scoring birds are more likely to pass their "genes" (network parameters) on to the next generation. The genetic operations applied include:
   - **Selection**: Birds with higher scores are more likely to be chosen as parents.
   - **Crossover**: Child networks are created by combining parameters from two parent networks.
   - **Mutation**: To introduce variability, small random changes are applied to the child networks' parameters.

3. **Evolution Over Generations**: Through repeated cycles of selection, crossover, and mutation, the population evolves. Over time, the birds' ability to navigate through pipes improves significantly, demonstrating the effectiveness of genetic algorithms for this type of reinforcement learning problem.

## Installation

To set up your local development environment, follow these steps:

```bash
# Clone the repository
git clone https://github.com/yourusername/flocky-bird.git

# Navigate to the project directory
cd Flocky-Bird

# Install required Python packages
pip install -r requirements.txt
```

# Usage
To start the game and see the genetic algorithm in action, run:
```bash
python main.py
```

# Configuration
- **Game Settings**: To adjust game parameters like pipe speed, gravity, and bird jump dynamics, modify the constants defined in `utils.py`.
- **Evolutionary Parameters**: To change aspects related to the evolutionary algorithm such as mutation rate or fitness calculations, edit the `utils.py` and `training.py` file.

# Contributing

Feel free to fork the project and submit pull requests. You can also send me suggestions or report issues. Any contributions you make are greatly appreciated.

## Contact

- **Amine Maazizi**
- Email: Aminema1000@gmail.com or my academic email amine.maazizi@ensta-paris.fr
- LinkedIn: [Amine Maazizi](https://www.linkedin.com/in/amine-maazizi-190266235/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
 
