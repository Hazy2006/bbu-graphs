from Graph import Graph
 
 
def neighbors_undirected(g, x):
    """Yield all neighbors of x treating the directed graph as undirected."""
    seen = set()
    for y in g.parse_outbound(x):
        if y not in seen:
            seen.add(y)
            yield y
    for y in g.parse_inbound(x):
        if y not in seen:
            seen.add(y)
            yield y
 
 
def bfs_component(g, start, visited):
    """
    BFS from `start` using undirected neighborhood.
    Marks all reached vertices in the shared `visited` set.
    Returns the set of vertices in this component.
    """
    component_vertices = set()
    queue = [start]
    visited.add(start)
    head = 0
    while head < len(queue):
        x = queue[head]
        head += 1
        component_vertices.add(x)
        for y in neighbors_undirected(g, x):
            if y not in visited:
                visited.add(y)
                queue.append(y)
    return component_vertices
 
 
def build_component_graph(g, vertices):
    """
    Build and return a new Graph object from a subset of vertices,
    preserving all edges (with original costs) between them.
    """
    comp = Graph(0)
    for v in vertices:
        comp.add_vertex(v)
    for v in vertices:
        for u in g.parse_outbound(v):
            if u in vertices:
                comp.add_edge(v, u, g.get_cost(v, u))
    return comp
 
 
def connected_components(g):
    """
    Find all connected components of graph g treated as undirected.
    Returns a list of Graph objects, one per component.
    """
    visited = set()
    components = []
    for v in g.parse_vertices():
        if v not in visited:
            comp_vertices = bfs_component(g, v, visited)
            components.append(build_component_graph(g, comp_vertices))
    return components