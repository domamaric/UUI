import argparse
import os
import pathlib  # It is better to provide Path object than pure string
import pathfinder
import pprint


def main(argv):
    sts, initial, target = pathfinder.read_space_state(pathlib.Path(argv.ss))
    search_alg = argv.alg

    # pprint.pprint(sts)

    if search_alg == 'bfs':
        algorithm = pathfinder.Bfs(sts)
    elif search_alg == 'ucs':
        algorithm = pathfinder.Ucs(sts)
    elif search_alg == 'astar':
        heuristic = pathfinder.read_heuristic(pathlib.Path(argv.h))
        algorithm = pathfinder.Astar(sts, heuristic)

    # Do a state search
    path, cost = algorithm.search(initial, target)
    if path is not None:
        print('[FOUND_SOLUTION]: yes')
        print('[STATES_VISITED]:', 10)
        print('[PATH_LENGTH]:', len(path))
        print('[TOTAL_COST]:', cost)
        print('[PATH]:', ' => '.join(path))
    else:
        print('[FOUND_SOLUTION]: no')
        print('[STATES_VISITED]:', 0)
        print('[PATH_LENGTH]: 0')
        print('[TOTAL_COST]:', cost)
        print('[PATH]:')

    if argv.check_optimistic:
        pass
    if argv.check_consistent:
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='solution.py',
                                     description='State space search analysis')
    parser.add_argument('--alg', choices=['bfs', 'ucs', 'astar'], help='')
    parser.add_argument('--ss', help='')
    parser.add_argument('--h', help='')
    parser.add_argument('--check-optimistic', action='store_true', help='')
    parser.add_argument('--check-consistent', action='store_true', help='')
    main(parser.parse_args())
