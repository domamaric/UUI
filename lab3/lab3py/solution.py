import csv
import sys

import id3_craftsman as id3


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        read_data = [x.strip().split(',') for x in f.readlines()]

    data = read_data[1:]
    attributes = read_data[0]

    new_samples = []
    actual_values = []
    with open(sys.argv[2], 'r') as f2:
        reader = csv.DictReader(f2)
        for row in reader:
            key, value = row.popitem()
            actual_values.append(value)
            new_samples.append(row)

    model = id3.ID3()
    model.fit(data, attributes)
    predictions = model.predict(new_samples)
    print("[PREDICTIONS]:", *predictions)
    id3.get_model_stats(actual_values, predictions)
