from math import log2


class ID3:
    class Leaf:
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return str(self.value)


    class Node:
        def __init__(self):
            self.name = None  # string
            self.next = None  # next node
            self.children = None  # children nodes
            self.depth = 1

        def __repr__(self):
            return str(self.name) + " {" + str(self.next) + "} " + str(
                self.children) + " " + str(self.depth)

    def __init__(self, train_data, feature_names, labels):
        self.X = train_data
        self.feature_names = feature_names
        self.labels = labels
        self.labelCategories = list(set(labels))
        self.labelCategoriesCount = [list(labels).count(x) for x in
                                     self.labelCategories]
        self.node = None
        self.entropy = self._get_entropy([x for x in range(
            len(self.labels))])  # calculates the initial entropy

    def fit(self):
        x_ids = [x for x in range(len(self.X))]
        feature_ids = [x for x in range(len(self.feature_names))]
        self.node = self._id3_recv(x_ids, feature_ids, self.node)
        print("\n[BRANCHES]:")
        self.print_tree(self.node)

    def predict(self, test_data, test_labels):
        solutions = []
        for row in test_data:
            nesto = dict()
            for index in range(len(row)):
                nesto[test_labels[index]] = row[index]
            solutions.append(self._make_prediction(nesto, self.node))
        return solutions

    def print_conf_mat(self, actual, predicted):
        unique = sorted(set(actual))
        matrix = [[0 for _ in unique] for _ in unique]

        map_labels = {key: i for i, key in enumerate(unique)}

        for p, a in zip(predicted, actual):
            matrix[map_labels[p]][map_labels[a]] += 1

        print("[CONFUSION_MATRIX]:")
        for x in range(len(unique)):
            for y in range(len(unique)):
                print(matrix[y][x], end=" ")
            print()

    def print_accuracy(self, predictions, actual_values):
        acc = list(zip(predictions, actual_values))
        i = 0
        for x in acc:
            if x[0] == x[1]:
                i += 1
        accuracy = i / len(predictions)
        print("[ACCURACY]: {:.5f}".format(accuracy))

    def _make_prediction(self, row, node):
        val = None
        if isinstance(node, Leaf):
            return node.value
        elif isinstance(node, Node):
            if node.name in row.keys():
                for i in node.children:
                    if i.name == row[node.name]:
                        val = self._make_prediction(row, i.next)
        return val

    def print_tree(self, node, result=""):
        if isinstance(node, Leaf):
            print("{}{}".format(result, node))
            return
        elif isinstance(node, Node):
            result += "{}:{}=".format(node.depth, node.name)
            for i in node.children:
                self.print_tree(i.next, result + "{} ".format(i.name))

    def _id3_recv(self, x_ids, feature_ids, node, depth=1):
        if not node:
            node = self.Node()  # initialize nodes

        labels_in_features = [self.labels[x] for x in x_ids]
        node.depth = depth
        if len(set(labels_in_features)) == 1:
            leaf = self.Leaf(self.labels[x_ids[0]])
            return leaf
        if len(feature_ids) == 0:
            leaf = self.Leaf(max(set(labels_in_features),
                            key=labels_in_features.count))
            return leaf
        best_feature_name, best_feature_id = self._get_feature_max_information_gain(
            x_ids, feature_ids)
        node.name = best_feature_name
        node.children = []
        # value of the chosen feature for each instance
        feature_values = list(set([self.X[x][best_feature_id] for x in x_ids]))
        # loop through all the values
        for value in feature_values:
            child = self.Node()
            child.name = value
            node.children.append(child)  # append new child node to current node
            child_x_ids = [x for x in x_ids if
                           self.X[x][best_feature_id] == value]
            if not child_x_ids:
                child.next = max(set(labels_in_features),
                                 key=labels_in_features.count)
            else:
                if feature_ids and best_feature_id in feature_ids:
                    to_remove = feature_ids.index(best_feature_id)
                    feature_ids.pop(to_remove)
                # recursively call the algorithm
                child.next = self._id3_recv(child_x_ids, feature_ids,
                                            child.next, depth + 1)

        return node

    def _get_entropy(self, x_ids):
        labels = [self.labels[i] for i in x_ids]  # sorted labels by instance id
        label_count = [labels.count(x) for x in self.labelCategories]
        entropy = sum(
            [-count / len(x_ids) * log2(count / len(x_ids)) if count else 0 for
             count in label_count])
        return entropy

    def _get_information_gain(self, x_ids, feature_id):
        info_gain = self._get_entropy(x_ids)  # calculate total entropy
        x_features = [self.X[x][feature_id] for x in x_ids]
        feature_vals = list(set(x_features))  # get unique values
        feature_vals_count = [x_features.count(x) for x in feature_vals]
        feature_vals_id = [
            [x_ids[i] for i, x in enumerate(x_features) if x == y] for y in
            feature_vals]
        info_gain = info_gain - sum(
            [val_counts / len(x_ids) * self._get_entropy(val_ids) for
             val_counts, val_ids in zip(feature_vals_count, feature_vals_id)])

        print("IG({})={:.4f}".format(self.feature_names[feature_id], info_gain),
              end=" ")
        return info_gain

    def _get_feature_max_information_gain(self, x_ids, feature_ids):
        features_entropy = [self._get_information_gain(x_ids, feature_id) for
                            feature_id in feature_ids]
        max_id = feature_ids[features_entropy.index(max(features_entropy))]

        return self.feature_names[max_id], max_id
