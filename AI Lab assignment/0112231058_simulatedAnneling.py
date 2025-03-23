import random
import math

def calculate_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


def total_distance(route, locations):
    return sum(calculate_distance(locations[route[i]], locations[route[i + 1]]) for i in range(len(route) - 1))


def generate_initial_route(n):
    route = list(range(1, n))  
    random.shuffle(route)
    return [0] + route + [0] 


def generate_neighbor(route):
    i, j = random.sample(range(1, len(route) - 1), 2)
    neighbor = route[:]
    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
    return neighbor


def simulated_annealing(locations, initial_temperature=1000, cooling_rate=0.995, max_iterations=10000):
    current_route = generate_initial_route(len(locations))
    current_distance = total_distance(current_route, locations)
    best_route, best_distance = current_route[:], current_distance

    temperature = initial_temperature

    for _ in range(max_iterations):
        if temperature < 1e-3:
            break

        neighbor = generate_neighbor(current_route)
        neighbor_distance = total_distance(neighbor, locations)

        if neighbor_distance < current_distance or random.random() < math.exp((current_distance - neighbor_distance) / temperature):
            current_route, current_distance = neighbor, neighbor_distance

        if current_distance < best_distance:
            best_route, best_distance = current_route[:], current_distance

        temperature *= cooling_rate

    return best_route, best_distance

n = int(input())
locations = [tuple(map(float, input().split())) for _ in range(n)]
route, distance = simulated_annealing(locations)

print("Simulated Annealing")
print(f"Route: {'->'.join(map(str, [i + 1 for i in route]))}")
print(f"Total Distance: {distance:.2f}")
