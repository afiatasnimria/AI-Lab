import heapq

def a_star(maze, start, goal):
    """
    A* search algorithm for shortest path in a maze.
    """
    if not maze or not maze[0]:
        raise ValueError("Maze cannot be empty")
    rows, cols = len(maze), len(maze[0])
    pq = []  # Priority queue
    heapq.heappush(pq, (0, start))
    distances = {start: 0}
    f_costs = {start: heuristic(start, goal)}
    came_from = {}

    while pq:
        _, current_node = heapq.heappop(pq)

        if current_node == goal:  # Path found
            return reconstruct_path(came_from, current_node), distances[goal]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Move directions
            neighbor = (current_node[0] + dx, current_node[1] + dy)

            # Check if the neighbor is valid
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] == 0:
                tentative_distance = distances[current_node] + 1

                if neighbor not in distances or tentative_distance < distances[neighbor]:
                    distances[neighbor] = tentative_distance
                    f_costs[neighbor] = tentative_distance + heuristic(neighbor, goal)
                    came_from[neighbor] = current_node
                    heapq.heappush(pq, (f_costs[neighbor], neighbor))

    return None, float('inf')  # No path found

def reconstruct_path(came_from, current_node):
    """
    Reconstructs the path from the goal to the start.
    """
    path = [current_node]
    while current_node in came_from:
        current_node = came_from[current_node]
        path.append(current_node)
    path.reverse()
    return path

def heuristic(node, goal):
    """
    Manhattan distance heuristic function.
    """
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

# Example usage
maze = [
    [0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 1],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0]
]
start = (0, 0)
goal = (4, 4)

path, cost = a_star(maze, start, goal)
print(f"A* path from {start} to {goal}: {path}")
print(f"Cost of A* path: {cost}")