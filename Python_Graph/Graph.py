import random

class Graph:
    def __init__(self, n = 0):
        """Initialize a graph with n vertices."""
        self.__vertices = set()
        self.__outbounds = {}
        self.__inbounds = {}
        self.__costs = {}

        for i in range(n):
            self.__vertices.add(i)
            self.__outbounds[i] = []
            self.__inbounds[i] = []

    def count_vertices(self):
        """Return the number of vertices in the graph."""
        return len(self.__vertices)

    def count_edges(self):
        """Return the number of edges in the graph."""
        return len(self.__costs)

    def is_edge(self, x, y):
        """Check if there is an edge from x to y."""
        if x not in self.__vertices:
            raise ValueError("Vertex x does not exist.")
        if y not in self.__vertices:
            raise ValueError("Vertex y does not exist.")
        return (x, y) in self.__costs

    def add_edge(self, x, y, cost):
        """Add an edge from x to y with the given cost."""
        if x not in self.__vertices:
            raise ValueError("Vertex x does not exist.")
        if y not in self.__vertices:
            raise ValueError("Vertex y does not exist.")
        if (x, y) in self.__costs:
            raise ValueError("Edge already exists.")
        self.__outbounds[x].append(y)
        self.__inbounds[y].append(x)
        self.__costs[(x, y)] = cost

    def remove_edge(self, x, y):
        """Remove the edge from x to y."""
        if x not in self.__vertices:
            raise ValueError("Vertex x does not exist.")
        if y not in self.__vertices:
            raise ValueError("Vertex y does not exist.")
        if (x, y) not in self.__costs:
            raise ValueError("Edge does not exist.")
        del self.__costs[(x, y)]
        self.__outbounds[x].remove(y)
        self.__inbounds[y].remove(x)

    def add_vertex(self, x=None):
        """Add a new vertex. If x is None, auto-assign the next available id."""
        if x is None:
            x = max(self.__vertices) + 1 if self.__vertices else 0
        if x in self.__vertices:
            raise ValueError("Vertex already exists.")
        self.__vertices.add(x)
        self.__outbounds[x] = []
        self.__inbounds[x] = []
        return x

    def remove_vertex(self, x):
        """Remove vertex x and all its incident edges."""
        if x not in self.__vertices:
            raise ValueError("Vertex does not exist.")
        for y in list(self.__outbounds[x]):
            del self.__costs[(x, y)]
            self.__inbounds[y].remove(x)
        for y in list(self.__inbounds[x]):
            del self.__costs[(y, x)]
            self.__outbounds[y].remove(x)
        del self.__outbounds[x]
        del self.__inbounds[x]
        self.__vertices.remove(x)

    def in_degree(self, x):
        """Return the in-degree of vertex x."""
        if x not in self.__vertices:
            raise ValueError("Vertex does not exist.")
        return len(self.__inbounds[x])

    def out_degree(self, x):
        """Return the out-degree of vertex x."""
        if x not in self.__vertices:
            raise ValueError("Vertex does not exist.")
        return len(self.__outbounds[x])

    def get_cost(self, x, y):
        """Return the cost of the edge from x to y."""
        if x not in self.__vertices:
            raise ValueError("Vertex x does not exist.")
        if y not in self.__vertices:
            raise ValueError("Vertex y does not exist.")
        if (x, y) not in self.__costs:
            raise ValueError("Edge does not exist.")
        return self.__costs[(x, y)]

    def set_cost(self, x, y, cost):
        """Update the cost of the edge from x to y."""
        if x not in self.__vertices:
            raise ValueError("Vertex x does not exist.")
        if y not in self.__vertices:
            raise ValueError("Vertex y does not exist.")
        if (x, y) not in self.__costs:
            raise ValueError("Edge does not exist.")
        self.__costs[(x, y)] = cost

    def parse_vertices(self):
        """Iterate over all vertices in the graph."""
        for vertex in self.__vertices:
            yield vertex

    def parse_inbound(self, x):
        """Iterate over all inbound neighbors of vertex x."""
        if x not in self.__vertices:
            raise ValueError("Vertex does not exist.")
        for vertex in self.__inbounds[x]:
            yield vertex

    def parse_outbound(self, x):
        """Iterate over all outbound neighbors of vertex x."""
        if x not in self.__vertices:
            raise ValueError("Vertex does not exist.")
        for vertex in self.__outbounds[x]:
            yield vertex

    def copy_graph(self):
        """Return a deep copy of the graph."""
        new_graph = Graph(0)
        new_graph.__vertices = set(self.__vertices)
        new_graph.__outbounds = {k: list(v) for k, v in self.__outbounds.items()}
        new_graph.__inbounds = {k: list(v) for k, v in self.__inbounds.items()}
        new_graph.__costs = dict(self.__costs)
        return new_graph


def read_from_file(filename):
    """Read a graph from a file and return it."""
    with open(filename, "r") as f:
        parts = f.readline().split()
        n, m = int(parts[0]), int(parts[1])
        g = Graph(n)
        for i in range(m):
            parts = f.readline().split()
            x, y, cost = int(parts[0]), int(parts[1]), int(parts[2])
            g.add_edge(x, y, cost)
    return g


def write_to_file(graph, filename):
    """Write the graph to a file."""
    with open(filename, "w") as f:
        f.write(f"{graph.count_vertices()} {graph.count_edges()}\n")
        for x in graph.parse_vertices():
            for y in graph.parse_outbound(x):
                cost = graph.get_cost(x, y)
                f.write(f"{x} {y} {cost}\n")


def random_graph(n, m):
    """Generate a random graph with n vertices and m edges."""
    g = Graph(n)
    edges = set()
    while len(edges) < m:
        x = random.randint(0, n - 1)
        y = random.randint(0, n - 1)
        if x != y and (x, y) not in edges:
            cost = random.randint(1, 100)
            g.add_edge(x, y, cost)
            edges.add((x, y))
    return g