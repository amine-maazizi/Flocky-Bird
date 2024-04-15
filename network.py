import torch
import torch.nn as nn
import torch.optim as optim

class NeuralNet(nn.Module):
    def __init__(self, input_size=4, hidden_size=64, output_size=2, params=None):
        """
        Initializes the Neural Network with an optional parameter to load predefined weights.

        Args:
            input_size (int): Number of input features to the network.
            hidden_size (int): Number of units in each hidden layer.
            output_size (int): Number of output classes or actions (for classification tasks).
            params (dict, optional): Pretrained parameters for the network.
        """
        super(NeuralNet, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size),
            nn.Softmax(dim=-1)  # Use softmax for action probabilities at the output layer.
        )
        
        if params:
            self.load_params(params)

    def forward(self, x):
        """
        Defines the forward pass of the network.

        Args:
            x (Tensor): Input tensor containing the features.

        Returns:
            Tensor: The network's output tensor.
        """
        return self.net(x)
    
    def predict(self, state):
        """
        Predicts the action probabilities from a given state.
        
        Args:
            state (list or array): The state representation from the environment.

        Returns:
            int: The index of the action with the highest probability.
        """
        state = torch.tensor(state, dtype=torch.float32).unsqueeze(0)  # Convert to tensor, add batch dimension
        with torch.no_grad():  # Disable gradient computation for inference
            output = self.forward(state)
        return output.argmax().item()  # Return the action with the highest probability

    def save(self, filepath):
        """
        Saves the model parameters to a file.

        Args:
            filepath (str): Path to save the file.
        """
        torch.save(self.state_dict(), filepath)

    def load(self, filepath):
        """
        Loads the model parameters from a file.

        Args:
            filepath (str): Path of the file to load the model from.
        """
        self.load_state_dict(torch.load(filepath))
        self.eval()  # Set the model to evaluation mode

    def load_params(self, params):
        """
        Loads model parameters from a dictionary.

        Args:
            params (dict): Parameters for the network as a dictionary.
        """
        self.load_state_dict(params)

    def get_params(self):
        """
        Retrieves current model parameters.

        Returns:
            OrderedDict: A dictionary containing the model's parameters.
        """
        return self.state_dict()
