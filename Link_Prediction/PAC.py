adj = [[2, 3, 6], [3, 4, 6], [0, 3], [0, 1, 2, 4, 5], [1, 3, 5, 7], [3, 4, 7], [0, 1], [4, 5]]
n = len(adj)
node_pairs = []
degree = [0] * n

#finding all pairs of nodes that are not connected
for i in range(n):
    for j in range(i + 1, n):
        if j not in adj[i]:
            node_pairs.append((i, j))

for i in range(n):
    degree[i] = len(adj[i])

res = 0
ans = []

# calculating PAC for each pair of nodes that are not connected
for u, v in node_pairs:
    pac = degree[u] * degree[v]
    if pac > res:
        res = pac
        ans = [(u, v)]
    elif pac == res:
        ans.append((u, v))
    print(f"({u},{v}): {pac}")

print("Maximum Product of Degrees:", res)
print("Predicted Link:")
for u, v in ans:
    print(f"{u}-{v}")