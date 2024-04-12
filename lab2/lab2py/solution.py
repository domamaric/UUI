"""Main Script

Skripta sadrzi poboljsanjo izdanje mojega rjesenja s prethodne ak. godine.
"""

import sys
import pathlib

import logic_reasoning


if __name__ == "__main__":
    # First flag indicates task, [resolution, cooking]

    if sys.argv[1] == "resolution":
        list_of_clauses, goal_clause = logic_reasoning.parse_clauses(pathlib.Path(sys.argv[2]))
        check_valid = logic_reasoning.pl_resolution(list_of_clauses, goal_clause)

        if check_valid:
            print(f"[CONCLUSION]: {' v '.join(goal_clause)} is true")
        else:
            print(F"[CONCLUSION]: {' v '.join(goal_clause)} is unknown")

    elif sys.argv[1] == "cooking":
        print("Constructed with knowledge:")

        list_of_clauses, goal_clause = logic_reasoning.parse_clauses(pathlib.Path(sys.argv[2]))
        list_of_clauses += [goal_clause]
        user_commands = logic_reasoning.parse_user_commands(pathlib.Path(sys.argv[3]))

        for cmd in user_commands:
            clause = cmd[:-2].split(' v ')
            action = cmd[-1]

            if action == '+':
                list_of_clauses.append(clause)
            elif action == '-':
                list_of_clauses.remove(clause)
            elif action == '?':
                res = logic_reasoning.pl_resolution(list_of_clauses, clause)
                if res:
                    print(f"[CONCLUSION]: {' v '.join(clause)} is true")
                else:
                    print(F"[CONCLUSION]: {' v '.join(clause)} is unknown")
    else:
        print("[ERROR]: Invalid task name")
