"""Module for performing resolution refutation in propositional logic.

This module provides functions for performing resolution refutation in 
propositional logic. The main function 'pl_resolution' attempts to resolve
a given list of clauses with a goal clause. It iteratively applies resolution
steps until a contradiction or the absence of progress is encountered.

Functions:
    - pl_resolution(list_of_clauses, goal_clause): 
        Attempts to resolve a list of clauses with a goal clause.
        Returns True if a contradiction is found, False otherwise.
    - parse_user_commands(filepath):
        Parses user commands from a file.
        Returns a list of parsed commands.
    - parse_clauses(filepath):
        Parses clauses from a file.
        Returns a tuple containing a list of parsed clauses and the goal clause.
"""

from itertools import combinations


def pl_resolution(list_of_clauses, goal_clause):
    """Perform resolution refutation on a list of clauses."""
    set_of_support = [[_negate(literal)] for literal in goal_clause]
    visited = set()

    while True:
        set_of_support, new = _remove_redundant(set_of_support), []

        if not set_of_support:
            return False

        for c1, c2 in _select_clauses(list_of_clauses, set_of_support):
            resolvents = _pl_resolve(c1, c2)
            if "NIL" in resolvents:
                return True

            if resolvents and tuple(resolvents) not in visited:
                visited.add(tuple(resolvents))
                new.append(resolvents)

                for clause in new:
                    print(f"{' v '.join(clause)} ({' v '.join(c1)}, {' v '.join(c2)})")

        if not new:
            return False

        new = _remove_redundant(new)

        if all(tuple(clause) in set(map(tuple, set_of_support)) for clause in new):
            return False

        set_of_support += new
        print("==============")

def _select_clauses(clauses, sos):
    """ Selects a set of clause pairs to resolve."""
    selected = [(clause, s) for clause in clauses for s in sos]
    selected += list(combinations(sos, 2))

    return selected

def _pl_resolve(c1, c2):
    """Resolves parent clauses and returns a set of resolvents."""
    if len(c1) == 1 == len(c2) and c1[0] == _negate(c2[0]):
        return ["NIL"]

    if not any(_negate(literal) in c2 for literal in c1):
        return []

    resolvents = set()

    c1_negations = {_negate(literal) for literal in c1}
    c2_negations = {_negate(literal) for literal in c2}

    resolvents.update(literal for literal in c1 if literal not in c2_negations)
    resolvents.update(literal for literal in c2 if literal not in c1_negations)

    return list(resolvents)

def _negate(literal):
    """ Returns literal negation."""
    return literal[1:] if literal[0] == '~' else '~' + literal

def _remove_redundant(clauses):
    """ Removes clauses subsumed by others, tautologies and duplicate clauses"""
    tmp = set()
    tmp.update(
        list(set(map(tuple, clauses)))
    )
    tmp.update(
        {i for i, clause in enumerate(clauses) if any(_negate(lit) in clause for lit in clause)}
    )
    tmp.update(
        {j for i, c1 in enumerate(clauses) for j, c2 in enumerate(clauses) if i != j and set(c1).issubset(c2)}
    )

    return [clauses[i] for i in range(len(clauses)) if i not in tmp]

def parse_user_commands(filepath):
    with open(filepath, mode="r", encoding="utf-8") as f:
        file_lines = _remove_comments(f.readlines())

    return file_lines

def parse_clauses(filepath):
    with open(filepath, mode="r", encoding="utf-8") as f:
        file_lines = _remove_comments(f.readlines())

        print('\n'.join(file_lines))
        print("==============")

        file_lines = [line.split(" v ") for line in file_lines]

    return file_lines[:-1], file_lines[-1]

def _remove_comments(file_lines):
    return [line.lower().strip() for line in file_lines if not line.startswith('#')]
