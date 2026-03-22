def findIntersection(adj, u, v):
    count = 0
    for it in adj[u]:
        if it in adj[v]:
            count += 1
    return count

def findUnion(adj, u, v):
    unique_nodes = set()
    for it in adj[u]:
        unique_nodes.add(it)
    for it in adj[v]:
        unique_nodes.add(it)
    return len(unique_nodes)

adj = [[2, 3, 6], [3, 4, 6], [0, 3], [0, 1, 2, 4, 5], [1, 5, 7], [3, 4, 7], [0, 1], [4, 5]]
n = len(adj)
node_pairs = []

# finding all pairs of nodes that are not connected
for i in range(n):
    for j in range(i + 1, n):
        if j not in adj[i]:
            node_pairs.append((i, j))

res = 0.0
ans = []

# calculating Jaccard coefficient for each pair of nodes
for u, v in node_pairs:
    intersection_count = findIntersection(adj, u, v)
    union_count = findUnion(adj, u, v)

    if union_count != 0:
        jac = intersection_count / union_count
    else:
        jac = 0.0

    if jac > res:
        res = jac
        ans = [(u, v)]
    elif jac == res:
        ans.append((u, v))

    print(f"({u},{v}): {jac}")

print("Maximum Jaccard Similarity:", res)
print("Predicted Link:")
for u, v in ans:
    print(f"{u}-{v}")