# Ovaj je kod moje autorsko djelo od prošle godine koji sam izmijenio da skoro pa svi slucajevi rade :)
import argparse

from algorithm import Algorithm


def main(argv):
    if argv.ss is not None:
        with open(argv.ss, encoding='utf-8') as f:
            lines = [x.strip() for x in f.readlines() if not x.startswith("#")]
            initial_state = lines[0]
            final_states = set(lines[1].split())
            transitions = dict()
            for line in lines[2:]:
                state, neighbours = line.split(":")
                transitions[state] = {x for x in neighbours.split()}
    if argv.h is not None:
        with open(argv.h, encoding='utf-8') as f:
            lines = [x.strip() for x in f.readlines() if not x.startswith("#")]
            heuristic = dict()
            for line in lines:
                state, heuristic_val = line.split(":")
                heuristic[state] = float(heuristic_val)
    # Komentari su izbačeni, te se sada prva linija sadržava početno stanje,
    # a druga sadrži ciljna stanja
    if argv.alg == "bfs":
        b = Algorithm("BFS", initial_state, transitions, final_states)
        b.bfs()
        b.cumulative_price()
        b.print_info()
    elif argv.alg == "ucs":
        u = Algorithm("UCS", initial_state, transitions, final_states)
        u.ucs()
        u.cumulative_price()
        u.print_info()
    elif argv.alg == "astar":
        a = Algorithm("ASTAR", initial_state, transitions, final_states, heuristic)
        a.astar()
        a.cumulative_price()
        a.print_info()
    elif argv.check_optimistic:
        print("# HEURISTIC-OPTIMISTIC {}".format(argv.h))
        no_of_errors = 0
        for k, v in heuristic.items():
            try:
                alg = Algorithm("UCS", k, transitions, final_states)
                alg.ucs()
                alg.cumulative_price()
                if v <= alg.fetch_price():
                    print("[CONDITION]: [OK] h({}) <= h*: {} <= {}".format(k, v, alg.fetch_price()))
                else:
                    print("[CONDITION]: [ERR] h({}) <= h*: {} <= {}".format(k, v, alg.fetch_price()))
                    no_of_errors += 1
            except AttributeError:
                print("[CONDITION]: [OK] h({}) <= h*: {} <= {}".format(k, v, v))
        if no_of_errors == 0:  # Ispis zakljucka
            print("[CONCLUSION]: Heuristic is optimistic.")
        else:
            print("[CONCLUSION]: Heuristic is not optimistic.")
    elif argv.check_consistent:
        print("# HEURISTIC-CONSISTENT {}".format(argv.h))
        no_of_errors = 0

        for state, transit in transitions.items():
            for x in transit:
                st, c = x.split(',')
                c = float(c)
                for k, heuristic_val in heuristic.items():
                    if k == state:
                        for y, h2 in heuristic.items():
                            if y == st:
                                if heuristic_val <= h2 + c:
                                    print(
                                        "[CONDITION]: [OK] h({}) <= h({}) + c: {} <= {} + {}".format(
                                            k, st, heuristic_val, h2, c))
                                else:
                                    print(
                                        "[CONDITION]: [ERR] h({}) <= h({}) + c: {} <= {} + {}".format(
                                            k, st, heuristic_val, h2, c))
                                    no_of_errors += 1
                                break
                        break
        if no_of_errors == 0:  # Ispis zakljucka
            print("[CONCLUSION]: Heuristic is consistent.")
        else:
            print("[CONCLUSION]: Heuristic is not consistent.")
    else:
        print("Oops something went wrong :'(")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--alg', type=str, help="Kratica za algoritam pretraživanja",
                        choices=['bfs', 'ucs', 'astar'])
    parser.add_argument('--ss', type=str, help="Putanja do opisnika prostora stanja")
    parser.add_argument('--h', type=str, help="Putanja do opisnika heuristike")
    parser.add_argument('--check-optimistic', '--check_optimistic',
                        action='store_true', help="Zastavica za provjeru optimističnosti heuristike")
    parser.add_argument('--check-consistent', '--check_consistent',
                        action='store_true', help="Zastavica za provjeru konzistentnosti heuristike")
    main(parser.parse_args())
