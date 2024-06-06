import math
import numpy as np
import random


def sigmoid(x):
    """Calculate sigmoid value of value x."""
    return 1 / (1 + np.exp(-x))


def load_csv(filepath):
    """Read csv file and split it into features and targets."""
    data = np.loadtxt(filepath, delimiter=",", skiprows=1)
    X, Y = data[:, :-1], data[:, -1]
    return X, Y


class NeuralNetwork:
    """Neural network class implementation with random initialization."""

    def __init__(self, input_dim, hidden_dims, output_dim):
        self.mse = float("inf")
        layer_dims = [input_dim] + hidden_dims + [output_dim]
        self.weights = [np.random.normal(0, 0.01, (layer_dims[i + 1], layer_dims[i]))
                        for i in range(len(layer_dims) - 1)]
        self.biases = [np.random.normal(0, 0.01, (layer_dims[i + 1]))
                       for i in range(len(layer_dims) - 1)]

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
        self.popsize = popsize
        self.population = [NeuralNetwork(input_dim, hidden_dims, output_dim)
                           for _ in range(popsize)]

    def __repr__(self):
        return "\n".join(str(nn) for nn in self.population)

    def __str__(self):
        return "\n".join(str(nn) for nn in self.population)

    def _propagation(self, X, y):
        """Performs forward propagation for each neural network."""
        for nn in self.population:
            total_mse = 0.0

            for x, target in zip(X, y):
                outputs = x

                for i, (weights, biases) in enumerate(zip(nn.weights, nn.biases)):
                    outputs = np.dot(outputs, weights.T) + biases
                    if i != len(nn.weights) - 1:  # Skip sigmoid for last layer
                        outputs = sigmoid(outputs)
                total_mse += np.mean(np.square(target - outputs))

            nn.mse = total_mse / len(X)

    def _crossing(self, elit_population):
        """Perform crossing for generating new individuals."""
        def arithmetic_mean(pair):
            return [(w1 + w2) / 2 for w1, w2 in zip(*pair)]

        new_population = []
        while len(new_population) < self.popsize:
            nn1 = random.choice(elit_population)
            nn2 = random.choice(elit_population)

            new_nn = self._create_neural_network(arithmetic_mean((nn1.weights, nn2.weights)),
                                                arithmetic_mean((nn1.biases, nn2.biases)))
            new_population.append(new_nn)
        return new_population

    def _mutation(self, new_population, K, p):
        """Perform mutation on the new population."""
        for nn in new_population:
            for weights in nn.weights:
                mutation_mask = np.random.random(weights.shape) < p
                weights += np.random.normal(0, K, weights.shape) * mutation_mask

            for biases in nn.biases:
                mutation_mask = np.random.random(biases.shape) < p
                biases += np.random.normal(0, K, biases.shape) * mutation_mask

    def train(self, X, y, epochs, K, p, elit):
        """Performs training using Genetic Algorithm."""
        for i in range(1, epochs + 1):
            self._propagation(X, y)

            if i % 2000 == 0:  # Every 2000 iterations, print current train error
                best_population = min(self.population, key=lambda nn: nn.mse)
                print(f"[Train error @{i}]: {best_population.mse}")

            # Elitism and selection
            elit_population = sorted(self.population, key=lambda nn: nn.mse)[:elit]
            new_population = self._crossing(elit_population)
            self._mutation(new_population, K, p)
            self.population = new_population

    def evaluate(self, X, y):
        """Forward propagation on the best individual in the population"""
        best_nn = min(self.population, key=lambda nn: nn.mse)
        total_mse = 0.0

        for x, target in zip(X, y):
            outputs = x
            for i, (weights, biases) in enumerate(zip(best_nn.weights, best_nn.biases)):
                outputs = np.dot(outputs, weights.T) + biases
                if i != len(best_nn.weights) - 1:  # Skip sigmoid for last layer
                    outputs = sigmoid(outputs)
            total_mse += np.mean(np.square(target - outputs))

        return total_mse / len(X)

    def _create_neural_network(self, weights, biases):
        """Create a neural network with given weights and biases."""
        new_nn = NeuralNetwork(self.input_dim, self.hidden_dims, self.output_dim)
        new_nn.weights = weights
        new_nn.biases = biases
        return new_nn
