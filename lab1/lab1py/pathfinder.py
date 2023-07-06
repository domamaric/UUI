import heapq


def read_space_state(path):
    successor_dict = {}
    initial_state = None
    target_states = []

    with open(path, 'r') as f:
        file_lines = remove_comments([x for x in f.readlines()])

        initial_state = file_lines[0]
        target_states = file_lines[1].split()

        for line in file_lines[2:]:
            state, successors = line.split(':')
            state = state.strip()
            successors = successors.strip().split()
            successor_list = []

            for successor in successors:
                next_state, cost = successor.split(',')
                successor_list.append((next_state, float(cost)))
            successor_dict[state] = successor_list

    return successor_dict, initial_state, target_states


def read_heuristic(path):
    heuristic_dict = {}

    with open(path, 'r') as f:
        file_lines = remove_comments([x for x in f.readlines()])
        for line in file_lines:
            state, cost = line.split(':')
            state = state.strip()
            cost = cost.strip()
            heuristic_dict[state] = float(cost)

    return heuristic_dict


def remove_comments(file_lines):
    removed_comments = []

    for line in file_lines:
        if not line.startswith('#'):
            removed_comments.append(line.strip())

    return removed_comments


class Algorithm:
    def __init__(self, state_space):
        self.state_space = state_space

    def search(self, start_state, goal_state):
        raise NotImplementedError("Subclasses must implement search method")

    def reconstruct_path(self, parent, node):
        path = [node]

        while node in parent:
            node = parent[node]
            path.append(node)
        path.reverse()

        return path


class Astar(Algorithm):
    def __init__(self, state_space, heuristic):
        super().__init__(state_space)
        self._heuristic = heuristic

    def search(self, start, goal):
        open_set = [(0 + self._heuristic[start], start)]
        closed_set = set()
        g = {start: 0}
        parent = {}

        while open_set:
            current_cost, current_node = heapq.heappop(open_set)

            if current_node in goal:
                return super().reconstruct_path(parent, current_node), g[current_node]

            closed_set.add(current_node)

            for successor, cost in self.state_space[current_node]:
                if successor in closed_set:
                    continue

                new_cost = g[current_node] + cost
                if successor not in g or new_cost <= g[successor]:
                    g[successor] = new_cost
                    f = new_cost + self._heuristic[successor]
                    heapq.heappush(open_set, (f, successor))
                    parent[successor] = current_node

        return None, 0.0
