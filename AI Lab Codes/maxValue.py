def function(x):
    # The function we want to maximize: f(x) = -x^2 + 4x
    return -x**2 + 4*x

def hill_climb(function, start, epsilon=0.01, max_iter=1000):
    current = start
    
    # Start hill climbing
    for _ in range(max_iter):
        left = current - epsilon
        right = current + epsilon
        
        # Evaluate the neighbors
        left_value = function(left)
        right_value = function(right)
        current_value = function(current)
        
        # Choose the neighbor with the highest value
        if left_value > current_value:
            current = left
        elif right_value > current_value:
            current = right
        else:
            # If neither neighbor is better, stop (local maximum reached)
            break
            
    return current, function(current)

# Example usage
start_point = 0  # You can start at any point within the range, e.g., x = 0
result_x, result_y = hill_climb(function, start_point)

print(f"The maximum value is found at x = {result_x}, f(x) = {result_y}")
