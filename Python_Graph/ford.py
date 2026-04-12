def ford(graph, s, t):
    #1. initialize dist and prev
    #2. relax all edges n-1 times
    #3. check for negative cycle on nth iteration
    #4. reconstruct and return path

    # Validate that source and target vertices exist in the graph
    vertices = set(graph.parse_vertices())
    if s not in vertices:
        return "invalid_vertex", None
    if t not in vertices:
        return "invalid_vertex", None

    dist = {}
    prev = {}
    for x in graph.parse_vertices():
        dist[x] = float('inf')
    dist[s] = 0
    changed = True
    iteration = 0
    while changed:
        changed = False
        iteration+=1
        for x in graph.parse_vertices():
            for y in graph.parse_outbound(x):
                if dist[x] + graph.get_cost(x,y) < dist[y]:
                   dist[y] = dist[x] + graph.get_cost(x, y)
                   prev[y] = x
                   changed = True
        if iteration == graph.count_vertices():
            return "negative_cycle", None # there exists a negative cost cycle
    if dist[t] == float('inf'):
        return "no_path", None #t is unreachable from s
    path = []
    current  = t
    while current != s:
        path.append(current)
        current = prev[current]
    path.append(s)
    path.reverse()
    return path, dist[t]