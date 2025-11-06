if __name__ == "__main__":
    graph = {
        'A': {'B': 6, 'F': 3},
        'B': {'A': 6, 'C': 3, 'D': 2},
        'C': {'B': 3, 'D': 1, 'E': 5},
        'D': {'B': 2, 'C': 1, 'E': 8},
        'E': {'C': 5, 'D': 8, 'I': 5, 'J': 5},
        'J': {'E': 5, 'I': 3},
        'I': {'J': 3, 'E': 5, 'H': 2, 'G': 3},
        'H': {'I': 2, 'F': 7},
        'G': {'I': 3, 'F': 1},
        'F': {'A': 3, 'H': 7, 'G': 1}
    }

    heuristic = {
        'A': 10,
        'B': 8,
        'C': 5,
        'D': 7,
        'E': 3,
        'F': 6,
        'G': 5,
        'H': 3,
        'I': 1,
        'J': 0
    }

    start_node = 'A'
    goal_node = 'J'

    def astar():
        print("Starting A* Search")
        print("----------------------------\n")
        
        # Initialize data structures
        OPEN = {start_node: (0, 0 + heuristic[start_node])}  # node: (g_cost, f_cost)
        CLOSED = {}
        parent = {start_node: None}
        g_cost = {start_node: 0}
        
        while OPEN:
            # Get node with lowest f_cost
            current = min(OPEN, key=lambda x: OPEN[x][1])
            current_g, current_f = OPEN.pop(current)
            
            print(f"Current node: {current} (g={current_g}, h={heuristic[current]}, f={current_f})")
            
            # Goal check
            if current == goal_node:
                CLOSED[current] = (current_g, current_f)
                print(f"\nGoal {goal_node} reached!\n")
                break
            
            # Add to CLOSED
            CLOSED[current] = (current_g, current_f)
            
            # Explore neighbors
            for neighbor, edge_cost in graph[current].items():
                if neighbor in CLOSED:
                    continue
                
                tentative_g = current_g + edge_cost
                tentative_f = tentative_g + heuristic[neighbor]
                
                print(f"  f({neighbor}) = g({neighbor}) + h({neighbor}) = {tentative_g} + {heuristic[neighbor]} = {tentative_f}")
                
                if neighbor not in OPEN or tentative_g < g_cost.get(neighbor, float('inf')):
                    OPEN[neighbor] = (tentative_g, tentative_f)
                    g_cost[neighbor] = tentative_g
                    parent[neighbor] = current
            
            print()
        
        # Reconstruct path
        path = []
        node = goal_node
        while node is not None:
            path.append(node)
            node = parent[node]
        path.reverse()
        
        print("Path:", " -> ".join(path))
        print(f"Total cost = {g_cost[goal_node]}")

    astar()