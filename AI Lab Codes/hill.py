import random

def hill_climbing_maze(maze, start, goal, max_iterations):

    def heuristic(pos):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def get_neighbors(pos):
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        neighbors = []
        for move in moves:
            new_x, new_y = pos[0] + move[0], pos[1] + move[1]
            if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] == 0:
                neighbors.append((new_x, new_y))
        return neighbors

    current_pos = start
    path = [current_pos]

    for _ in range(max_iterations):
        if current_pos == goal:
            return path, True

        neighbors = get_neighbors(current_pos)
        if not neighbors:
            break

        next_pos = min(neighbors, key=heuristic)
        if heuristic(next_pos) >= heuristic(current_pos):
            break

        current_pos = next_pos
        path.append(current_pos)

    return path, False


maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
]
start = (0, 0)
goal = (4, 4)
max_iterations = 100

path, success = hill_climbing_maze(maze, start, goal, max_iterations)

if success:
    print("Path to goal found!")
else:
    print("Failed to reach the goal.")
print("Path:", path)
