from collections import deque

def bfs(adj, start, end):
    shortest_paths = []
    q = deque([[start]])
    mini = float('inf')

    while q:
        path = q.popleft()
        node = path[-1]

        if len(path) > mini:
            continue

        if node == end:
            if len(path) < mini:
                mini = len(path)
                shortest_paths = [path]
            elif len(path) == mini:
                shortest_paths.append(path)
            continue

        for adjNode in adj[node]:
            if adjNode not in path:
                new_path = path.copy()
                new_path.append(adjNode)
                q.append(new_path)

    return shortest_paths


adj = [[2, 4], [2], [0, 1, 3], [2, 4], [0, 3]]

n = len(adj)

for i in range(n):
    betweenness_node_total = 0

    for j in range(n):
        for k in range(j + 1, n):
            if i == j or i == k:
                continue

            paths = bfs(adj, j, k)
            denominator = len(paths)
            if denominator == 0:
                continue

            numerator = 0

            for path in paths:
                if i in path:
                    numerator += 1

            betweenness = numerator / denominator
            betweenness_node_total += betweenness

    print(f"Betweenness Centrality of node {i} is: {betweenness_node_total}")