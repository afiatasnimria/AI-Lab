import random
import math

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

# Simulated Annealing algorithm for Graph Coloring
def simulated_annealing(graph, initial_temperature=1000, cooling_rate=0.003):
    coloring = {vertex: random.randint(1, len(graph)) for vertex in graph}
    current_cost = evaluate(graph, coloring)
    temperature = initial_temperature

    while temperature > 1:
        neighbors = get_neighbors(graph, coloring)
        next_coloring = random.choice(neighbors)
        next_cost = evaluate(graph, next_coloring)

        # Calculate the cost difference
        delta_cost = current_cost - next_cost

        # If the next coloring is better or if a worse one is accepted based on probability
        if delta_cost > 0 or random.random() < math.exp(delta_cost / temperature):
            coloring = next_coloring
            current_cost = next_cost

        # Cool down the temperature
        temperature *= 1 - cooling_rate

        # Stop if the cost is 0 (perfect solution)
        if current_cost == 0:
            break
    
    return coloring, current_cost

# Example graph as an adjacency list
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D'],
    'D': ['B', 'C']
}

# Run Simulated Annealing to find a solution
solution, conflicts = simulated_annealing(graph)
print("Coloring Solution:", solution)
print("Conflicts:", conflicts)
