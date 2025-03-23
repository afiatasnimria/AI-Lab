import random

# Function to check if the coloring is valid (no adjacent vertices share the same color)
def is_valid_coloring(graph, coloring):
    for u in graph:
        for v in graph[u]:
            if coloring[u] == coloring[v]:
                return False
    return True

# Function to evaluate the number of conflicts (edges where two vertices have the same color)
def evaluate(graph, coloring):
    conflicts = 0
    for u in graph:
        for v in graph[u]:
            if coloring[u] == coloring[v]:
                conflicts += 1
    return conflicts

# Function to generate neighbors by changing the color of one vertex
def get_neighbors(graph, coloring):
    neighbors = []
    for vertex in graph:
        for color in range(1, len(graph) + 1):
            new_coloring = coloring.copy()
            new_coloring[vertex] = color
            neighbors.append(new_coloring)
    return neighbors

# Hill Climbing algorithm for Graph Coloring
def hill_climbing(graph):
    # Start with a random coloring
    coloring = {vertex: random.randint(1, len(graph)) for vertex in graph}
    current_cost = evaluate(graph, coloring)
    
    while True:
        neighbors = get_neighbors(graph, coloring)
        best_neighbor = None
        best_cost = float('inf')

        # Evaluate neighbors
        for neighbor in neighbors:
            cost = evaluate(graph, neighbor)
            if cost < best_cost:
                best_cost = cost
                best_neighbor = neighbor
        
        # If no improvement, stop the search
        if best_cost >= current_cost:
            break

        coloring = best_neighbor
        current_cost = best_cost
    
    return coloring, current_cost

# Example graph as an adjacency list
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D'],
    'D': ['B', 'C']
}

# Run Hill Climbing to find a solution
solution, conflicts = hill_climbing(graph)
print("Coloring Solution:", solution)
print("Conflicts:", conflicts)
