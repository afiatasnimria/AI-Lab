import heapq

def a_star_word_ladder(start, goal, word_list):
    """
    A* algorithm to solve the word ladder problem.
    
    Parameters:
    - start: Starting word.
    - goal: Goal word.
    - word_list: List of valid words.
    
    Returns:
    - shortest_path: List of words in the transformation sequence.
    """
    def heuristic(word1, word2):
        # Hamming distance heuristic
        return sum(1 for a, b in zip(word1, word2) if a != b)

    word_set = set(word_list)
    pq = [(heuristic(start, goal), 0, start, [])]
    visited = set()

    while pq:
        f_n, g_n, current, path = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)

        # Add current word to path
        path = path + [current]

        # Check if the goal is reached
        if current == goal:
            return path

        # Explore neighbors
        for i in range(len(current)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                neighbor = current[:i] + c + current[i + 1:]
                if neighbor in word_set and neighbor not in visited:
                    new_g = g_n + 1
                    new_f = new_g + heuristic(neighbor, goal)
                    heapq.heappush(pq, (new_f, new_g, neighbor, path))

    return []  # No path found

# Example input
start = "hit"
goal = "cog"
word_list = ["hot", "dot", "dog", "lot", "log", "cog"]
path = a_star_word_ladder(start, goal, word_list)
print(f"Path: {path}")
