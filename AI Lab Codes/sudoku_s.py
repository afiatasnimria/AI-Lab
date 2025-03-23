import random
import math

# Check if the current Sudoku board is valid
def is_valid(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                # Check row, column, and subgrid
                if board[i].count(board[i][j]) > 1:
                    return False
                if [board[k][j] for k in range(9)].count(board[i][j]) > 1:
                    return False
                subgrid_x = (i // 3) * 3
                subgrid_y = (j // 3) * 3
                subgrid = [board[x][y] for x in range(subgrid_x, subgrid_x + 3) for y in range(subgrid_y, subgrid_y + 3)]
                if subgrid.count(board[i][j]) > 1:
                    return False
    return True

# Evaluate the number of conflicts (violations of Sudoku rules)
def evaluate(board):
    conflicts = 0
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                # Check row and column conflicts
                if board[i].count(board[i][j]) > 1:
                    conflicts += 1
                if [board[k][j] for k in range(9)].count(board[i][j]) > 1:
                    conflicts += 1
                # Check 3x3 subgrid conflicts
                subgrid_x = (i // 3) * 3
                subgrid_y = (j // 3) * 3
                subgrid = [board[x][y] for x in range(subgrid_x, subgrid_x + 3) for y in range(subgrid_y, subgrid_y + 3)]
                if subgrid.count(board[i][j]) > 1:
                    conflicts += 1
    return conflicts

# Generate a random neighbor by changing a value in an empty cell
def get_neighbors(board):
    neighbors = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1, 10):
                    new_board = [row[:] for row in board]
                    new_board[i][j] = num
                    neighbors.append(new_board)
    return neighbors

# Simulated Annealing Algorithm for Sudoku
def simulated_annealing(board, initial_temperature=1000, cooling_rate=0.003):
    current_board = board
    current_cost = evaluate(current_board)
    temperature = initial_temperature

    while temperature > 1:
        neighbors = get_neighbors(current_board)
        next_board = random.choice(neighbors)
        next_cost = evaluate(next_board)

        # Calculate the difference in cost
        delta_cost = current_cost - next_cost

        # If the next board is better or we accept a worse board based on probability, move to it
        if delta_cost > 0 or random.random() < math.exp(delta_cost / temperature):
            current_board = next_board
            current_cost = next_cost

        # Cool down
        temperature *= 1 - cooling_rate

        # Stop if we find a solution (cost = 0)
        if current_cost == 0:
            break

    return current_board, current_cost

# Example of a Sudoku puzzle (0 denotes an empty cell)
sudoku_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

solution, cost = simulated_annealing(sudoku_board)
print("Solution:", solution)
print("Conflicts:", cost)
