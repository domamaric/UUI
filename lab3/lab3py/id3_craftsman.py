import csv
import math


def read_dataset(filepath):
    with open(file=filepath, mode="r") as f:
        reader = csv.reader(f)
        columns = []
        for row in reader:
            if columns:
                for i, value in enumerate(row):
                    columns[i].append(value)
            else:  # Handle the first row by initializing columns
                columns = [[value] for value in row]
        # Convert the data into a column-major 2D array
    return {c[0]: c[1:] for c in columns}


def get_model_stat(predictions, real_values):
    accuracy = 0.0

    # TODO add accuracy calculating logic
    print(f"[ACCURACY]: {accuracy:.5f}")

    print("[CONFUSION_MATRIX]:")
    # TODO add double for loop to print rest of confusion matrix


class ID3:
    def __init__(self, depth):
        self._depth = depth
        self._root = None

    def fit(self, train_data):
        X = list(train_data.keys())
        y = X[-1]
        X.remove(y)
        self._root = self._id3_recv(train_data, X, y)

    def _id3_recv(self, D, X, y):
        if not D or len(set(D[y])) == 1:  # If D is empty or pure
            v = max(set(D[y]), key=D[y].count)
            return v  # Return leaf(v)

        if not X:
            v = max(set(D[y]), key=D[y].count)
            return v  # Return leaf(v)

        x = self.find_best_attribute(D, X)  # Fix: Call using self.
        subtree = {x: {}}
        values = set(D[x])

        for v in values:
            new_X = [attr for attr in X if attr != x]
            subset_D = {key: [val for val, label in zip(D[x], D[y]) if val == v] for key, val in D.items()}
            subtree[x][v] = self._id3_recv(subset_D, new_X, y)

        return subtree

    def find_best_attribute(self, D, X):  # Fix: Define as a method.
        pass

    def predict(self, test_data):
        pass
