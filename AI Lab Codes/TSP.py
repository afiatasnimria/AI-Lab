import random

def calculate_tsp_distance(cities, route):
    total_distance = 0
    for i in range(len(route)):
        city1 = route[i]
        city2 = route[(i + 1) % len(route)]  # Wrap around to first city
        total_distance += cities[city1][city2]
    return total_distance

def hill_climb_tsp(cities):
    route = list(range(len(cities)))
    random.shuffle(route)  # Start with a random route
    current_distance = calculate_tsp_distance(cities, route)

    while True:
        neighbors = []
        for i in range(len(route)):
            for j in range(i + 1, len(route)):
                neighbor = route[:]
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]  # Swap two cities
                neighbors.append((neighbor, calculate_tsp_distance(cities, neighbor)))
        
        # Sort neighbors by distance
        neighbors.sort(key=lambda x: x[1])
        best_neighbor, best_distance = neighbors[0]

        if best_distance < current_distance:
            route = best_neighbor
            current_distance = best_distance
        else:
            break  # Stop if no improvement

    return route, current_distance

# Example: Cities as a distance matrix
cities = [
    [0, 10, 15, 20, 25],
    [10, 0, 35, 25, 30],
    [15, 35, 0, 30, 10],
    [20, 25, 30, 0, 15],
    [25, 30, 10, 15, 0]
]

route, distance = hill_climb_tsp(cities)
print(f"Best route: {route} with total distance: {distance}")
