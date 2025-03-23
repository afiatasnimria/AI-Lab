import heapq

def bfs_a_star(graph, start, target, heuristic):
    """
    Perform BFS with A* by using a priority queue and a heuristic.
    
    Parameters:
    - graph: Dictionary representation of the graph, {node: [(neighbor, weight), ...]}.
    - start: Starting node.
    - target: Target node.
    - heuristic: Dictionary of heuristic estimates {node: cost_to_target}.
    
    Returns:
    - shortest_path_cost: Cost of the shortest path.
    - path: List of nodes representing the shortest path.
    """
    # Priority queue to store (f(n), g(n), node, path)
    pq = [(heuristic[start], 0, start, [])]

    # Set to track visited nodes
    visited = set()

    while pq:
        # Pop the node with the smallest f(n)
        f_n, g_n, current_node, path = heapq.heappop(pq)

        # If the current node is the target, return the cost and path
        if current_node == target:
            return g_n, path + [current_node]

        # Skip if we've already visited this node
        if current_node in visited:
            continue
        visited.add(current_node)

        # Explore neighbors
        for neighbor, weight in graph.get(current_node, []):
            if neighbor not in visited:
                new_g = g_n + weight
                new_f = new_g + heuristic.get(neighbor, float('inf'))
                heapq.heappush(pq, (new_f, new_g, neighbor, path + [current_node]))

    # If the target is unreachable, return infinity and an empty path
    return float('inf'), []


def dfs_a_star(graph, start, target, heuristic, path_cost=0, path=None, best_path=None, best_cost=float('inf')):
    """
    Perform DFS with A* by exploring paths based on heuristics.
    
    Parameters:
    - graph: Dictionary representation of the graph, {node: [(neighbor, weight), ...]}.
    - start: Starting node.
    - target: Target node.
    - heuristic: Dictionary of heuristic estimates {node: cost_to_target}.
    - path_cost: Current cost of the path (default: 0).
    - path: Current path being explored (default: None).
    - best_path: Current best path found (default: None).
    - best_cost: Current best cost found (default: infinity).
    
    Returns:
    - best_cost: Cost of the best path.
    - best_path: List of nodes representing the best path.
    """
    if path is None:
        path = []

    # Add the current node to the path
    path = path + [start]

    # If the target node is reached, update the best path and cost
    if start == target:
        if path_cost < best_cost:
            return path_cost, path
        return best_cost, best_path

    # Explore neighbors
    for neighbor, weight in graph.get(start, []):
        # Avoid revisiting nodes in the current path
        if neighbor not in path:
            new_cost = path_cost + weight
            # Compute f(n) = g(n) + h(n)
            f_n = new_cost + heuristic.get(neighbor, float('inf'))
            if f_n < best_cost:
                # Recur with the neighbor
                best_cost, best_path = dfs_a_star(graph, neighbor, target, heuristic, new_cost, path, best_path, best_cost)

    return best_cost, best_path


# Example Usage
if __name__ == "__main__":
    # Define a weighted graph as an adjacency list
    graph = {
        'A': [('B', 1), ('C', 4)],
        'B': [('C', 2), ('D', 6)],
        'C': [('D', 3)],
        'D': []
    }

    # Define the heuristic for A* (e.g., straight-line distance to target)
    heuristic = {
        'A': 7,
        'B': 6,
        'C': 2,
        'D': 0
    }

    # Start and target nodes
    start = 'A'
    target = 'D'

    # BFS with A*
    bfs_cost, bfs_path = bfs_a_star(graph, start, target, heuristic)
    if bfs_cost == float('inf'):
        print(f"BFS A*: No path exists from {start} to {target}.")
    else:
        print(f"BFS A*: Shortest path from {start} to {target} is {bfs_path} with cost {bfs_cost}.")

    # DFS with A*
    dfs_cost, dfs_path = dfs_a_star(graph, start, target, heuristic)
    if dfs_cost == float('inf'):
        print(f"DFS A*: No path exists from {start} to {target}.")
    else:
        print(f"DFS A*: Shortest path from {start} to {target} is {dfs_path} with cost {dfs_cost}.")
