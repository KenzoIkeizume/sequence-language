from queue import Queue

from DataStructure.node import Node


class Graph:

    def __init__(self, production_rules: list = []):
        self.nodes = []
        self.production_rules = production_rules

    def list_edges(self):
        edges = []
        for node in self.nodes:
            for edge in node.edges:
                print(edge.str_edge())
                edges.append(edge)

    def add_node(self, node_name: str):
        node = Node(node_name)
        self.nodes.append(node)

    def find_node(self, node_name: str):
        for node in self.nodes:
            if node.name == node_name:
                return node
        return None

    def clear_visited(self):
        for node in self.nodes:
            node.visited = False