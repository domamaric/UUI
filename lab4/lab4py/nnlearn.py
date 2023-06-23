import csv
import numpy as np


def load_csv(filepath):
    """Read csv file and split it data and labels.

    Truncate first row since it contains only labels and cast all other string
    values to float. Returns 2D matrix as ``np.array`` object and list of
    labels.

    Parameters
    ----------
    filepath : str
        Path to .csv file
    """
    with open(file=filepath, mode='r') as f:
        matrix = [row for row in csv.reader(f)]
        y = matrix.pop(0)
        X = [[float(val) for val in row] for row in matrix]

    return np.array(X), y


# Activation functions
def sigmoid(x):
    """ Calculate sigmoid value of value x. """
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    """ Calculate value derivation of sigmoid function. """
    return x * (1 - x)


class NeuralNetwork:
    """Neural network class implementation.

    It has an initialization method that takes the dimensions of the input,
    hidden, and output layers. The weights and biases are randomly initialized
    from normal distribution with 0.01 standard deviation in the constructor.
    """

    def __init__(self, input_dim, hidden_dims, output_dim):
        self._input_dim = input_dim
        self._hidden_dims = hidden_dims
        self._output_dim = output_dim

        self.layers = []
        self.biases = []
        self.weights = []

        layer_dims = [input_dim] + hidden_dims + [output_dim]

        for i in range(len(layer_dims) - 1):
            self._weights.append(
                np.random.normal(0, 0.01, layer_dims[i], layer_dims[i + 1])
            )
            self._biases.append(np.random.rand(layer_dims[i + 1]))

    def _forward_propagation(self, X):
        self.layers = []
        self.layers.append(X)

        for i in range(len(self.weights)):
            hidden_output = sigmoid(
                np.dot(self.layers[i], self.weights[i]) + self.biases[i])
            self.layers.append(hidden_output)

        return self.layers[-1]

    def train():
        pass

    def predict(self, X):
        return self._forward_propagation(X)
