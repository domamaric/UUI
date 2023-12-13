from ferlearn import ID3
import koalas as kl
import sys


def main():
    train_dataset = kl.read_csv(sys.argv[1])
    validation_dataset = kl.read_csv(sys.argv[2])
    depth = None

    try:
        depth = sys.argv[3]
    except IndexError as e:
        pass

    model = ID3(train_data=train_dataset.x_train,
                feature_names=train_dataset.features,
                labels=train_dataset.y_train)
    model.fit()
    predictions = model.predict(test_data=validation_dataset.x_train,
                                test_labels=validation_dataset.features)

    print("[PREDICTIONS]:", *predictions)
    model.print_accuracy(predictions, validation_dataset.y_train)
    model.print_conf_mat(validation_dataset.y_train, predictions)


if __name__ == '__main__':
    main()
