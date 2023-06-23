import argparse
import nnlearn


def main(argv):
    X_train = nnlearn.load_csv(argv.train)
    X_test = nnlearn.load_csv(argv.test)
    breakpoint()
    input_dim = len(X_train[0]) - 1

    # Cascade through nn architecture
    if argv.nn == '5s':
        nn = nnlearn.NeuralNetwork(input_dim=input_dim,
                                   hidden_dims=[5],
                                   output_dim=1)
    elif argv.nn == '20s':
        nn = nnlearn.NeuralNetwork(input_dim=input_dim,
                                   hidden_dims=[20],
                                   output_dim=1)
    elif argv.nn == '5s5s':
        nn = nnlearn.NeuralNetwork(input_dim=input_dim,
                                   hidden_dims=[5, 5],
                                   output_dim=1)

    nn.train(data=X_train, k=argv.K, epochs=argv.iter, popsize=argv.popsize,
             prob=argv.p, elit=argv.elitism)


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
