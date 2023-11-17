from sys import argv

import id3_craftsman as ic


if __name__ == "__main__":
    train_filename = argv[1]  # Train dataset filename
    test_filename = argv[2]  # Test dataset filename

    train_dataset = ic.read_dataset(train_filename)
    test_dataset = ic.read_dataset(test_filename)
    
    if len(argv) == 4:
        depth = int(argv[3])
    else:
        depth = None

    model = ic.ID3(depth) # Construct model with depth hyperparameter
    model.fit(train_dataset)  # Learn the model
    predictions = model.predict(test_dataset)  # Generate predictions

    print("[PREDICTIONS]:" *predictions)
    ic.get_model_stat(predictions, test_dataset)