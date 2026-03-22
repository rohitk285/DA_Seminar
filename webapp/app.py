from flask import Flask, render_template, request, jsonify
import json
import os
import sys
from importlib.machinery import SourceFileLoader
import networkx as nx

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def load_module(path, name):
    return SourceFileLoader(name, path).load_module()

# Paths to existing scripts in the workspace
BETWEEN_PATH = os.path.join(BASE_DIR, 'Centrality_Analysis', 'betweenness.py')
CLOSENESS_PATH = os.path.join(BASE_DIR, 'Centrality_Analysis', 'closeness.py')
JAC_PATH = os.path.join(BASE_DIR, 'Link_Prediction', 'JAC.py')
PAC_PATH = os.path.join(BASE_DIR, 'Link_Prediction', 'PAC.py')
GIRVAN_PATH = os.path.join(BASE_DIR, 'Community_Detection', 'girvan.py')

bet_mod = load_module(BETWEEN_PATH, 'betweenness_mod')
clos_mod = load_module(CLOSENESS_PATH, 'closeness_mod')
jac_mod = load_module(JAC_PATH, 'jac_mod')
pac_mod = load_module(PAC_PATH, 'pac_mod')
girvan_mod = load_module(GIRVAN_PATH, 'girvan_mod')

app = Flask(__name__, template_folder='templates', static_folder='static')


def parse_adj_input(text):
    """Try to parse adjacency input as JSON. Accept either dict or list-of-lists."""
    try:
        data = json.loads(text)
        return data
    except Exception:
        # try simple line-based parser: each line: node: n1,n2,...
        graph = {}
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        for idx, line in enumerate(lines):
            if ':' in line:
                key, rest = line.split(':', 1)
                key = key.strip()
                neigh = [r.strip() for r in rest.split(',') if r.strip()]
                graph[key] = neigh
            else:
                parts = [p.strip() for p in line.split() if p.strip()]
                graph[str(idx)] = parts
        return graph


def to_index_adj(data):
    """Convert various adjacency representations to list-of-lists with integer node ids."""
    if isinstance(data, dict):
        # keys may be strings or ints
        keys = list(data.keys())
        mapping = {k: i for i, k in enumerate(keys)}
        n = len(keys)
        adj = [[] for _ in range(n)]
        for k, neigh in data.items():
            i = mapping[k]
            for v in neigh:
                if v in mapping:
                    adj[i].append(mapping[v])
                else:
                    # try parse as int or match by label
                    try:
                        vi = int(v)
                        if 0 <= vi < n:
                            adj[i].append(vi)
                    except Exception:
                        pass
        return adj, mapping
    elif isinstance(data, list):
        return data, {i: i for i in range(len(data))}
    else:
        return [], {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/compute', methods=['POST'])
def compute():
    payload = request.get_json() or {}
    adj_text = payload.get('adjacency', '')
    algo = payload.get('algorithm')

    parsed = parse_adj_input(adj_text)
    adj_list, mapping = to_index_adj(parsed)

    # Build graph dict mapping labels to neighbor labels for betweenness/girvan
    rev_mapping = {v: k for k, v in mapping.items()}
    graph_dict = {}
    for i, neigh in enumerate(adj_list):
        label = rev_mapping.get(i, str(i))
        graph_dict[label] = [rev_mapping.get(j, str(j)) for j in neigh]

    G = nx.Graph()
    for i in range(len(adj_list)):
        G.add_node(rev_mapping.get(i, str(i)))
    for i, neigh in enumerate(adj_list):
        for j in neigh:
            u = rev_mapping.get(i, str(i))
            v = rev_mapping.get(j, str(j))
            G.add_edge(u, v)

    pos = nx.spring_layout(G, seed=42)

    result = {'nodes': [], 'edges': [], 'metric': None}
    for node, p in pos.items():
        result['nodes'].append({'id': node, 'x': float(p[0]), 'y': float(p[1])})
    for u, v in G.edges():
        result['edges'].append({'source': u, 'target': v})

    if algo == 'betweenness':
        try:
            bc = bet_mod.betweenness_centrality(graph_dict)
            result['metric'] = {'betweenness': bc}
        except Exception as e:
            result['error'] = str(e)
    elif algo == 'closeness':
        try:
            # reuse dijkstra from clos_mod
            n = len(adj_list)
            clos = {}
            for i in range(n):
                dist_sum = 0
                for j in range(n):
                    if i == j:
                        continue
                    d = clos_mod.dijkstra(adj_list, i, j)
                    if d < 0:
                        d = float('inf')
                    dist_sum += d
                if dist_sum == 0 or dist_sum == float('inf'):
                    clos_val = 0
                else:
                    clos_val = (n - 1) / dist_sum
                clos[rev_mapping.get(i, str(i))] = clos_val
            result['metric'] = {'closeness': clos}
        except Exception as e:
            result['error'] = str(e)
    elif algo == 'jaccard':
        try:
            n = len(adj_list)
            pairs = []
            for i in range(n):
                for j in range(i + 1, n):
                    if j not in adj_list[i]:
                        inter = jac_mod.findIntersection(adj_list, i, j)
                        uni = jac_mod.findUnion(adj_list, i, j)
                        jac = inter / uni if uni != 0 else 0.0
                        pairs.append({'pair': (rev_mapping.get(i), rev_mapping.get(j)), 'jaccard': jac})
            result['metric'] = {'jaccard_pairs': pairs}
        except Exception as e:
            result['error'] = str(e)
    elif algo == 'preferential':
        try:
            n = len(adj_list)
            degree = [len(adj_list[i]) for i in range(n)]
            pairs = []
            for i in range(n):
                for j in range(i + 1, n):
                    if j not in adj_list[i]:
                        pac = degree[i] * degree[j]
                        pairs.append({'pair': (rev_mapping.get(i), rev_mapping.get(j)), 'pac': pac})
            result['metric'] = {'preferential_pairs': pairs}
        except Exception as e:
            result['error'] = str(e)
    elif algo == 'girvan':
        try:
            # girvan_newman expects dict with int keys in original script; it handles ints
            # our graph_dict has labels -> labels; but girvan_mod.girvan_newman will work with int keys,
            # so create int-key graph
            int_graph = {i: adj_list[i][:] for i in range(len(adj_list))}
            communities = girvan_mod.girvan_newman(int_graph)
            # map back to labels
            mapped = [[rev_mapping.get(node, str(node)) for node in comp] for comp in communities]
            result['metric'] = {'communities': mapped}
        except Exception as e:
            result['error'] = str(e)
    else:
        result['error'] = 'Unknown algorithm'

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
