import heapq

def a_star(graph, start, goal, heuristic_function):
    # Priority queue to store (f_cost, node)
    pq = []
    heapq.heappush(pq, (0, start))

    # Distance dictionaries
    distances = {node: float('inf') for node in graph}  # Actual cost from start to each node
    distances[start] = 0

    f_costs = {node: float('inf') for node in graph}  # Estimated total cost (g_cost + heuristic)
    f_costs[start] = heuristic_function(start, goal)

    # Path dictionary to reconstruct the shortest path
    came_from = {}

    while pq:
        # Get the node with the lowest f_cost
        _, current_node = heapq.heappop(pq)

        # If goal is reached, reconstruct the path
        if current_node == goal:
            return reconstruct_path(came_from, current_node), distances[goal]

        # Process neighbors
        for neighbor, weight in graph[current_node].items():
            tentative_distance = distances[current_node] + weight

            if tentative_distance < distances[neighbor]:
                # Update distances
                distances[neighbor] = tentative_distance
                f_costs[neighbor] = tentative_distance + heuristic_function(neighbor, goal)

                # Record the best path to the neighbor
                came_from[neighbor] = current_node

                # Add neighbor to the priority queue
                heapq.heappush(pq, (f_costs[neighbor], neighbor))

    # If we exit the loop without finding the goal
    return None, float('inf')

def reconstruct_path(came_from, current_node):
    path = [current_node]
    while current_node in came_from:
        current_node = came_from[current_node]
        path.append(current_node)
    path.reverse()
    return path

# Example heuristic function (straight-line distance)
def heuristic_function(node, goal):
    # Example: Simple heuristic where closer nodes have lower values
    heuristic_map = {
        'A': {'D': 7},
        'B': {'D': 6},
        'C': {'D': 2},
        'D': {'D': 0}
    }
    return heuristic_map.get(node, {}).get(goal, 0)

# Example graph
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 6},
    'C': {'A': 4, 'B': 2, 'D': 3},
    'D': {'B': 6, 'C': 3}
}

start_node = 'A'
goal_node = 'D'

shortest_path, cost = a_star(graph, start_node, goal_node, heuristic_function)
print(f"Shortest path from {start_node} to {goal_node}: {shortest_path}")
print(f"Cost of the path: {cost}")