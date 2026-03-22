#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<vector<int>> adj = {{2, 3, 6},{3, 4, 6},{0, 3},{0, 1, 2, 4, 5},{1, 3, 5, 7},{3, 4, 7},{0, 1},{4, 5}};
    int n = adj.size();
    vector<pair<int,int>> node_pairs;
    vector<int> degree(n);

    for(int i=0; i<n; i++){
        for(int j=i+1; j<n; j++){
            if(find(adj[i].begin(), adj[i].end(), j) == adj[i].end()){
                node_pairs.push_back({i,j});
            }
        }
    }

    for(int i=0; i<n; i++){
        degree[i] = adj[i].size();
    }

    int res = 0;
    vector<pair<int,int>> ans;
    for(auto& it: node_pairs){
        int pac = degree[it.first] * degree[it.second];
        if(pac > res){
            res = pac;
            ans = {{it.first, it.second}};
        }
        else if(pac == res){
            ans.push_back({it.first, it.second});
        }
        cout << "(" <<it.first << "," << it.second << "): " << pac << endl;
    }

    cout << "Maximum Product of Degrees: " << res << endl;
    cout << "Predicted Link: " << endl;
    for(auto& it: ans){
        cout << it.first << "-" << it.second << endl;
    }
}