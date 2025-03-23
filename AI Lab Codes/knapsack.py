import random

def knapsack_value(items, selected_items):
    total_value = sum(item[0] for item in selected_items)
    total_weight = sum(item[1] for item in selected_items)
    return total_value if total_weight <= weight_limit else 0

def hill_climb_knapsack(items, weight_limit):
    # Initialize with a random subset of items
    current_items = random.sample(items, len(items) // 2)
    current_value = knapsack_value(items, current_items)

    while True:
        neighbors = []
        
        # Generate neighbors by adding/removing an item from the knapsack
        for i in range(len(items)):
            if items[i] not in current_items:
                neighbor = current_items + [items[i]]
                neighbors.append((neighbor, knapsack_value(items, neighbor)))
            else:
                neighbor = current_items.copy()
                neighbor.remove(items[i])
                neighbors.append((neighbor, knapsack_value(items, neighbor)))
        
        # Sort neighbors by their value
        neighbors.sort(key=lambda x: x[1], reverse=True)
        
        # If the best neighbor is better than the current solution, move to it
        best_neighbor, best_value = neighbors[0]
        if best_value > current_value:
            current_items = best_neighbor
            current_value = best_value
        else:
            break  # Stop if no improvement

    return current_items, current_value

# Example items: (value, weight)
items = [(60, 10), (100, 20), (120, 30), (80, 15)]
weight_limit = 50

solution, value = hill_climb_knapsack(items, weight_limit)
print(f"Selected items: {solution} with total value: {value}")
