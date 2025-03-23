import random

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

def hill_climb(n):
    board = [random.randint(0, n - 1) for _ in range(n)]  # Initial random solution
    current_conflicts = calculate_conflicts(board)
    
    while current_conflicts > 0:
        neighbors = []
        
        # Generate neighbors by moving queens to a different column in their row
        for row in range(n):
            for col in range(n):
                if col != board[row]:  # Don't move the queen to the same column
                    neighbor = board[:]
                    neighbor[row] = col
                    neighbors.append((neighbor, calculate_conflicts(neighbor)))
        
        # Sort neighbors by the number of conflicts (choose the one with the fewest conflicts)
        neighbors.sort(key=lambda x: x[1])
        best_neighbor, best_conflicts = neighbors[0]
        
        # If no improvement is made, stop
        if best_conflicts >= current_conflicts:
            break
        
        # Move to the best neighbor
        board = best_neighbor
        current_conflicts = best_conflicts
        
    return board, current_conflicts

# Example usage:
n = 8  # 8-Queens problem
solution, conflicts = hill_climb(n)
if conflicts == 0:
    print(f"Solution found: {solution}")
else:
    print(f"Best solution with {conflicts} conflicts: {solution}")
