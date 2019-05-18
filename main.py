import json
from enum import Enum

from DataStructure.graph import Graph


class State(Enum):
    MARKED = 1
    UNMARKED = 2


_EMPTY = "EMPTY"


class Language:
    def __init__(self, archive: str = "inputs.json"):

        self.graph = Graph()
        self.new_graph = Graph()
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
        self.generate_new_graph()

    def generate_new_graph(self):
        pushed_nodes = []

        # find the selected nodes
        for line in range(0, len(self.nodes) - 1):
            for column in range(1 + line, len(self.nodes)):
                line_name = self.nodes[line]
                column_name = self.nodes[column]

                position_table = self.get_set(line_name, column_name)

                if self.table[position_table] is State.UNMARKED:
                    self.new_graph.add_node(position_table)
                    pushed_nodes.append(line_name)
                    pushed_nodes.append(column_name)

        # add in graph all nodes not inserted by unmarked
        for node in self.graph.nodes:
            if node.name not in pushed_nodes:
                self.new_graph.add_node(node.name)

        # make a conection between nodes
        for node in self.new_graph.nodes:
            node_begin_name, node_end_name = self.split_new_node(node.name)

            node_begin = self.graph.find_node(node_begin_name)
            node_end = self.graph.find_node(node_end_name)

            for edge in node_begin.edges:
                for new_node in self.new_graph.nodes:
                    search_begin_name, search_end_name = self.split_new_node(new_node.name)

                    if search_end_name and edge.target.name == search_end_name:
                        if not self.has_edge_in_new_graph(node, new_node, edge.info):
                            node.add_edge(new_node, edge.info)

                    if edge.target.name == search_begin_name:
                        if not self.has_edge_in_new_graph(node, new_node, edge.info):
                            node.add_edge(new_node, edge.info)

            if node_end:
                for edge in node_end.edges:
                    for new_node in self.new_graph.nodes:
                        search_begin_name, search_end_name = self.split_new_node(new_node.name)

                        if search_end_name and edge.target.name == search_end_name:
                            if not self.has_edge_in_new_graph(node, new_node, edge.info):
                                node.add_edge(new_node, edge.info)

                        if edge.target.name == search_begin_name:
                            if not self.has_edge_in_new_graph(node, new_node, edge.info):
                                node.add_edge(new_node, edge.info)

    def has_edge_in_new_graph(self, node, new_node, info):
        for validate_node in self.new_graph.nodes:
            for validate_edge in validate_node.edges:
                if validate_node.name == node.name \
                        and validate_edge.target.name == new_node.name\
                        and validate_edge.info == info:
                    return True
        return False

    def generate_table(self):
        # loop in nodes to mount the initial table
        for line in range(0, len(self.nodes) - 1):
            for column in range(1 + line, len(self.nodes)):
                line_name = self.nodes[line]
                column_name = self.nodes[column]

                position_table = self.get_set(line_name, column_name)

                self.table[position_table] = self.mark_node_final(line_name, column_name)

        marked_nodes = True

        while marked_nodes:
            will_mark = []

            # loop for find the father nodes
            for line in range(0, len(self.nodes) - 1):
                for column in range(1 + line, len(self.nodes)):
                    line_name = self.nodes[line]
                    column_name = self.nodes[column]

                    position_table = self.get_set(line_name, column_name)

                    if self.table[position_table] is State.UNMARKED:
                        will_mark.append(self.mark_father_node(line_name, column_name))

            if all(will_mark):
                print(self.table)
                marked_nodes = False

    def mark_father_node(self, begin, end):
        marked_nodes = True
        # find a node that have a father to mark
        node_begin = self.graph.find_node(begin)
        node_end = self.graph.find_node(end)

        for consume in self.alphabet:
            consume_node_begin = self.find_consume_node(node_begin, consume)
            consume_node_end = self.find_consume_node(node_end, consume)

            position_table = self.get_set(consume_node_begin.name, consume_node_end.name)

            if self.table.get(position_table, _EMPTY) is not _EMPTY:
                if self.table[position_table] is State.MARKED:
                    position_table_target = self.get_set(node_begin.name, node_end.name)
                    self.table[position_table_target] = State.MARKED
                    marked_nodes = False

        return marked_nodes

    def find_consume_node(self, node, consume):
        for edge in node.edges:
            if edge.info is consume:
                return edge.target

        return None

    def mark_node_final(self, begin, end):
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

    @staticmethod
    def get_set(begin, end):
        return "{}|{}".format(begin, end)

    @staticmethod
    def split_new_node(node_name):
        returned_node_names = node_name.split('|')

        if len(returned_node_names) == 1:
            return [returned_node_names[0], None]

        return returned_node_names


if __name__ == '__main__':
    # mount language rules
    language = Language()
    language.graph.list_edges()

    language.minimization_table()
    print('------------------------------')
    language.new_graph.list_edges()