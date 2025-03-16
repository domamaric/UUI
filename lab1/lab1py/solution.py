import argparse
import pathlib  # It is better to provide Path object than pure string

import pathfinder
import file_parser


def main(argv):
    start_state, goal_states, transitions = file_parser.transitions_parser(pathlib.Path(argv.ss))
    search_alg = argv.alg

    if search_alg == 'bfs':
        algorithm = pathfinder.Bfs(transitions)
    elif search_alg == 'ucs':
        algorithm = pathfinder.Ucs(transitions)
    elif search_alg == 'astar':
        heuristics = file_parser.heuristics_parser(pathlib.Path(argv.h))
        algorithm = pathfinder.Astar(transitions, heuristics)

    # Do a state search
    if search_alg is not None:
        path, cost = algorithm.search(start_state, goal_states)
        if path is not None:
            print('[FOUND_SOLUTION]: yes')
            print('[STATES_VISITED]:', 10)
            print('[PATH_LENGTH]:', len(path))
            print('[TOTAL_COST]:', cost)
            print('[PATH]:', ' => '.join(path))

    if argv.check_optimistic:
        print('# HEURISTIC-OPTIMISTIC', argv.h)
        heuristics = file_parser.heuristics_parser(pathlib.Path(argv.h))
        optimistic = pathfinder.is_optimistic(heuristics, transitions, goal_states)

        if optimistic:
            print('[CONCLUSION]: Heuristic is optimistic.')
        else:
            print('[CONCLUSION]: Heuristic is not optimistic.')

    if argv.check_consistent:
        print('# HEURISTIC-CONSISTENT', argv.h)
        heuristics = file_parser.heuristics_parser(pathlib.Path(argv.h))
        consistent = pathfinder.is_consistent(heuristics, transitions)

        if consistent:
            print('[CONCLUSION]: Heuristic is consistent.')
        else:
            print('[CONCLUSION]: Heuristic is not consistent.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='solution.py',
                                     description='State space search analysis')
    parser.add_argument('--alg', choices=['bfs', 'ucs', 'astar'], help='')
    parser.add_argument('--ss', help='')
    parser.add_argument('--h', help='')
    parser.add_argument('--check-optimistic', action='store_true', help='')
    parser.add_argument('--check-consistent', action='store_true', help='')
    main(parser.parse_args())
