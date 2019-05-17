class Edge:

    def __init__(self, source, target, info: str = ""):
        self.source = source
        self.target = target
        self.info = info

    def str_edge(self):
        return "{} => {} : {}".format(self.source.name, self.target.name, self.info)
