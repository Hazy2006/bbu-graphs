#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_map>
#include <map>
#include <cstdlib>
#include <stdexcept>


using namespace std;

class Graph {
private:
    unordered_map<int, vector<int>>successors;
    unordered_map<int, vector<int>>predecessors;
    map<pair<int, int>, int> costs;

public:
    // Returns the number of vertices in the graph
    int count_vertices() const
    {
        return successors.size();
    }

    // Returns the number of edges in the graph
    int count_edges() const
    {
        return costs.size();
    }

    // Checks if there is an edge from vertex x to vertex y
    // Throws invalid_argument if x or y does not exist
    bool is_edge(int x, int y) const
    {
        if (successors.count(x) == 0)
            throw invalid_argument("Vertex x does not exist!");
        if (successors.count(y) == 0)
            throw invalid_argument("Vertex y does not exist!");
        for (int v : successors.at(x))
            if (v == y)
                return true;
        return false;
    }

    // Constructor: creates a graph with n isolated vertices (0 to n-1)
    Graph(int n)
    {
        for (int i = 0; i < n; i++)
        {
            successors[i] = vector<int>();
            predecessors[i] = vector<int>();
        }
    }

    // Adds an edge from x to y with the given cost
    // Throws invalid_argument if x or y does not exist
    void add_edge(int x, int y, int cost)
    {
        if (successors.count(x) == 0)
            throw invalid_argument("Vertex x does not exist!");
        if (successors.count(y) == 0)
            throw invalid_argument("Vertex y does not exist!");
        if (is_edge(x, y))
            return;
        successors[x].push_back(y);
        predecessors[y].push_back(x);
        costs[{x, y}] = cost;
    }

    // Removes the edge from x to y
    // Throws invalid_argument if x or y does not exist
    void remove_edge(int x, int y)
    {
        if (successors.count(x) == 0)
            throw invalid_argument("Vertex x does not exist!");
        if (successors.count(y) == 0)
            throw invalid_argument("Vertex y does not exist!");
        if (!is_edge(x, y))
            return;
        costs.erase({ x,y });
        for (int i = 0; i < successors[x].size(); i++)
        {
            if (successors[x][i] == y)
            {
                successors[x].erase(successors[x].begin() + i);
                break;
            }
        }
        for (int i = 0; i < predecessors[y].size(); i++)
        {
            if (predecessors[y][i] == x)
            {
                predecessors[y].erase(predecessors[y].begin() + i);
                break;
            }
        }
    }

    // Adds a new isolated vertex and returns its ID
    int add_vertex()
    {
        int new_id = 0;
        for (auto& pair : successors)
            if (pair.first >= new_id)
                new_id = pair.first + 1;
        successors[new_id] = vector<int>();
        predecessors[new_id] = vector<int>();
        return new_id;
    }

    // Removes vertex v and all its incident edges
    // Throws invalid_argument if v does not exist
    void remove_vertex(int v)
    {
        if (successors.count(v) == 0)
            throw invalid_argument("Vertex does not exist!");

        for (int i = 0; i < successors[v].size(); i++)
        {
            int y = successors[v][i];
            costs.erase({ v,y });
            for (int j = 0; j < predecessors[y].size(); j++)
            {
                if (predecessors[y][j] == v)
                {
                    predecessors[y].erase(predecessors[y].begin() + j);
                    break;
                }
            }
        }
            
        for (int i = 0; i < predecessors[v].size(); i++)
        {
            int z = predecessors[v][i];
            costs.erase({ z,v });
            for (int j = 0; j < successors[z].size(); j++)
            {
                if (successors[z][j] == v)
                {
                    successors[z].erase(successors[z].begin() + j);
                    break;
                }
            }
        }
        successors.erase(v);
        predecessors.erase(v);
    }

    // Returns the in-degree of vertex x (number of incoming edges)
    // Throws invalid_argument if x does not exist
    int in_degree(int x)
    {
        if (successors.count(x) == 0)
            throw invalid_argument("Vertex does not exist!");
        return predecessors[x].size();
    }

    // Returns the out-degree of vertex x (number of outgoing edges)
    // Throws invalid_argument if x does not exist
    int out_degree(int x)
    {
        if (successors.count(x) == 0)
            throw invalid_argument("Vertex does not exist!");
        return successors[x].size();
    }

