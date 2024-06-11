import argparse
import pathlib

import antsys


def main(argv):
    filepath = pathlib.Path(argv.path)
    cities = antsys.read_csv(filepath)

    # --alpha 1.2 --beta 3 --decay 0.8 --ants 30 provides best solution so far
    ant_colony = antsys.AntColony(epochs=argv.epochs, alpha=argv.alpha,
                                  beta=argv.beta, decay=argv.decay, ant_count=argv.ants)
    best_solution, cost = ant_colony.fit(cities)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="solution.py",
                                     description="Ant colony optimization algorithm "
                                     "for solving traveling salesman problem.")
    parser.add_argument("--path", help="path to cities file")
    parser.add_argument("--epochs", help="number of training epochs (defaults to 20)",
                        default=20, type=int)
    parser.add_argument("--alpha", help="exponent on pheromone (defaults to 1.0)",
                        default=1.0, type=float)
    parser.add_argument("--beta", help="exponent on distance (defaults to 1.0)",
                        default=1.0, type=float)
    parser.add_argument("--decay", help="rate in which pheromone decays (defaults to 1.0)",
                        default=1.0, type=float)
    parser.add_argument("--ants", help="number of ants (defaults to 10)", default=10, type=int)
    main(parser.parse_args())
