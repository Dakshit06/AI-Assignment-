from collections import deque
import copy

class PuzzleNode:
    def __init__(self, state, parent=None, move=None, depth=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
    
    def __eq__(self, other):
        return self.state == other.state
    
    def __hash__(self):
        return hash(str(self.state))
    
    def get_blank_position(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return (i, j)
    
    def get_possible_moves(self):
        moves = []
        blank_i, blank_j = self.get_blank_position()
        
        # Check all four possible moves: up, down, left, right
        directions = [
            ('Up', -1, 0),
            ('Down', 1, 0),
            ('Left', 0, -1),
            ('Right', 0, 1)
        ]
        
        for direction, di, dj in directions:
            new_i, new_j = blank_i + di, blank_j + dj
            
            # Check if move is valid
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                moves.append((direction, new_i, new_j))
        
        return moves
    
    def get_new_state(self, move):
        direction, new_i, new_j = move
        blank_i, blank_j = self.get_blank_position()
        
        # Create a deep copy of the current state
        new_state = copy.deepcopy(self.state)
        
        # Swap the blank with the adjacent tile
        new_state[blank_i][blank_j], new_state[new_i][new_j] = \
            new_state[new_i][new_j], new_state[blank_i][blank_j]
        
        return new_state

def print_puzzle(state):
    for row in state:
        print(" ".join(str(tile) if tile != 0 else "_" for tile in row))
    print()

def print_solution(node):
    if not node:
        return
    
    path = []
    current = node
    
    while current:
        path.append((current.state, current.move))
        current = current.parent
    
    print(f"Solution found in {len(path)-1} moves:")
    
    for i, (state, move) in enumerate(reversed(path)):
        print(f"Step {i}: {move if move else 'Initial state'}")
        print_puzzle(state)

def solve_puzzle(initial_state, goal_state):
    initial_node = PuzzleNode(initial_state)
    goal_node = PuzzleNode(goal_state)
    
    # If the initial state is already the goal state
    if initial_node == goal_node:
        return initial_node
    
    # BFS uses a queue
    queue = deque([initial_node])
    # Use a set to keep track of visited states
    visited = set([initial_node])
    
    while queue:
        current_node = queue.popleft()
        
        # Get all possible moves from the current state
        for move_info in current_node.get_possible_moves():
            direction = move_info[0]
            new_state = current_node.get_new_state(move_info)
            
            new_node = PuzzleNode(
                state=new_state,
                parent=current_node,
                move=direction,
                depth=current_node.depth + 1
            )
            
            # Check if this state has been visited
            if new_node not in visited:
                visited.add(new_node)
                
                # Check if we've reached the goal state
                if new_node == goal_node:
                    return new_node
                
                # Add the new node to the queue for further exploration
                queue.append(new_node)
    
    # If no solution is found
    return None

def main():
    # Example initial state (0 represents the blank space)
    initial_state = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]
    ]
    
    # Goal state
    goal_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    
    print("Initial State:")
    print_puzzle(initial_state)
    
    print("Goal State:")
    print_puzzle(goal_state)
    
    print("Solving...")
    solution = solve_puzzle(initial_state, goal_state)
    
    if solution:
        print_solution(solution)
    else:
        print("No solution found!")

if __name__ == "__main__":
    main()