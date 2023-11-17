import csv


def read_dataset(filepath):
    with open(file=filepath, mode="r") as f:
        reader = csv.DictReader(f=f)


def get_model_stat(predictions, real_values):
    accuracy = 0.0

    # TODO add accuracy calculating logic
    print(f"[ACCURACY]: {accuracy:.5f}")

    print("[CONFUSION_MATRIX]:")
    # TODO add double for loop to print rest of confusion matrix


class ID3():
    def __init__(self, depth):
        self._depth = depth
    
    def fit(train_dataset):
        pass

    def predict(test_dataset):
        pass
