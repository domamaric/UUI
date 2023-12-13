import csv
import pathlib
import sys

import id3_craftsman as id3


def read_train(filepath):
    with open(filepath) as f:
        data = [row for row in csv.reader(f)]
    return data


def read_test(filepath):
    with open(filepath) as f:
        new_samples, actual_values = [], []
        reader = csv.DictReader(f)
        for row in reader:
            _, val = row.popitem()
            new_samples.append(row)
            actual_values.append(val)
    return new_samples, actual_values


if __name__ == '__main__':    
    train_filepath = pathlib.Path(sys.argv[1])
    test_filepath = pathlib.Path(sys.argv[2])

    train_dataset = read_train(train_filepath)
    test_dataset, actual_values = read_test(test_filepath)

    model = id3.ID3()
    model.fit(train_dataset)
    predictions = model.predict(test_dataset)
    print("[PREDICTIONS]:", *predictions)
    id3.get_model_stats(actual_values, predictions)
