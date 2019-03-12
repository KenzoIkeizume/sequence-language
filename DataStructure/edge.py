from DataStructure.node import Node


class Edge:

    def __init__(self, source: Node, target: Node, cost: float = 0):
        self.source = source
        self.target = target
        self.cost = cost