    // Returns the cost of the edge from x to y
    // Throws invalid_argument if x, y, or the edge does not exist
    int get_cost(int x, int y) const
    {
        if (successors.count(x) == 0)
            throw invalid_argument("Vertex x does not exist!");
        if (successors.count(y) == 0)
            throw invalid_argument("Vertex y does not exist!");
        if (costs.count({ x,y }) == 0)
            throw invalid_argument("Edge does not exist!");
        return costs.at({ x,y });
    }

    // Sets the cost of the edge from x to y to sc
    // Throws invalid_argument if x, y, or the edge does not exist
    void set_cost(int x, int y, int sc)
    {
        if (successors.count(x) == 0)
            throw invalid_argument("Vertex x does not exist!");
        if (successors.count(y) == 0)
            throw invalid_argument("Vertex y does not exist!");
        if (costs.count({ x,y }) == 0)
            throw invalid_argument("Edge does not exist!");
        costs[{ x,y }] = sc;
    }

    // Returns a vector of all outbound neighbors of vertex x
    // Throws invalid_argument if x does not exist
    vector<int> parse_outbound(int x) const
    {
        if (successors.count(x) == 0)
            throw invalid_argument("Vertex does not exist!");
        return successors.at(x);
    }

    // Returns a vector of all inbound neighbors of vertex x
    // Throws invalid_argument if x does not exist
    vector<int> parse_inbound(int x) const
    {
        if (successors.count(x) == 0)
            throw invalid_argument("Vertex does not exist!");
        return predecessors.at(x);
    }

    // Returns a vector of all vertex IDs in the graph
    vector<int> parse_vertices() const
    {
        vector<int> vertices;
        for (auto& pair : successors)
            vertices.push_back(pair.first);
        return vertices;
    }

    // Copy constructor: creates a deep copy of the graph
    Graph(const Graph& other)
    {
        successors = other.successors;
        predecessors = other.predecessors;
        costs = other.costs;
    }
    
};

// Reads a graph from a file
// File format: first line contains n (vertices) and m (edges)
// Following m lines contain: x y cost (edge from x to y)
Graph read_from_file(const string& filename)
{
    ifstream f(filename);
    int n, m;
    f >> n >> m;
    Graph g(n);
        
    for (int i = 0; i < m; i++)
    {
        int x, y, cost;
        f >> x >> y >> cost;
        g.add_edge(x, y, cost);
    }
    f.close();

    return g;
}

// Writes the graph to a file in the same format as read_from_file
void write_to_file(const Graph& g, const string& filename)
{
    ofstream o(filename);
    vector<int> vertices = g.parse_vertices();
    o << g.count_vertices() << " " << g.count_edges() << "\n";
    for (int i = 0; i < vertices.size(); i++)
    {
        vector<int> neighbours = g.parse_outbound(vertices[i]);
        for (int j = 0; j < neighbours.size(); j++)
        {
            o << vertices[i] << " " << neighbours[j] << " " << g.get_cost(vertices[i], neighbours[j]) << "\n";
        }
    }
    o.close();
}

// Generates a random directed graph with n vertices and m edges
// Edge costs are random values between 1 and 100
Graph random_graph(int n, int m)
{
    Graph g(n);
    srand(time(0));
    int added = 0;
    while (added < m)
    {
        int x = rand() % n;
        int y = rand() % n;
        if (!g.is_edge(x, y))
        {
            g.add_edge(x, y, rand() % 100 + 1);
            added++;
        }
    }
    return g;
}

