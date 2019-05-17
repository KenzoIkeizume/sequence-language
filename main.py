import json
from enum import Enum

from DataStructure.graph import Graph


class State(Enum):
    MARKED = 1
    UNMARKED = 2
    WAIT = 3


class Language:
    def __init__(self, archive: str = "inputs.json"):

        self.graph = Graph()
        self.table = {}
        self.unmarked_path = []

        # read the json file
        archive = open(archive, "r")
        data = json.load(archive)

        self.alphabet = data["alphabet"]
        self.nodes = data["nodes"]
        self.linked_edges = data["&"]
        self.initial_node = data["initial_node"]
        self.final_nodes = data["final_nodes"]

        self.mount_graph()

    def mount_graph(self):
        # add nodes
        for node_name in self.nodes:
            self.graph.add_node(node_name=node_name)

        # add edges
        for node in self.graph.nodes:
            list_edges = self.linked_edges[node.name]

            for edge_obj in list_edges:
                key = list(edge_obj.keys())[0]
                value = list(edge_obj.values())[0]

                target_node = self.graph.find_node(key)

                node.add_edge(target_node, value)

    def minimization_table(self):
        self.generate_table()
        self.reverse_final()

    def generate_table(self):
        # loop in nodes to mount the table
        for line in range(0, len(self.nodes)-1):
            for column in range(1+line, len(self.nodes)):
                line_name = self.nodes[line]
                column_name = self.nodes[column]

                position_table = line_name+column_name

                self.table[position_table] = self.mark_node(line_name, column_name)

    def mark_node(self, begin, end):
        # mark if the not is different
        if not self.is_final(begin) and self.is_final(end):
            return State.MARKED
        if self.is_final(begin) and not self.is_final(end):
            return State.MARKED
        else:
            return State.UNMARKED

    def is_final(self, node_name):
        # validate if the node is final
        return node_name in self.final_nodes

    def reverse_final(self):
        # reverse the fianl states in table
        for node in self.graph.nodes:
            for state in self.alphabet:
                self.consume(node, state)

    def consume(self, node, state):
        # find the consume of the state
        for edge in node.edges:
            if edge.info is state:
                return edge.target

        return None


if __name__ == '__main__':

    # mount language rules
    language = Language()
    language.graph.list_edges()

    language.minimization_table()

