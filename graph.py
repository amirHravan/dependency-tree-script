class Graph:
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        if self._find_node(node.node_name) is None:
            self.nodes.append(node)

    def _find_node(self, node_name):
        for node in self.nodes:
            if node.node_name == node_name:
                return node
        return None

    def add_edge(self, node_from, node_to):
        first_node = self._find_node(node_from)
        second_node = self._find_node(node_to)
        if first_node is not None and second_node is not None:
            first_node.add_children(second_node)

    def __str__(self):
        return f"{self.nodes}"

    def __repr__(self):
        return f"{self.nodes}"


class Node:
    def __init__(self, node_name, node_type):
        self.node_name = node_name
        self.node_type = node_type
        self.children = []

    def add_children(self, node):
        if node not in self.children:
            self.children.append(node)

    def __str__(self):
        return f"{self.node_name}: {self.children}\n"

    def __repr__(self):
        return f"\n{self.node_name}: {self.children}"
