import math
import numpy as np
import random


def sigmoid(x):
    """ Calculate sigmoid value of value x. """
    return 1 / (1 + np.exp(-x))


def load_csv(filepath):
    """Read csv file and split it into features and targets."""
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

    The weights and biases are randomly initialized from normal distribution
    with 0.01 standard deviation in the constructor.
    """
    def __init__(self, input_dim, hidden_dims, output_dim):
        self.biases = []
        self.weights = []
        self.mse = float('inf')

        layer_dims = [input_dim] + hidden_dims + [output_dim]

        for i in range(len(layer_dims) - 1):
            self.weights.append(np.random.normal(loc=0,scale=0.01,
                                 size=(layer_dims[i + 1], layer_dims[i])))
            self.biases.append(np.random.normal(loc=0, scale=0.01,
                                                size=(layer_dims[i + 1])))

    def __repr__(self):
        return f"{self.mse}\n"

    def __str__(self):
        return f"{self.mse}\n"


class Population:
    """Population class implementation."""
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
        length = len(X)

        for nn in self.population:
            total_mse = 0.0

            for x, target in zip(X, y):
                outputs = x

                for i, (weights, biases) in enumerate(zip(nn.weights, nn.biases)):
                    outputs = np.dot(outputs, weights.T) + biases

                    if i != len(nn.weights) - 1:  # Skip sigmoid for last layer
                        outputs = sigmoid(outputs)

                mse = np.mean(np.square(target - outputs))
                total_mse += mse

            nn.mse = total_mse / length

    def _crossing(self, elit_population):
        """Perform crossing for generating new individuals."""
        new_population = []

        while len(new_population) < self.popsize:
            nn1 = random.choice(elit_population)
            nn2 = random.choice(elit_population)

            # Create copies of weights and biases
            new_weights = [(w1 + w2) / 2 for w1, w2 in zip(nn1.weights, nn2.weights)]
            new_biases = [(b1 + b2) / 2 for b1, b2 in zip(nn1.biases, nn2.biases)]

            new_nn = NeuralNetwork(self.input_dim, self.hidden_dims, self.output_dim)
            new_nn.weights = new_weights
            new_nn.biases = new_biases
            new_population.append(new_nn)

        return new_population

    def _mutation(self, new_population, K, p):
        """Perform mutation on the new population."""
        for current_pop in new_population:
            for weight in current_pop.weights:
                weight += np.random.normal(0, K, size=weight.shape) * (np.random.random() < p)

            for bias in current_pop.biases:
                bias += np.random.normal(0, K, size=bias.shape) * (np.random.random() < p)

    def train(self, X, y, epochs, K, p, elit):
        """Performs training using Genetic Algorithm. """
        for i in range(1, epochs + 1):
            self._propagation(X, y)

            if i % 2000 == 0:  # Every 2000 iteration print current train error
                best_population = min(self.population, key=lambda nn: nn.mse)
                print(f"[Train error @{i}]: {best_population.mse}")

            # Elitism and selection
            elit_population = sorted(self.population, key=lambda nn: nn.mse)[:elit]
            new_population = self._crossing(elit_population)
            self._mutation(new_population, K, p)
            self.population = new_population.copy()

    def evaluate(self, X, y):
        """ Forward propagation on the best individual in the population """
        best_nn = min(self.population, key=lambda nn: nn.mse)
        total_mse = 0.0

        for x, target in zip(X, y):
            outputs = x

            for i, (weights, biases) in enumerate(zip(best_nn.weights, best_nn.biases)):
                outputs = np.dot(outputs, weights.T) + biases

                if i != len(best_nn.weights) - 1:  # Skip sigmoid for last layer
                    outputs = sigmoid(outputs)

            mse = np.mean(np.square(target - outputs))
            total_mse += mse

        return total_mse / len(X)
