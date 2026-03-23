#include <bits/stdc++.h>
using namespace std;

vector<vector<int>> bfs(vector<vector<int>>& adj, int start, int end){
    vector<vector<int>> shortest_paths;
    queue<vector<int>> q;
    q.push({start});

    int mini = INT_MAX;

    while(!q.empty()){
        vector<int> path = q.front();
        q.pop();
        int node = path.back();

        if(path.size() > mini) continue;
        
        if(node == end){
            if(path.size() < mini){
                mini = path.size();
                shortest_paths = {path};
            }
            else if(path.size() == mini)
                shortest_paths.push_back(path);
            continue;
        }

        for(int adjNode: adj[node]){
            if(find(path.begin(), path.end(), adjNode) == path.end()){
                vector<int> new_path = path;
                new_path.push_back(adjNode);
                q.push(new_path);
            }
        }
    }
    return shortest_paths;
}

int main(){
    vector<vector<int>> adj = {{2,4},{2},{0,1,3},{2,4},{0,3}};

    int n = adj.size();
    for(int i=0; i<n; i++){
        double betweenness_node_total = 0;
        for(int j=0; j<n; j++){
            for(int k=j+1; k<n; k++){
                if(i==j || i==k) continue;

                vector<vector<int>> paths = bfs(adj, j, k);
                int denominator = paths.size();
                if(denominator == 0) continue;
                int numerator = 0;

                for(auto& path: paths){
                    if(find(path.begin(), path.end(), i) != path.end()) numerator++;
                }

                double betweenness = (double)numerator / (double)denominator;
                betweenness_node_total += betweenness;
            }
        }

        cout << "Betweenness Centrality of node " << i << " is: " << betweenness_node_total << endl;
    }
}