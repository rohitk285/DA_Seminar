from collections import deque

def find_all_shortest_paths(graph, start, end):
    """
    Find all shortest paths between start and end using BFS.
    Returns a list of paths.
    """
    queue = deque([[start]])
    shortest_paths = []
    shortest_length = float('inf')

    while queue:
        path = queue.popleft()
        node = path[-1]

        # Stop exploring longer paths
        if len(path) > shortest_length:
            continue

        if node == end:
            if len(path) < shortest_length:
                shortest_length = len(path)
                shortest_paths = [path]
            elif len(path) == shortest_length:
                shortest_paths.append(path)
            continue

        for neighbor in graph[node]:
            if neighbor not in path:   # avoid cycles
                new_path = path + [neighbor]
                queue.append(new_path)

    return shortest_paths


def betweenness_centrality(graph):
    nodes = list(graph.keys())
    bc = {node: 0.0 for node in nodes}

    n = len(nodes)

    for i in range(n):
        for j in range(i + 1, n):
            s = nodes[i]
            t = nodes[j]

            shortest_paths = find_all_shortest_paths(graph, s, t)
            total_paths = len(shortest_paths)

            if total_paths == 0:
                continue

            for path in shortest_paths:
                # exclude src and trgt
                for node in path[1:-1]:
                    bc[node] += 1 / total_paths

    return bc


# Example graph
graph = {
    'A': ['B', 'E'],
    'B': ['A', 'C', 'D'],
    'C': ['B', 'D', 'F'],
    'D': ['B', 'C'],
    'E': ['A', 'F'],
    'F': ['C', 'E']
}

result = betweenness_centrality(graph)

print("Betweenness Centrality:")
for node, value in result.items():
    print(f"{node}: {value:.2f}")