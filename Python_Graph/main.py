from Graph import Graph, read_from_file, write_to_file, random_graph
from connected_components import connected_components
from ford import ford
 
def main():
    g = Graph(0)
    while True:
        print("\n--- Graph Menu ---")
        print("1.  Read graph from file")
        print("2.  Write graph to file")
        print("3.  Add edge")
        print("4.  Remove edge")
        print("5.  Add vertex")
        print("6.  Remove vertex")
        print("7.  Is edge?")
        print("8.  In/Out degree")
        print("9.  Get cost")
        print("10. Set cost")
        print("11. Parse vertices")
        print("12. Parse outbound")
        print("13. Parse inbound")
        print("14. Generate random graph")
        print("15. Find connected components (BFS)")
        print("16. Bellman-Ford algorithm")
        print("0.  Exit")
 
        choice = int(input("Choice: "))
 
        if choice == 0:
            break
        elif choice == 1:
            filename = input("Filename: ")
            g = read_from_file(filename)
        elif choice == 2:
            filename = input("Filename: ")
            write_to_file(g, filename)
        elif choice == 3:
            x, y = map(int, input("Enter x y: ").split())
            cost = int(input("Cost: "))
            try:
                g.add_edge(x, y, cost)
                print("Edge added.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == 4:
            x, y = map(int, input("Enter x y: ").split())
            try:
                g.remove_edge(x, y)
                print("Edge removed.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == 5:
            x = int(input("Enter vertex id: "))
            try:
                g.add_vertex(x)
                print("Vertex added.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == 6:
            x = int(input("Enter vertex: "))
            try:
                g.remove_vertex(x)
                print("Vertex removed.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == 7:
            x, y = map(int, input("Enter x y: ").split())
            try:
                if g.is_edge(x, y):
                    print("Edge exists.")
                else:
                    print("Edge does not exist.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == 8:
            x = int(input("Enter vertex: "))
            try:
                print(f"In degree: {g.in_degree(x)}, Out degree: {g.out_degree(x)}")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == 9:
            x, y = map(int, input("Enter x y: ").split())
            try:
                print(f"Cost: {g.get_cost(x, y)}")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == 10:
            x, y = map(int, input("Enter x y: ").split())
            cost = int(input("Cost: "))
            try:
                g.set_cost(x, y, cost)
                print("Cost updated.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == 11:
            print("Vertices:", sorted(g.parse_vertices()))
        elif choice == 12:
            x = int(input("Enter vertex: "))
            try:
                print("Outbound:", list(g.parse_outbound(x)))
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == 13:
            x = int(input("Enter vertex: "))
            try:
                print("Inbound:", list(g.parse_inbound(x)))
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == 14:
            n = int(input("Number of vertices: "))
            m = int(input("Number of edges: "))
            g = random_graph(n, m)
            print("Random graph generated.")
        elif choice == 15:
            components = connected_components(g)
            print(f"\nNumber of connected components: {len(components)}")
            for i, comp in enumerate(components):
                verts = sorted(comp.parse_vertices())
                print(f"  Component {i + 1}: vertices = {verts}")
        elif choice == 16:
            s = int(input("Enter source vertex: "))
            t = int(input("Enter target vertex: "))
            result, cost = ford(g,s,t)
            if result == "invalid_vertex":
                print("Error: Source or target vertex does not exist in the graph")
            elif result == "negative_cycle":
                print("Negative cost cycle detected")
            elif result == "no_path":
                print("No path exists between s and t")
            else:
                print(f"Path: {result}, Cost: {cost}")
       
if __name__ == "__main__":
    main()