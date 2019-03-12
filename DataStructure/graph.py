from queue import Queue

from DataStructure.node import Node


class Graph:

    def __init__(self, production_rules: list = []):
        self.nodes = []
        self.production_rules = production_rules

    def breadth_first_search(self, begin: str, end: str):
        queue = Queue()

        self.add_node(begin)
        node_begin = self.find_node(begin)

        queue.put(node_begin)

        while queue.qsize() > 0:

            node_aux = queue.get()
            print(node_aux.name)

            if node_aux.name == end:
                return True

            neighbours_node = self.set_neighbours(node_aux.name)

            for node in neighbours_node:
                node.parent = node_aux

                queue.put(node)

        return False

    def set_neighbours(self, node_name: str):
        neighbours = []

        for prodution_rule in self.production_rules:
            variable = list(prodution_rule.keys())[0]
            value = list(prodution_rule.values())[0]

            if variable in node_name:
                replaced_value = node_name.replace(variable, value, 1)

                if self.find_node(replaced_value) is None:
                    self.nodes.append(Node(replaced_value))
                    node = self.find_node(replaced_value)
                    neighbours.append(node)

        return neighbours

    def add_node(self, node_name: str):
        node = Node(node_name)
        self.nodes.append(node)

    def find_node(self, node_name: str):
        for node in self.nodes:
            if node.name == node_name:
                return node
        return None
