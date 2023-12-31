import math
import numpy as np
import random


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
        self.biases = []
        self.weights = []
        self.diff_squared = float('inf')

        layer_dims = [input_dim] + hidden_dims + [output_dim]

        for i in range(len(layer_dims) - 1):
            self.weights.append(
                np.random.normal(loc=0, scale=0.01,
                                 size=(layer_dims[i + 1], layer_dims[i]))
            )
            self.biases.append(np.random.normal(loc=0, scale=0.01,
                                                size=(layer_dims[i + 1])))

    def __repr__(self):
        return f"{self.diff_squared}\n"

    def __str__(self):
        return f"{self.diff_squared}\n"


class Population:
    def __init__(self, popsize, input_dim, hidden_dims, output_dim):
        self.input_dim = input_dim
        self.hidden_dims = hidden_dims
        self.output_dim = output_dim

        self.population = []
        self.popsize = popsize
        for _ in range(popsize):
            self.population.append(NeuralNetwork(input_dim=input_dim,
                                                 hidden_dims=hidden_dims,
                                                 output_dim=output_dim))

    def __repr__(self):
        return "\n".join([nn.__str__() for nn in self.population])

    def __str__(self):
        return "\n".join([nn.__str__() for nn in self.population])

    def _propagation(self, X, y):
        """Performs forward propagation for each neural network."""
        for nn in self.population:
            # breakpoint()
            outputs = X

            for i, (weights, biases) in enumerate(zip(nn.weights, nn.biases)):
                outputs = np.dot(outputs, weights.T) + biases

                # Skip sigmoid for last layer
                if i != len(nn.weights) - 1:
                    outputs = sigmoid(outputs)

            err = np.mean(np.square(y - outputs))
            nn.diff_squared = err

    def train(self, X, y, epochs, K, p, elit):
        """ Performs training using Genetic Algorithm. """
        for i in range(1, epochs + 1):
            self._propagation(X, y)
            # Every 2 000 iteration print current train error
            if i % 2000 == 0:
                best_population = min(
                    self.population, key=lambda nn: nn.diff_squared)
                print(f"[Train error @{i}]: {best_population.diff_squared}")

            # Elitism and selection
            sortedPopulation = sorted(self.population,
                                      key=lambda nn: nn.diff_squared)[:elit]

            # Crossing
            newPopulation = []
            while len(newPopulation) < self.popsize:
                neuralNetwork1 = random.choice(sortedPopulation)

                if len(newPopulation) == 0:
                    neuralNetwork2 = random.choice(sortedPopulation)
                else:
                    neuralNetwork2 = random.choice(newPopulation)

                newWeights = [(n1 + n2) / 2 for n1, n2 in zip(
                    neuralNetwork1.weights, neuralNetwork2.weights)]
                newB = [(n1 + n2) / 2 for n1, n2 in zip(
                    neuralNetwork1.biases, neuralNetwork2.biases)]

                nn = NeuralNetwork(
                    self.input_dim, self.hidden_dims, self.output_dim)
                nn.weights = newWeights.copy()
                nn.biases = newB.copy()
                newPopulation.append(nn)

            # Mutation
            for currentPop in newPopulation:
                for w in currentPop.weights:
                    w += np.random.normal(0, K, size=w.shape) * \
                        (np.random.random() < p)

                for b in currentPop.biases:
                    b += np.random.normal(0, K, size=b.shape) * \
                        (np.random.random() < p)

            self.population = newPopulation.copy()

    def evaluate(self, X, y):
        """ Forward propagation on the best individual in the population """
        best_nn = min(self.population, key=lambda nn: nn.diff_squared)

        outputs = X
        for i, (weights, biases) in enumerate(zip(best_nn.weights,
                                                  best_nn.biases)):
            outputs = np.dot(outputs, weights.T) + biases

            # Skip sigmoid for last layer
            if i != len(best_nn.weights) - 1:
                outputs = sigmoid(outputs)

        diff_squared = np.mean(np.square(y - outputs))

        return diff_squared
