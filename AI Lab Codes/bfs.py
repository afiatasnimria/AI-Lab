import heapq

def dijkstra_bfs(graph, start, target):
    """
    Perform a BFS using a priority queue (Dijkstra's Algorithm) to find
    the shortest path from start to target in a weighted graph.
    
    Parameters:
    - graph: Dictionary representation of the graph, {node: [(neighbor, weight), ...]}.
    - start: Starting node.
    - target: Target node.

    Returns:
    - shortest_path_cost: Cost of the shortest path from start to target.
    - path: List of nodes representing the shortest path.
    """
    # Priority queue to store (cost, node, path)
    pq = [(0, start, [])]
    # Dictionary to store the shortest known distance to each node
    visited = {}

    while pq:
        # Get the node with the smallest path cost
        current_cost, current_node, current_path = heapq.heappop(pq)

        # If this node has already been visited with a smaller cost, skip it
        if current_node in visited and visited[current_node] <= current_cost:
            continue

        # Mark the node as visited
        visited[current_node] = current_cost

        # Append the current node to the path
        current_path = current_path + [current_node]

        # If we've reached the target node, return the cost and path
        if current_node == target:
            return current_cost, current_path

        # Explore neighbors
        for neighbor, weight in graph.get(current_node, []):
            if neighbor not in visited or current_cost + weight < visited[neighbor]:
                heapq.heappush(pq, (current_cost + weight, neighbor, current_path))

    # If the target is unreachable, return infinity and an empty path
    return float('inf'), []

# Example Usage
if __name__ == "__main__":
    # Define a weighted graph as an adjacency list
    graph = {
        'A': [('B', 1), ('C', 4)],
        'B': [('C', 2), ('D', 6)],
        'C': [('D', 3)],
        'D': []
    }

    # Define the start and target nodes
    start = 'A'
    target = 'D'

    # Find the shortest path using Dijkstra (BFS with a priority queue)
    shortest_path_cost, path = dijkstra_bfs(graph, start, target)

    # Print the result
    if shortest_path_cost == float('inf'):
        print(f"No path exists from {start} to {target}.")
    else:
        print(f"The shortest path from {start} to {target} is {path} with a cost of {shortest_path_cost}.")
