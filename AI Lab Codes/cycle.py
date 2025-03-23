import heapq

def a_star_cycle_detection(graph, start, heuristic):
    """
    Detect cycles in a graph using A* algorithm.
    
    Parameters:
    - graph: Dictionary representation of the graph, {node: [(neighbor, weight), ...]}.
    - start: Starting node.
    - heuristic: Dictionary of heuristic estimates {node: cost_to_target}.
    
    Returns:
    - has_cycle: Boolean indicating whether a cycle was detected.
    - cycle_path: List of nodes representing the detected cycle, if any.
    """
    # Priority queue for A* (stores (f(n), g(n), current_node, path))
    pq = [(heuristic[start], 0, start, [])]
    
    # Visited set to track fully expanded nodes
    visited = set()
    # Set to track nodes currently in the frontier
    frontier = set()

    while pq:
        # Pop the node with the smallest f(n)
        f_n, g_n, current_node, path = heapq.heappop(pq)

        # If the current node is in the frontier, we have found a cycle
        if current_node in frontier:
            cycle_path = path + [current_node]
            return True, cycle_path

        # Mark the node as being processed
        frontier.add(current_node)

        # Expand the current node
        for neighbor, weight in graph.get(current_node, []):
            if neighbor not in visited:
                new_g = g_n + weight
                new_f = new_g + heuristic.get(neighbor, float('inf'))
                heapq.heappush(pq, (new_f, new_g, neighbor, path + [current_node]))

        # Remove the node from the frontier and mark it as visited
        frontier.remove(current_node)
        visited.add(current_node)

    # No cycle detected
    return False, []

# Example Usage
if __name__ == "__main__":
    # Define a weighted graph as an adjacency list
    graph = {
        'A': [('B', 1), ('C', 4)],
        'B': [('C', 2), ('D', 6)],
        'C': [('A', 3)],  # Cycle here: A -> B -> C -> A
        'D': []
    }

    # Define the heuristic for A* (irrelevant for cycle detection but required for A* structure)
    heuristic = {
        'A': 7,
        'B': 6,
        'C': 2,
        'D': 0
    }

    # Start node for cycle detection
    start = 'A'

    # Run A* with cycle detection
    has_cycle, cycle_path = a_star_cycle_detection(graph, start, heuristic)

    # Print the result
    if has_cycle:
        print(f"Cycle detected: {cycle_path}")
    else:
        print("No cycle detected in the graph.")
