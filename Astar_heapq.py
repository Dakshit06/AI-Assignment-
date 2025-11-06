import heapq

def manhattan_distance(a, b):
    """Calculate Manhattan distance between two points"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):
    """
    A* pathfinding algorithm using dictionary-based implementation
    
    Parameters:
        grid: 2D list where 0 is open space and 1 is obstacle
        start: tuple (x, y) of starting position
        goal: tuple (x, y) of goal position
    
    Returns:
        Path as a list of positions or None if no path exists
    """
    rows, cols = len(grid), len(grid[0])
    
    # Possible movement directions
    directions = {
        "up": (0, -1),
        "right": (1, 0),
        "down": (0, 1),
        "left": (-1, 0)
    }
    
    # Initialize data structures
    open_list = []  # Priority queue
    closed_set = set()  # Set of visited nodes
    
    # Track g_score and f_score
    g_score = {start: 0}
    f_score = {start: manhattan_distance(start, goal)}
    
    # For path reconstruction
    parent = {}
    
    # Add start node to open list
    heapq.heappush(open_list, (f_score[start], start))
    
    while open_list:
        # Get node with lowest f_score
        _, current = heapq.heappop(open_list)
        
        # Goal check
        if current == goal:
            # Reconstruct path
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)
            return path[::-1]
        
        # Add to closed set
        closed_set.add(current)
        
        # Check neighbors
        for direction, (dx, dy) in directions.items():
            x, y = current[0] + dx, current[1] + dy
            neighbor = (x, y)
            
            # Skip invalid positions
            if not (0 <= x < cols and 0 <= y < rows):
                continue
                
            # Skip obstacles
            if grid[y][x] == 1:
                continue
                
            # Skip visited nodes
            if neighbor in closed_set:
                continue
            
            # Calculate new path cost
            tentative_g = g_score[current] + 1
            
            # If neighbor not in g_score or we found better path
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                # Record this path
                parent[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + manhattan_distance(neighbor, goal)
                
                # Add to open list if not there already
                if neighbor not in [item[1] for item in open_list]:
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))
    
    # No path found
    return None

def print_grid(grid, start, goal, path=None):
    """Print grid with path visualization"""
    symbols = {
        "start": "S",
        "goal": "G",
        "path": "*",
        "obstacle": "#",
        "empty": "."
    }
    
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            pos = (x, y)
            if pos == start:
                print(symbols["start"], end=" ")
            elif pos == goal:
                print(symbols["goal"], end=" ")
            elif path and pos in path:
                print(symbols["path"], end=" ")
            elif grid[y][x] == 1:
                print(symbols["obstacle"], end=" ")
            else:
                print(symbols["empty"], end=" ")
        print()

# Example usage
if __name__ == "__main__":
    # Grid representation: 0 = open space, 1 = obstacle
    grid = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 1, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    
    # Define start and goal positions
    start_pos = (0, 0)
    goal_pos = (8, 8)
    
    print("A* Search Algorithm")
    print("-----------------")
    
    # Find path using A*
    path = astar(grid, start_pos, goal_pos)
    
    if path:
        print(f"Path found! Length: {len(path)-1} steps")
        print_grid(grid, start_pos, goal_pos, path)
    else:
        print("No path found!")