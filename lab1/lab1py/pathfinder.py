import heapq

from collections import deque


def is_optimistic(heuristic, state_space, goal):
    no_of_errors = 0

    for state, val in heuristic.items():
        try:
            algorithm = Ucs(state_space)
            _, cost = algorithm.search(state, goal)
            cost = float(cost)
            if val <= cost:
                print(
                    f"[CONDITION]: [OK] h({state}) <= h*: {val} <= {cost}")
            else:
                print(f"[CONDITION]: [ERR] h({state}) <= h*: {val} <= {cost}")
                no_of_errors += 1
        except AttributeError:
            print(f"[CONDITION]: [OK] h({state}) <= h*: {val} <= {val}")

    return no_of_errors == 0


def is_consistent(heuristic, state_space):
    no_of_errors = 0

    for state, transitions in state_space.items():
        state_heuristic = heuristic.get(state)

        if state_heuristic is not None:
            for successor_state, cost in transitions:
                successor_heuristic = heuristic.get(successor_state)
                if successor_heuristic is not None and state_heuristic > successor_heuristic + cost:
                    print(f"[CONDITION]: [ERR] h({state}) <= h({successor_state}) + c: {state_heuristic} <= {successor_heuristic} + {cost}")
                    no_of_errors += 1
                else:
                    print(f"[CONDITION]: [OK] h({state}) <= h({successor_state}) + c: {state_heuristic} <= {successor_heuristic} + {cost}")

    return no_of_errors == 0


class Algorithm:
    def __init__(self, state_space):
        self.state_space = state_space

    def search(self, start_state, goal_state):
        raise NotImplementedError("Subclasses must implement search method!")

    def reconstruct_path(self, parent, node):
        path = [node]

        while node in parent:
            node = parent[node]
            path.append(node)
        path.reverse()

        return path


class Bfs(Algorithm):
    def __init__(self, state_space):
        super().__init__(state_space)

    def search(self, start, goal):
        queue = deque([(start, [])])
        visited = set()
        parent = {}

        while queue:
            current_node, path = queue.popleft()
            if current_node in goal:
                return path + [current_node], 0.0

            visited.add(current_node)

            for successor, _ in self.state_space[current_node]:
                if successor not in visited:
                    queue.append((successor, path + [current_node]))
                    parent[successor] = current_node

        return None


class Ucs(Algorithm):
    def __init__(self, state_space):
        super().__init__(state_space)

    def search(self, start, goal):
        priority_queue = [(0, start)]
        visited = set()
        g = {start: 0}
        parent = {}

        goal_set = set(goal)  # Convert goal to a set for faster membership check

        while priority_queue:
            _, current_node = heapq.heappop(priority_queue)

            if current_node in goal_set:
                return super().reconstruct_path(parent, current_node), g[current_node]

            visited.add(current_node)

            for successor, cost in self.state_space[current_node]:
                new_cost = g[current_node] + cost
                successor_cost = g.get(successor, float('inf'))

                if successor not in visited and new_cost < successor_cost:
                    g[successor] = new_cost
                    heapq.heappush(priority_queue, (new_cost, successor))
                    parent[successor] = current_node

        return None


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
            _, current_node = heapq.heappop(open_set)

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
