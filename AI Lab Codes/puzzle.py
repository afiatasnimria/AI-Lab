import heapq

def a_star_8_puzzle(start, goal):
    """
    A* algorithm to solve the 8-puzzle problem.
    
    Parameters:
    - start: Initial state as a tuple (e.g., (1, 2, 3, 4, 5, 6, 7, 8, 0)).
    - goal: Goal state as a tuple (e.g., (1, 2, 3, 4, 5, 6, 7, 8, 0)).
    
    Returns:
    - shortest_path: List of moves to solve the puzzle.
    """
    def heuristic(state):
        # Manhattan distance heuristic for 8-puzzle
        distance = 0
        for i in range(9):
            if state[i] != 0:  # Skip the blank tile
                goal_pos = goal.index(state[i])
                distance += abs(i // 3 - goal_pos // 3) + abs(i % 3 - goal_pos % 3)
        return distance

    def neighbors(state):
        # Find neighbors by moving the blank (0)
        state = list(state)
        zero_pos = state.index(0)
        row, col = zero_pos // 3, zero_pos % 3
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        result = []
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_zero_pos = new_row * 3 + new_col
                new_state = state[:]
                new_state[zero_pos], new_state[new_zero_pos] = new_state[new_zero_pos], new_state[zero_pos]
                result.append(tuple(new_state))
        return result

    pq = [(heuristic(start), 0, start, [])]  # (f(n), g(n), state, path)
    visited = set()
    
    while pq:
        f_n, g_n, current, path = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)
        
        # Add current state to path
        path = path + [current]
        
        # Check if the goal is reached
        if current == goal:
            return path
        
        # Explore neighbors
        for neighbor in neighbors(current):
            if neighbor not in visited:
                new_g = g_n + 1
                new_f = new_g + heuristic(neighbor)
                heapq.heappush(pq, (new_f, new_g, neighbor, path))
    
    return []  # No solution found

# Example start and goal states
start = (1, 2, 3, 4, 5, 6, 0, 7, 8)
goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
solution = a_star_8_puzzle(start, goal)
print(f"Solution: {solution}")