// Interactive console application for directed graph operations
// Supports: file I/O, edge/vertex management, graph queries, random generation
int main()
{
    Graph g(0);
    int choice;
    do {
        cout << "1. Read graph from file\n";
        cout << "2. Write graph to file\n";
        cout << "3. Add edge\n";
        cout << "4. Remove edge\n";
        cout << "5. Add vertex\n";
        cout << "6. Remove vertex\n";
        cout << "7. Is edge?\n";
        cout << "8. In/Out degree\n";
        cout << "9. Get cost\n";
        cout << "10. Set cost\n";
        cout << "11. Parse vertices\n";
        cout << "12. Parse outbound\n";
        cout << "13. Parse inbound\n";
        cout << "14. Generate random graph\n";
        cout << "0. Exit\n";
        cout << "Choice: ";
        cin >> choice;
        switch (choice)
    {
        case 1:
        {
            string file_in;
            cout << "Enter filename: ";
            cin >> file_in;
            g = read_from_file(file_in);
            cout << "Graph loaded successfully\n";
            break;
        }
        case 2:
        {
            string file_out;
            cout << "Enter filename: ";
            cin >> file_out;
            write_to_file(g, file_out);
            cout << "Graph written successfully\n";
            break;
        }
        case 3:
        {
            int x, y, cost;
            cout << "Enter source vertex: ";
            cin >> x;
            cout << "Enter target vertex: ";
            cin >> y;
            cout << "Enter cost: ";
            cin >> cost;
            try {
                g.add_edge(x, y, cost);
                cout << "Edge added\n";
            }
            catch (invalid_argument& e) {
                cout << "Error: " << e.what() << "\n";
            }
            break;
        }
    case 4:
    {
        int x, y;
        cout << "Enter source vertex: ";
        cin >> x;
        cout << "Enter target vertex: ";
        cin >> y;
        try {
            g.remove_edge(x, y);
            cout << "Edge deleted\n";
        }
        catch (invalid_argument& e) {
            cout << "Error: " << e.what() << "\n";
        }
        break;
    }
    case 5:
    {
        int new_id = g.add_vertex();
        cout << "Vertex added with ID: " << new_id << "\n";
        break;
    }
    case 6:
    {
		int v;
		cout << "Enter vertex ID to remove: ";
		cin >> v;
        try {
            g.remove_vertex(v);
        }
        catch (invalid_argument& e) {
            cout << "Error: " << e.what() << "\n";
            break;
		}
        cout << "Vertex removed:\n";
        
        break;
    }

    case 7:
    {
        int x, y;
        cout << "Enter source vertex: ";
        cin >> x;
        cout << "Enter target vertex: ";
        cin >> y;
        try {
            bool result = g.is_edge(x, y);
            cout << (result ? "Edge exists\n" : "Edge does not exist\n");
        }
        catch (invalid_argument& e) {
            cout << "Error: " << e.what() << "\n";
        }
        break;
    }
    case 8:
    {
        int v;
        cout << "Enter vertex: ";
        cin >> v;
        try {
            cout << "In-degree: " << g.in_degree(v) << "\n";
            cout << "Out-degree: " << g.out_degree(v) << "\n";
        }
        catch (invalid_argument& e) {
            cout << "Error: " << e.what() << "\n";
        }
        break;
    }
    case 9:
    {
        int x, y;
        cout << "Enter source vertex: ";
        cin >> x;
        cout << "Enter target vertex: ";
        cin >> y;
        try {
            cout << "Cost: " << g.get_cost(x, y) << "\n";
        }
        catch (invalid_argument& e) {
            cout << "Error: " << e.what() << "\n";
        }
        break;
    }
    case 10:
    {
        int x, y, cost;
        cout << "Enter source vertex: ";
        cin >> x;
        cout << "Enter target vertex: ";
        cin >> y;
        cout << "Enter new cost: ";
        cin >> cost;
        try {
            g.set_cost(x, y, cost);
            cout << "Cost updated\n";
        }
        catch (invalid_argument& e) {
            cout << "Error: " << e.what() << "\n";
        }
        break;
    }
    case 11:
    {
        vector<int> vertices = g.parse_vertices();
        cout << "Vertices: ";
        for (int v : vertices)
            cout << v << " ";
        cout << "\n";
        break;
    }
    case 12:
    {
        int v;
        cout << "Enter vertex: ";
        cin >> v;
        try {
            vector<int> out = g.parse_outbound(v);
            cout << "Outbound neighbours: ";
            for (int u : out)
                cout << u << " ";
            cout << "\n";
        }
        catch (invalid_argument& e) {
            cout << "Error: " << e.what() << "\n";
        }
        break;
    }
    case 13:
    {
        int v;
        cout << "Enter vertex: ";
        cin >> v;
        try {
            vector<int> in = g.parse_inbound(v);
            cout << "Inbound neighbours: ";
            for (int u : in)
                cout << u << " ";
            cout << "\n";
        }
        catch (invalid_argument& e) {
            cout << "Error: " << e.what() << "\n";
        }
        break;
    }
    case 14:
    {
        int n, m;
        cout << "Enter number of vertices: ";
        cin >> n;
        cout << "Enter number of edges: ";
        cin >> m;
        g = random_graph(n, m);
        cout << "Random graph generated\n";
        break;
    }
    case 0:
        cout << "Exiting\n";
        break;
    
    }
    } while (choice != 0);

}