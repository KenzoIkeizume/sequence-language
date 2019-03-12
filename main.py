import json

from DataStructure.graph import Graph


class Language:
    def __init__(self, archive: str = "inputs.json"):

        archive = open(archive, "r")
        data = json.load(archive)

        self.inputs_production_rules = data["inputs_production_rules"]
        self.input_values = data["input_values"]
        self.variables = data["variables"]
        self.alphabet = data["alphabet"]
        self.initial_variable = data["initial_variable"]
        self.target_variable = data["target_variable"]

        self.production_rules = []

    def generate_product_rules(self):
        for production_rule in self.inputs_production_rules:
            key, array_values = production_rule.split("->")
            values = array_values.split("|")

            for value in values:
                if value == "&":
                    value = ""
                self.production_rules.append({key: value})

        print("production_rules: ", self.production_rules)

    def generate_sequence_language(self):
        replaced_value = self.initial_variable

        for input_value in self.input_values:
            current_value = self.production_rules[input_value - 1]
            print("current_value: ", current_value)

            variable = list(current_value.keys())[0]
            value = list(current_value.values())[0]

            replaced_value = replaced_value.replace(variable, value, 1)
            print("replaced_value: ", replaced_value)

    def generate_language_sequence(self):
        graph = Graph(self.production_rules)

        graph.breadth_first_search(self.initial_variable, self.target_variable)

        return graph

    def returned_path(self, graph: Graph):
        aux_node = graph.find_node(self.target_variable)

        while aux_node.name != self.initial_variable:
            aux_node = aux_node.parent

            print(aux_node.name)


if __name__ == '__main__':
    # mount language rules
    language = Language()
    language.generate_product_rules()

    # find generate sequence lenguage
    language.generate_sequence_language()

    # find generate language sequence
    mount_graph = language.generate_language_sequence()
    print("----")
    language.returned_path(mount_graph)
