import argparse
import nnlearn


def main(argv):
    X_train, Y_train = nnlearn.load_csv(argv.train)
    X_test, Y_test = nnlearn.load_csv(argv.test)

    input_dim = len(X_train[0])

    # Cascade through nn architecture
    if argv.nn == '5s':
        hidden_dims = [5]
    elif argv.nn == '20s':
        hidden_dims = [20]
    elif argv.nn == '5s5s':
        hidden_dims = [5, 5]

    population = nnlearn.Population(popsize=argv.popsize, input_dim=input_dim,
                                    hidden_dims=hidden_dims, output_dim=1)

    population.train(X=X_train, y=Y_train, epochs=argv.iter,
                     K=argv.K, p=argv.p, elit=argv.elitism)

    error = population.evaluate(X_test, Y_test)
    print(f"[Test error]: {error}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='solution.py',
                                     description=('Program for learning an '
                                                  'artificial neural network '
                                                  'by means of genetic algo.'))
    parser.add_argument('--train', help='path to the training dataset')
    parser.add_argument('--test', help='path to the test dataset')
    parser.add_argument('--nn', help='the neural network architecture',
                        choices=['5s', '20s', '5s5s'])
    parser.add_argument('--popsize', help='the population size for gen. algo.',
                        type=int)
    parser.add_argument('--elitism', help='the elitism od the gen. algo.',
                        type=int)
    parser.add_argument('--p', help=('the mutation probability of each '
                                     'chromosome element'),
                        type=float)
    parser.add_argument('--K', help=('the standard deviation of the mutation '
                                     'Gaussian noise'), type=float)
    parser.add_argument('--iter', help='the number of gen. algo. iterations',
                        type=int)
    main(parser.parse_args())
