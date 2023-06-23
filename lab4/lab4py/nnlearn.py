import csv
import numpy as np


def load_csv(filepath):
    """
    Read csv file and split it data and labels.

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


class NeuralNetwork:
    def __init__(self):
        pass
