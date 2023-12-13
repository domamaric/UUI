import heapq
import math

from collections import Counter


class ID3():
    def __init__(self):
        self.decision_tree = None
        self.labels = None

    def entropy(self, data):
        labels = [item[-1] for item in data]
        label_counts = Counter(labels)
        entropy_value = 0.0
        total_samples = len(data)

        for count in label_counts.values():
            probability = count / total_samples
            entropy_value -= probability * math.log2(probability)

        return entropy_value

    def split_data(self, data, attribute_index, attribute_value):
        split_data = []

        for item in data:
            if item[attribute_index] == attribute_value:
                reduced_item = item[:attribute_index] + \
                    item[attribute_index + 1:]
                split_data.append(reduced_item)

        return split_data

    def select_best_attribute(self, data):
        num_attrs = len(data[0]) - 1
        current_entropy = self.entropy(data)
        best_info_gain = 0.0
        best_attribute = -1

        for i in range(num_attrs):
            attribute_values = [item[i] for item in data]
            unique_values = set(attribute_values)
            new_entropy = 0.0

            for value in unique_values:
                sub_data = self.split_data(data, i, value)
                probability = len(sub_data) / float(len(data))
                new_entropy += probability * self.entropy(sub_data)

            info_gain = current_entropy - new_entropy

            if info_gain > best_info_gain:
                best_info_gain = info_gain
                best_attribute = i

        return best_attribute


    def create_decision_tree(self, data, attributes):
        labels = [item[-1] for item in data]

        if labels.count(labels[0]) == len(labels):
            return labels[0]

        best_attribute = self.select_best_attribute(data)
        best_attribute_label = attributes[best_attribute]
        decision_tree = {best_attribute_label: {}}

        attribute_values = [item[best_attribute] for item in data]
        unique_values = set(attribute_values)

        for value in unique_values:
            sub_attributes = attributes[:best_attribute] + \
                attributes[best_attribute + 1:]
            sub_data = self.split_data(data, best_attribute, value)
            decision_tree[best_attribute_label][value] = self.create_decision_tree(
                sub_data, sub_attributes)

        return decision_tree

    def fit(self, train_data):
        attributes = train_data[0]
        data = train_data[1:]
        self.labels = [row[-1] for row in data]
        heapq.heapify(self.labels)  # Linear complexity instead of n*logn

        self.decision_tree = self.create_decision_tree(data, attributes)
        print("[BRANCHES]:")
        self.print_tree(self.decision_tree)

    def predict_single(self, sample, decision_tree):
        if not isinstance(decision_tree, dict):
            return decision_tree

        attribute = list(decision_tree.keys())[0]
        value = sample[attribute]

        if value not in decision_tree[attribute]:
            label_counts = Counter(self.labels)
            majority_labels = label_counts.most_common(1)[0][0]
            return majority_labels

        subtree = decision_tree[attribute][value]
        return self.predict_single(sample, subtree)

    def predict(self, samples):
        predictions = []

        for sample in samples:
            prediction = self.predict_single(sample, self.decision_tree)
            predictions.append(prediction)

        return predictions


    def print_tree(self, decision_tree, depth=1, path=""):
        root = list(decision_tree.keys())[0]
        subtree = decision_tree[root]
        path += f"{depth}:{root}"
        
        for key in subtree:
            if isinstance(subtree[key], dict):
                self.print_tree(subtree[key], depth + 1, path + f"={key} ")
            elif isinstance(subtree[key], str):
                print(f"{path}={key} {subtree[key]}")


def create_conf_matrix(actual, predicted):
    unique = sorted(set(actual))
    matrix = [[sum(1 for p, a in zip(predicted, actual) if p == y and a == x) for x in unique] for y in unique]
    return matrix


def get_model_stats(actual_values, predictions):
    accuracy = sum(1 for x in zip(predictions, actual_values) if x[0] == x[1]) / len(predictions)
    print("[ACCURACY]: {:.5f}".format(accuracy))

    confusion_matrix = create_conf_matrix(actual_values, predictions)
    unique = set(actual_values)
    print("[CONFUSION_MATRIX]:")
    for x in range(len(unique)):
        for y in range(len(unique)):
            print(confusion_matrix[y][x], end=" ")
        print()

