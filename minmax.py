import math

class TicTacToe:
    def __init__(self):
        # Initialize 3x3 board with empty spaces
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.human = 'X'
        self.ai = 'O'
    
    def print_board(self):
        """Print the current board state"""
        print("\n   0   1   2")
        for i in range(3):
            print(f"{i}  {self.board[i][0]} | {self.board[i][1]} | {self.board[i][2]}")
            if i < 2:
                print("  ---|---|---")
    
    def is_winner(self, player):
        """Check if the given player has won"""
        # Check rows
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        
        # Check columns
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        
        # Check diagonals
        if all(self.board[i][i] == player for i in range(3)):
            return True
        if all(self.board[i][2-i] == player for i in range(3)):
            return True
        
        return False
    
    def is_board_full(self):
        """Check if the board is full"""
        for row in self.board:
            if ' ' in row:
                return False
        return True
    
    def is_game_over(self):
        """Check if the game is over"""
        return self.is_winner(self.human) or self.is_winner(self.ai) or self.is_board_full()
    
    def get_available_moves(self):
        """Get list of available moves (empty positions)"""
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    moves.append((i, j))
        return moves
    
    def make_move(self, row, col, player):
        """Make a move on the board"""
        if self.board[row][col] == ' ':
            self.board[row][col] = player
            return True
        return False
    
    def undo_move(self, row, col):
        """Undo a move (set position back to empty)"""
        self.board[row][col] = ' '
    
    def evaluate(self):
        """Evaluate the current board state"""
        if self.is_winner(self.ai):
            return 10  # AI wins
        elif self.is_winner(self.human):
            return -10  # Human wins
        else:
            return 0  # Draw or game not finished
    
    def minimax(self, depth, is_maximizing, alpha=-math.inf, beta=math.inf):
        """
        Minimax algorithm with alpha-beta pruning
        
        Args:
            depth: Current depth in the search tree
            is_maximizing: True if it's AI's turn (maximizing), False if human's turn (minimizing)
            alpha: Alpha value for alpha-beta pruning
            beta: Beta value for alpha-beta pruning
        
        Returns:
            Best score for the current position
        """
        # Base case: if game is over, return the evaluation
        if self.is_game_over():
            return self.evaluate()
        
        if is_maximizing:
            # AI's turn - maximize the score
            max_eval = -math.inf
            for row, col in self.get_available_moves():
                # Make the move
                self.board[row][col] = self.ai
                
                # Recursively call minimax for the opponent's turn
                eval_score = self.minimax(depth + 1, False, alpha, beta)
                
                # Undo the move
                self.board[row][col] = ' '
                
                # Update the maximum evaluation
                max_eval = max(max_eval, eval_score)
                
                # Alpha-beta pruning
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
                    
            return max_eval
        else:
            # Human's turn - minimize the score
            min_eval = math.inf
            for row, col in self.get_available_moves():
                # Make the move
                self.board[row][col] = self.human
                
                # Recursively call minimax for the AI's turn
                eval_score = self.minimax(depth + 1, True, alpha, beta)
                
                # Undo the move
                self.board[row][col] = ' '
                
                # Update the minimum evaluation
                min_eval = min(min_eval, eval_score)
                
                # Alpha-beta pruning
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
                    
            return min_eval
    
    def find_best_move(self):
        """
        Find the best move for the AI using minimax algorithm
        
        Returns:
            Tuple (row, col) representing the best move
        """
        best_move = None
        best_value = -math.inf
        
        print("AI is thinking...")
        
        for row, col in self.get_available_moves():
            # Make the move
            self.board[row][col] = self.ai
            
            # Calculate the minimax value for this move
            move_value = self.minimax(0, False)
            
            # Undo the move
            self.board[row][col] = ' '
            
            # Update best move if this move is better
            if move_value > best_value:
                best_value = move_value
                best_move = (row, col)
                
            print(f"Move ({row}, {col}): Score = {move_value}")
        
        print(f"Best move: {best_move} with score: {best_value}")
        return best_move
    
    def play_game(self):
        """Main game loop"""
        print("Welcome to Tic-Tac-Toe!")
        print("You are X, AI is O")
        print("Enter row and column (0-2) separated by space")
        
        while not self.is_game_over():
            self.print_board()
            
            # Human move
            try:
                row, col = map(int, input("\nEnter your move (row col): ").split())
                if 0 <= row <= 2 and 0 <= col <= 2:
                    if self.make_move(row, col, self.human):
                        if self.is_game_over():
                            break
                        
                        # AI move
                        ai_row, ai_col = self.find_best_move()
                        self.make_move(ai_row, ai_col, self.ai)
                        print(f"AI moves to ({ai_row}, {ai_col})")
                    else:
                        print("Position already occupied! Try again.")
                else:
                    print("Invalid position! Enter values between 0-2.")
            except ValueError:
                print("Invalid input! Enter two numbers separated by space.")
        
        # Game over - show final board and result
        self.print_board()
        if self.is_winner(self.human):
            print("\nCongratulations! You won!")
        elif self.is_winner(self.ai):
            print("\nAI wins! Better luck next time!")
        else:
            print("\nIt's a draw!")

def demonstrate_minimax():
    """Demonstrate the minimax algorithm with a specific board state"""
    print("="*50)
    print("MINIMAX ALGORITHM DEMONSTRATION")
    print("="*50)
    
    game = TicTacToe()
    
    # Set up a specific board state for demonstration
    game.board = [
        ['X', 'O', ' '],
        [' ', 'X', ' '],
        ['O', ' ', ' ']
    ]
    
    print("Current board state:")
    game.print_board()
    
    print("\nFinding best move for AI (O)...")
    best_move = game.find_best_move()
    
    print(f"\nThe AI should play at position: {best_move}")
    
    # Make the best move and show the result
    if best_move:
        game.make_move(best_move[0], best_move[1], game.ai)
        print("\nBoard after AI's best move:")
        game.print_board()

def main():
    """Main function"""
    print("1. Play against AI")
    print("2. Demonstrate Minimax Algorithm")
    
    choice = input("\nChoose an option (1 or 2): ")
    
    if choice == '1':
        game = TicTacToe()
        game.play_game()
    elif choice == '2':
        demonstrate_minimax()
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()