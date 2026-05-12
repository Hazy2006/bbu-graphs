import heapq
from Graph import Graph, read_from_file

def prim(graph, start):
    dist = {}
    prev = {}
    pq = []

    for x in graph.parse_outbound(start):
        cost = graph.get_cost(start, x)
        dist[x] = cost
        prev[x] = start
        heapq.heappush(pq, (cost, x))

    visited = {start}
    mst_edges = []
    total_cost = 0

    while pq:
        cost, x = heapq.heappop(pq)
        if x in visited:
            continue

        visited.add(x)
        mst_edges.append((prev[x], x, cost))
        total_cost += cost

        for y in graph.parse_outbound(x):
            if y not in visited:
                edge_cost = graph.get_cost(x, y)
                if y not in dist or edge_cost < dist[y]:
                    dist[y] = edge_cost
                    prev[y] = x
                    heapq.heappush(pq, (edge_cost, y))

    return mst_edges, total_cost