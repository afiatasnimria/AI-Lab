import random
import math

def calculate_conflicts(board):
    conflicts = 0
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j]:  # Same column
                conflicts += 1
            if abs(board[i] - board[j]) == abs(i - j):  # Diagonal conflict
                conflicts += 1
    return conflicts

def simulated_annealing(n, temperature=1000, cooling_rate=0.995, max_iter=1000):
    board = [random.randint(0, n - 1) for _ in range(n)]  # Initial random solution
    current_conflicts = calculate_conflicts(board)
    
    for _ in range(max_iter):
        # Generate a neighbor by randomly moving one queen to a different column
        row = random.randint(0, n - 1)
        new_col = random.randint(0, n - 1)
        new_board = board[:]
        new_board[row] = new_col
        
        new_conflicts = calculate_conflicts(new_board)
        
        # Calculate the energy difference
        delta_e = current_conflicts - new_conflicts
        
        # Accept the new board if it improves or based on the probability for worse solutions
        if delta_e > 0:
            board = new_board
            current_conflicts = new_conflicts
        else:
            acceptance_probability = math.exp(delta_e / temperature)
            if random.random() < acceptance_probability:
                board = new_board
                current_conflicts = new_conflicts
        
        # Reduce temperature
        temperature *= cooling_rate
        
        # If the solution has no conflicts, stop
        if current_conflicts == 0:
            break
    
    return board, current_conflicts

# Example usage:
n = 8  # 8-Queens problem
solution, conflicts = simulated_annealing(n)
if conflicts == 0:
    print(f"Solution found: {solution}")
else:
    print(f"Best solution with {conflicts} conflicts: {solution}")
