def transitions_parser(filepath):
    start_state = None
    goal_states = []
    transitions = {}

    with open(filepath, "r") as f:
        file_lines = [line.rstrip() for line in f.readlines() if line[0] != "#"]

    start_state, goal_states = file_lines[0], file_lines[1].split()

    for line in file_lines[2:]:
        current_state, transitions_part = line.split(':', 1)
        current_state = current_state.strip()
        
        if current_state not in transitions:
            transitions[current_state] = []
        
        for transition in transitions_part.strip().split():

            next_state, cost = transition.rsplit(',', 1)
            transitions[current_state].append((next_state, float(cost)))

    return start_state, goal_states, transitions


def heuristics_parser(filepath):
    with open(filepath, "r") as f:
        file_lines = [line.rstrip() for line in f.readlines() if line[0] != "#"]
    
    heuristics = {}

    for line in file_lines:
        state, cost = line.split(':')
        state = state.strip()
        cost = cost.strip()
        heuristics[state] = float(cost)

    return heuristics
