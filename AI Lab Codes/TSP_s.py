import random
import math

def calculate_tsp_distance(cities, route):
    total_distance = 0
    for i in range(len(route)):
        city1 = route[i]
        city2 = route[(i + 1) % len(route)]
        total_distance += cities[city1][city2]
    return total_distance

def simulated_annealing_tsp(cities, temperature=1000, cooling_rate=0.995, max_iter=1000):
    route = list(range(len(cities)))
    random.shuffle(route)
    current_distance = calculate_tsp_distance(cities, route)

    for _ in range(max_iter):
        # Generate a neighbor by swapping two cities in the route
        neighbor = route[:]
        i, j = random.sample(range(len(cities)), 2)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        
        new_distance = calculate_tsp_distance(cities, neighbor)
        
        # Calculate the energy difference
        delta_e = current_distance - new_distance

        if delta_e > 0:
            route = neighbor
            current_distance = new_distance
        else:
            acceptance_probability = math.exp(delta_e / temperature)
            if random.random() < acceptance_probability:
                route = neighbor
                current_distance = new_distance
        
        # Cool down
        temperature *= cooling_rate

    return route, current_distance

# Example: Cities as a distance matrix
cities = [
    [0, 10, 15, 20, 25],
    [10, 0, 35, 25, 30],
    [15, 35, 0, 30, 10],
    [20, 25, 30, 0, 15],
    [25, 30, 10, 15, 0]
]

route, distance = simulated_annealing_tsp(cities)
print(f"Best route: {route} with total distance: {distance}")
