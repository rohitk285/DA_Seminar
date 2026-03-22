import heapq

def dijkstra(adj, src, dest):
    n = len(adj)
    dist = [float('inf')] * n
    dist[src] = 0
    pq = [(0, src)]

    while pq:
        d, node = heapq.heappop(pq)

        if node == dest:
            return d

        for adjNode in adj[node]:
            if d + 1 < dist[adjNode]:
                dist[adjNode] = d + 1
                heapq.heappush(pq, (dist[adjNode], adjNode))

    return -1


adj = [[2, 4], [2], [0, 1, 3], [2, 4], [0, 3]]
n = len(adj)

maxi = 0
node_ans = []

for i in range(n):
    dist_sum = 0
    for j in range(n):
        if i == j:
            continue
        dist_ij = dijkstra(adj, i, j)
        dist_sum += dist_ij

    closeness_centrality = (n - 1) / dist_sum

    if closeness_centrality > maxi:
        maxi = closeness_centrality
        node_ans = [i]
    elif closeness_centrality == maxi:
        node_ans.append(i)

    print(f"Closeness Centrality of node {i}: {closeness_centrality}")

print("Node(s) with maximum closeness centrality:")
for node in node_ans:
    print(f"Node {node}")