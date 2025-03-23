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

def generate_neighbors(route):
    neighbors = []
    for i in range(1, len(route) - 2):
        for j in range(i + 1, len(route) - 1):
            neighbor = route[:]
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors


def hill_climbing(locations):
    current_route = generate_initial_route(len(locations))
    current_distance = total_distance(current_route, locations)

    while True:
        neighbors = generate_neighbors(current_route)
        best_neighbor = min(neighbors, key=lambda route: total_distance(route, locations))
        best_neighbor_distance = total_distance(best_neighbor, locations)

        if best_neighbor_distance < current_distance:
            current_route, current_distance = best_neighbor, best_neighbor_distance
        else:
            break

    return current_route, current_distance

n = int(input())
locations = [tuple(map(float, input().split())) for _ in range(n)]
route, distance = hill_climbing(locations)

print("Hill Climbing")
print(f"Route: {'->'.join(map(str, [i + 1 for i in route]))}")
print(f"Total Distance: {distance:.2f}")
