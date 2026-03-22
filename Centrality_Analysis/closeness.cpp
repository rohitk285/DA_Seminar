#include <bits/stdc++.h>
using namespace std;

int dijkstra(vector<vector<int>>& adj, int src, int dest) {
    int n = adj.size();
    vector<int> dist(n, INT_MAX);
    dist[src] = 0;
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
    pq.push({0, src});

    while(!pq.empty()){
        int d = pq.top().first;
        int node = pq.top().second;
        pq.pop();

        if(node == dest) return d;

        for(int adjNode: adj[node]){
            if(d + 1 < dist[adjNode]){
                dist[adjNode] = d + 1;
                pq.push({dist[adjNode], adjNode});
            }
        }
    }
    return -1;
}

int main(){
    vector<vector<int>> adj={{2,4},{2},{0,1,3},{2,4},{0,3}};
    int n = adj.size();

    double maxi = 0;
    vector<int> node_ans;

    for(int i=0; i<n; i++){
        int dist = 0;
        for(int j=0; j<n; j++){
            if(i==j) continue;
            int dist_ij = dijkstra(adj, i, j);
            dist += dist_ij;
        }
        double closeness_centrality = (n-1) / (double)dist;
        if(closeness_centrality > maxi) {
            maxi = closeness_centrality;
            node_ans.clear();
            node_ans.push_back(i);
        } else if(closeness_centrality == maxi) {
            node_ans.push_back(i);
        }
        cout << "Closeness Centrality of node " << i << ": " << closeness_centrality << endl;
    }

    cout << "Node(s) with maximum closeness centrality: ";
    for(auto node : node_ans) {
        cout <<"Node "<<node<< endl;
    }
}