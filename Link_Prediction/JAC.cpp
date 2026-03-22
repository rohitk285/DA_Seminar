#include <bits/stdc++.h>
using namespace std;

int findIntersection(vector<vector<int>>& adj, int u, int v){
    int count = 0;
    for(auto& it: adj[u]){
        if(find(adj[v].begin(), adj[v].end(), it) != adj[v].end()){
            count++;
        }
    }
    return count;
}

int findUnion(vector<vector<int>>& adj, int u, int v){
    unordered_set<int> unique_nodes;
    for(auto& it: adj[u]){
        unique_nodes.insert(it);
    }
    for(auto& it: adj[v]){
        unique_nodes.insert(it);
    }
    return unique_nodes.size();
}

int main(){
    vector<vector<int>> adj = {{2, 3, 6},{3, 4, 6},{0, 3},{0, 1, 2, 4, 5},{1, 3, 5, 7},{3, 4, 7},{0, 1},{4, 5}};
    int n = adj.size();
    vector<pair<int,int>> node_pairs;

    for(int i=0; i<n; i++){
        for(int j=i+1; j<n; j++){
            if(find(adj[i].begin(), adj[i].end(), j) == adj[i].end()){
                node_pairs.push_back({i,j});
            }
        }
    }

    double res = 0.0;
    vector<pair<int,int>> ans;
    for(auto& it: node_pairs){
        int intersection_count = findIntersection(adj, it.first, it.second);
        int union_count = findUnion(adj, it.first, it.second);
        double jac = (double)intersection_count / union_count;
        if(jac > res){
            res = jac;
            ans = {{it.first, it.second}};
        }
        else if(jac == res){
            ans.push_back({it.first, it.second});
        }
        cout << "(" <<it.first << "," << it.second << "): " << jac << endl;
    }

    cout<< "Maximum Jaccard Similarity: " << res << endl;
    cout<< "Predicted Link: " << endl;
    for(auto& it: ans){
        cout << it.first << "-" << it.second << endl;
    }
}