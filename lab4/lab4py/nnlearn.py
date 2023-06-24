import numpy as np


# Activation function
def sigmoid(x):
    """ Calculate sigmoid value of value x. """
    return 1 / (1 + np.exp(-x))


def load_csv(filepath):
    """Read csv file and split it into features and targets.

    Truncate first row since it contains only labels and cast all other string
    values to float. Returns 2D matrices for features and target values as
    ``np.array`` objects.

    Parameters
    ----------
    filepath : str
        Path to .csv file
    """
    X, Y = [], []

    with open(file=filepath, mode='r') as f:
        lines = [x.strip().split(',') for x in f.readlines()]

        for row in lines[1:]:
            features = row[:-1]
            target = row[-1]

            X.append(features)
            Y.append(target)

    return np.array(X, dtype=float), np.array(Y, dtype=float)


class NeuralNetwork:
    """Neural network class implementation.

    It has an initialization method that takes the dimensions of the input,
    hidden, and output layers. The weights and biases are randomly initialized
    from normal distribution with 0.01 standard deviation in the constructor.
    """

    def __init__(self, input_dim, hidden_dims, output_dim):
        self.layers = []
        self.biases = []
        self.weights = []
        self.diff_squared = 0.0

        layer_dims = [input_dim] + hidden_dims + [output_dim]

        for i in range(len(layer_dims) - 1):
            self.weights.append(
                np.random.normal(loc=0, scale=0.01,
                                 size=(layer_dims[i + 1], layer_dims[i]))
            )
            self.biases.append(np.random.normal(loc=0, scale=0.01,
                                                size=(layer_dims[i + 1])))

    def __repr__(self):
        return f"biases: {self.biases}\nweights: {self.weights}"

    def __str__(self):
        return f"biases: {self.biases}\nweights: {self.weights}"


class Population:
    def __init__(self, popsize, input_dim, hidden_dims, output_dim):
        self.population = []
        for _ in range(popsize):
            self.population.append(NeuralNetwork(input_dim=input_dim,
                                                 hidden_dims=hidden_dims,
                                                 output_dim=output_dim))

    def __repr__(self):
        return "\n".join([nn.__str__() for nn in self.population])

    def __str__(self):
        return "\n".join([nn.__str__() for nn in self.population])

    def _propagation(self, X):
        pass

    # Perform neural networks training
    def train(self, X, y, epochs, K, p, elit):
        """ Performs training using Genetic Algorithm. """
        self._propagation(X)

        for i in range(1, epochs + 1):
            # Every 2 000 iteration print current train error
            if i % 2000 == 0:
                print(f"[Train error @{i}: {1}]")

    def evaluate(self, X, y):
        return 0.1234567
