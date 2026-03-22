from collections import deque, defaultdict
import copy

def edge_betweenness(graph):
    betweenness = defaultdict(float)

    for s in graph:
        stack = []
        pred = {w: [] for w in graph}
        sigma = dict.fromkeys(graph, 0)
        sigma[s] = 1
        dist = dict.fromkeys(graph, -1)
        dist[s] = 0

        queue = deque([s])

        while queue:
            v = queue.popleft()
            stack.append(v)
            for w in graph[v]:
                if dist[w] < 0:
                    queue.append(w)
                    dist[w] = dist[v] + 1
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]
                    pred[w].append(v)

        delta = dict.fromkeys(graph, 0)

        while stack:
            w = stack.pop()
            for v in pred[w]:
                c = (sigma[v] / sigma[w]) * (1 + delta[w])
                edge = tuple(sorted((v, w)))
                betweenness[edge] += c
                delta[v] += c

    for edge in betweenness:
        betweenness[edge] /= 2

    return betweenness


def remove_edge(graph, edge):
    u, v = edge
    if v in graph[u]:
        graph[u].remove(v)
    if u in graph[v]:
        graph[v].remove(u)


def connected_components(graph):
    visited = set()
    components = []

    for node in graph:
        if node not in visited:
            comp = []
            queue = deque([node])
            visited.add(node)

            while queue:
                v = queue.popleft()
                comp.append(v)
                for nei in graph[v]:
                    if nei not in visited:
                        visited.add(nei)
                        queue.append(nei)

            components.append(comp)

    return components


def girvan_newman(graph):
    g = copy.deepcopy(graph)  #creating deep copy of graph

    step = 1
    while True:
        print(f"\nStep {step}: Edge Betweenness Centrality")
        eb = edge_betweenness(g)

        for edge, val in sorted(eb.items()):
            print(f"{edge}: {val:.4f}")

        if not eb:
            break

        max_edge = max(eb, key=eb.get)
        print(f"\nRemoving edge with highest betweenness: {max_edge}")

        remove_edge(g, max_edge)

        components = connected_components(g)
        print("Current Communities:", components)

        if len(components) > 1:
            return components

        step += 1


graph = {
    0: [1,2],
    1: [0,2,3],
    2: [0,1],
    3: [1,4,5,6],
    4: [3,5],
    5: [3,4,6],
    6: [3,5]
}

communities = girvan_newman(graph)

print("\nFinal Communities:")
for c in communities:
    print(c)