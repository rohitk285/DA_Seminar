# Graph Analysis Webapp

Small Flask app that reuses existing Python scripts in this workspace to compute:
- Betweenness centrality
- Closeness centrality
- Jaccard coefficient (JAC)
- Preferential attachment (PAC)
- Girvan-Newman community detection

Run:

```bash
python webapp/app.py
```

Open http://127.0.0.1:5000 in your browser. Input adjacency as JSON (dict or list-of-lists) and choose an algorithm.
