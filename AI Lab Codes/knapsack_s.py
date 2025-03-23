import random
import math

def knapsack_value(items, selected_items):
    total_value = sum(item[0] for item in selected_items)
    total_weight = sum(item[1] for item in selected_items)
    return total_value if total_weight <= weight_limit else 0

def simulated_annealing_knapsack(items, weight_limit, temperature=1000, cooling_rate=0.995, max_iter=1000):
    current_items = random.sample(items, len(items) // 2)
    current_value = knapsack_value(items, current_items)

    for _ in range(max_iter):
        # Generate a neighbor by randomly adding/removing an item
        neighbor = current_items.copy()
        if random.random() < 0.5 and len(neighbor) < len(items):
            new_item = random.choice([item for item in items if item not in neighbor])
            neighbor.append(new_item)
        elif len(neighbor) > 0:
            neighbor.remove(random.choice(neighbor))

        new_value = knapsack_value(items, neighbor)
        
        # Calculate the energy difference
        delta_e = new_value - current_value

        if delta_e > 0:
            current_items = neighbor
            current_value = new_value
        else:
            # Accept worse solution with a probability
            acceptance_probability = math.exp(delta_e / temperature)
            if random.random() < acceptance_probability:
                current_items = neighbor
                current_value = new_value
        
        # Cool down
        temperature *= cooling_rate

        if current_value == sum(item[0] for item in items):  # If perfect solution found
            break

    return current_items, current_value

# Example items: (value, weight)
items = [(60, 10), (100, 20), (120, 30), (80, 15)]
weight_limit = 50

solution, value = simulated_annealing_knapsack(items, weight_limit)
print(f"Selected items: {solution} with total value: {value}")
