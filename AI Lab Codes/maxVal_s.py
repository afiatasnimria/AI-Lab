import math
import random

def function(x):
    # The function to maximize: f(x) = -x^2 + 4x
    return -x**2 + 4*x

def simulated_annealing(function, start, temperature=1000, cooling_rate=0.995, max_iter=1000):
    current = start
    current_value = function(current)
    
    # Start simulated annealing
    for _ in range(max_iter):
        # Generate a neighbor by randomly perturbing the current solution
        neighbor = current + random.uniform(-1, 1)  # Random perturbation
        neighbor_value = function(neighbor)
        
        # Calculate the change in energy (difference in function values)
        delta_e = neighbor_value - current_value
        
        # If the neighbor is better, accept it
        if delta_e > 0:
            current = neighbor
            current_value = neighbor_value
        else:
            # If the neighbor is worse, accept it with a probability depending on the temperature
            acceptance_probability = math.exp(delta_e / temperature)
            if random.random() < acceptance_probability:
                current = neighbor
                current_value = neighbor_value
        
        # Reduce the temperature according to the cooling schedule
        temperature *= cooling_rate
        
        # If temperature is below a threshold, stop
        if temperature < 1e-3:
            break
    
    return current, current_value

# Example usage
start_point = 0  # Initial point
result_x, result_y = simulated_annealing(function, start_point)

print(f"The maximum value is found at x = {result_x}, f(x) = {result_y}")
