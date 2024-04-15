import matplotlib.pyplot as plt
from IPython import display
from utils import NUMBER_GENERATION  

plt.ion()  # Enable interactive mode

def plot(scores, mean_scores):
    """
    Plots the scores and mean scores over the generations and updates the plot live during training.

    Args:
        scores (list of int): List of scores per generation.
        mean_scores (list of float): List of mean scores calculated over the scores up to the current generation.

    This function is designed to be called within a training loop to visualize the progress.
    """
    display.clear_output(wait=True)  # Clear the output to make way for the new plot
    display.display(plt.gcf())  # Display the figure

    plt.clf()  # Clear the current figure
    fig = plt.gcf()  # Get the current figure

    plt.title('Training Progress')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    
    plt.plot(scores, label='Scores')  # Plot the raw scores
    plt.plot(mean_scores, label='Mean Scores')  # Plot the mean scores

    plt.ylim(ymin=0)  # Set the minimum y value to 0 for clarity

    # Annotate the latest points on the graph
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))

    plt.legend()  # Add a legend to clarify plot lines

    # Save the figure at the end of training
    if len(scores) == NUMBER_GENERATION:
        plt.savefig("training_progress.png")

    plt.show(block=False)  # Display the plot without blocking the rest of the program
    plt.pause(0.1)  # Pause briefly so updates are visible
