class Node:
    def __init__(self, state, depth, parent):
        self.state = state
        self.depth = depth
        self.parent = parent

    def __str__(self):
        return "State: {}, depth: {}, parent: {}".format(self.state, self.depth, self.parent)

    def __eq__(self, other):
        return True if self.state == other.state else False

    def __lt__(self, other):
        return self.state < other.state

    def __hash__(self):
        return hash((self.state, self.depth, self.parent))
