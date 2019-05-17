from DataStructure.edge import Edge


class Node:

    def __init__(self, name: str, info: str = ""):
        self.name = name
        self.parent = None
        self.visited = False
        self.info = info
        self.edges = []

    def add_edge(self, target, info: str):
        self.edges.append(Edge(self, target, info))

    def __eq__(self, other):
        return self.name == other.name

    def __cmp__(self, other):
        if self.name < other.name:
            return -1
        elif self.name > other.name:
            return 1
        else:
            return 0

    def __lt__(self, other):
        return self.name < other.name
