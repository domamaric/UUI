import heapq
from collections import deque

from node import Node


class Algorithm:
    def __init__(self, name, initial, transitions, final_states, heuristic=None):
        self._name = name
        self._initial = Node(initial, 1, None)
        self._transitions = transitions
        self._final_states = [Node(x, None, None) for x in final_states]
        self._open_bfs = deque()
        self._open_bfs.append(self._initial)
        self._open_ucs = []
        heapq.heappush(self._open_ucs, (0.0, self._initial))
        # Statistike za ispis na konzoli
        self._heuristic = heuristic
        self._found = "no"
        self._length = 0
        self._price = 0.0
        self._visited = set()
        self._path = deque()

    def print_info(self):
        print("# {}\n[FOUND_SOLUTION]: {}\n[STATES_VISITED]: {}".format(self._name, self._found,
                                                                        len(self._visited)))
        print("[PATH_LENGTH]: {}\n[TOTAL_COST]: {}".format(self._length, round(self._price, 1)))
        print("[PATH]: {}".format(" => ".join(self._path)))

    def bfs(self):
        while self._open_bfs:
            n = self._open_bfs.popleft()
            if n in self._final_states:
                self._found = "yes"
                self._length = n.depth
                self._reconstruct(n)
                return n

            self._visited.add(n.state)
            for m in self._expand_bfs(n):
                if m.state not in self._visited:
                    self._open_bfs.append(m)
        return False

    def ucs(self):
        while self._open_ucs:
            cost, state = heapq.heappop(self._open_ucs)
            if state in self._final_states:
                self._found = "yes"
                self._length = state.depth
                self._reconstruct(state)
                return state

            self._visited.add(state.state)
            for m in self._expand_ucs(state, cost):
                if m[1].state not in self._visited:
                    heapq.heappush(self._open_ucs, m)
        return False

    def _expand_ucs(self, node, cost):
        ret = set()
        for n in self._transitions[node.state]:
            next_state, next_cost = n.split(",")
            ret.add((float(next_cost) + cost, Node(next_state, node.depth + 1, node)))
        return ret

    def _expand_bfs(self, node):
        ret = set()
        for n in self._transitions[node.state]:
            next_state, cost = n.split(",")
            ret.add(Node(next_state, node.depth + 1, node))
        return ret

    def _reconstruct(self, node):
        self._path.appendleft(node.state)
        p = node.parent
        if p.parent is None:
            self._path.appendleft(p.state)
            return
        self._reconstruct(p)

    def cumulative_price(self):
        for i in range(len(self._path)):
            next_states = self._transitions[self._path[i]]
            try:
                for x in next_states:
                    next_state, cost = x.split(",")
                    if next_state.startswith(self._path[i + 1]):
                        self._price += float(cost)
            except IndexError:
                break

    def astar(self):
        while self._open_ucs:
            cost, state = heapq.heappop(self._open_ucs)
            if state in self._final_states:
                self._found = "yes"
                self._length = state.depth
                self._reconstruct(state)
                return state

            self._visited.add((cost, state))
            for m in self._expand_ucs(state, cost):
                for m_slash in set(self._open_ucs).union(self._visited):
                    if m_slash[1] == m[1]:  # state(m') = state(m)
                        if m_slash[0] < m[0]:
                            continue
                        else:
                            try:
                                self._visited.remove(m_slash)
                                heapq.heappush(self._open_ucs, m_slash)
                            except KeyError:
                                pass
                        break

                heuristic = self._heuristic[m[1].state]
                heapq.heappush(self._open_ucs, (heuristic + m[0], m[1]))
        return False

    def fetch_price(self):
        return self._price
