from heapq import heappop, heappush

def astar(graph, start, goal, heuristic):
    """
    Perform A* search on a graph.
    
    Args:
    - graph: A dictionary representing the adjacency list. 
      Format: {node: [(neighbor, cost), ...]}
    - start: Start node.
    - goal: Goal node.
    - heuristic: A function that estimates the cost to reach the goal from a node.
    
    Returns:
    - List representing the path from start to goal, or an empty list if no path exists.
    """
    open_set = []
    heappush(open_set, (0, start))
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic(start, goal)

    while open_set:
        current = heappop(open_set)[1]

        if current == goal:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]  # Return reversed path

        for neighbor, cost in graph[current]:
            tentative_g_score = g_score[current] + cost
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                heappush(open_set, (f_score[neighbor], neighbor))

    return []  # No path found
# Define the graph as an adjacency list
graph = {
    'A': [('B', 1), ('C', 3)],
    'B': [('A', 1), ('D', 1), ('E', 4)],
    'C': [('A', 3), ('F', 2)],
    'D': [('B', 1)],
    'E': [('B', 4), ('F', 1)],
    'F': [('C', 2), ('E', 1)]
}

# Define a simple heuristic (e.g., straight-line distance)
def heuristic(node, goal):
    distances = {
        'A': 6, 'B': 4, 'C': 4,
        'D': 3, 'E': 2, 'F': 0  # Assume F is the goal
    }
    return distances[node]

# Run A*
start = 'A'
goal = 'F'
path = astar(graph, start, goal, heuristic)
print("Path found:", path)
