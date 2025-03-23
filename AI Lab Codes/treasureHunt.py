import heapq
import random
import curses
import time
from collections import Counter

# Constants
GRID_SIZE = 15
DIRECTIONS = {'W': (0, -1), 'S': (0, 1), 'A': (-1, 0), 'D': (1, 0)}
K = 3  # Number of nearest neighbors for k-NN

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

def a_star(start, goal, grid):
    open_list = []
    closed_list = set()
    start_node = Node(start)
    goal_node = Node(goal)

    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)
        closed_list.add(current_node.position)

        if current_node.position == goal_node.position:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        for direction in DIRECTIONS.values():
            neighbor_pos = (current_node.position[0] + direction[0], current_node.position[1] + direction[1])

            if (
                0 <= neighbor_pos[0] < GRID_SIZE
                and 0 <= neighbor_pos[1] < GRID_SIZE
                and grid[neighbor_pos[1]][neighbor_pos[0]] != 1
                and neighbor_pos not in closed_list
            ):
                neighbor_node = Node(neighbor_pos, current_node)
                neighbor_node.g = current_node.g + 1
                neighbor_node.h = abs(neighbor_pos[0] - goal_node.position[0]) + abs(neighbor_pos[1] - goal_node.position[1])
                neighbor_node.f = neighbor_node.g + neighbor_node.h

                if any(
                    open_node.position == neighbor_node.position and open_node.f <= neighbor_node.f
                    for open_node in open_list
                ):
                    continue

                heapq.heappush(open_list, neighbor_node)

    return []

def knn_predict(player_pos, treasure_positions, k):
    """
    Predict the next treasure position using k-Nearest Neighbors.
    """
    distances = []
    for treasure_pos in treasure_positions:
        distance = abs(player_pos[0] - treasure_pos[0]) + abs(player_pos[1] - treasure_pos[1])
        distances.append((distance, treasure_pos))

    distances.sort(key=lambda x: x[0])
    nearest_neighbors = [pos for _, pos in distances[:k]]

    # Predict the most likely position based on k-NN
    prediction = Counter(nearest_neighbors).most_common(1)[0][0]
    return prediction

def display_grid(stdscr, grid, player_pos, enemies, treasure_pos):
    stdscr.clear()
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if (x, y) == player_pos:
                stdscr.addstr(y, x * 2, "P")  # Player
            elif (x, y) == treasure_pos:
                stdscr.addstr(y, x * 2, "T")  # Treasure
            elif (x, y) in enemies:
                stdscr.addstr(y, x * 2, "E")  # Enemies
            elif grid[y][x] == 1:
                stdscr.addstr(y, x * 2, "#")  # Wall
            else:
                stdscr.addstr(y, x * 2, ".")  # Empty space
    stdscr.addstr(GRID_SIZE + 1, 0, "\nMove Player with W/A/S/D keys. Press Q to quit.\n")
    stdscr.refresh()

def main(stdscr):
    # Initialize grid, positions, and walls
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    player_pos = (1, 1)
    enemies = [(GRID_SIZE - 2, GRID_SIZE - 2), (GRID_SIZE - 2, 1)]
    treasure_pos = (GRID_SIZE // 2, GRID_SIZE // 2)
    treasure_history = [treasure_pos]  # For k-NN prediction

    # Add some walls
    for i in range(3, 10):
        grid[7][i] = 1

    score = 0

    stdscr.nodelay(True)
    while True:
        display_grid(stdscr, grid, player_pos, enemies, treasure_pos)

        # Check if player reached the treasure
        if player_pos == treasure_pos:
            print("You found the treasure!")
            score += 1
            treasure_pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            treasure_history.append(treasure_pos)
            time.sleep(1)

        # Check if enemies caught the player
        if player_pos in enemies:
            print("Game Over! An enemy caught you!")
            break

        try:
            move = stdscr.getkey().upper()
        except:
            move = None
        move = input("Your move (W/A/S/D): ").upper()
        if move == 'Q':
            print(f"Thanks for playing! Your final score is {score}.")
            break
        if move in DIRECTIONS:
            new_pos = (player_pos[0] + DIRECTIONS[move][0], player_pos[1] + DIRECTIONS[move][1])
            if 0 <= new_pos[0] < GRID_SIZE and 0 <= new_pos[1] < GRID_SIZE and grid[new_pos[1]][new_pos[0]] != 1:
                player_pos = new_pos

        # Move enemies using A* pathfinding or k-NN prediction
        for i, enemy_pos in enumerate(enemies):
            if len(treasure_history) >= K:
                predicted_treasure = knn_predict(player_pos, treasure_history, K)
            else:
                predicted_treasure = treasure_pos

            path = a_star(enemy_pos, predicted_treasure, grid)
            if len(path) > 1:
                enemies[i] = path[1]
    curses.wrapper(main)
    time.sleep(0.2)

if __name__ == "__main__":
    main()
