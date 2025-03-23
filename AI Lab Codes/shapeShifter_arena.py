import heapq
import random
import os
import time

# Constants
GRID_SIZE = 15
DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
ENERGY_ORBS = 10

# Colors/Types
PLAYER_TYPES = ["Predator", "Prey", "Neutral"]
ENEMY_TYPES = ["Predator", "Prey"]

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

        for direction in DIRECTIONS:
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

def display_grid(grid, player_pos, enemies, orbs, player_type):
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
    print(f"Player Type: {player_type} | Orbs Collected: {orbs['collected']}/{ENERGY_ORBS}")
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if (x, y) == player_pos:
                print("P", end=" ")  # Player
            elif (x, y) in enemies:
                print("E", end=" ")  # Enemies
            elif (x, y) in orbs['positions']:
                print("O", end=" ")  # Energy Orbs
            elif grid[y][x] == 1:
                print("#", end=" ")  # Wall
            else:
                print(".", end=" ")  # Empty space
        print()
    print("\nControls: W/A/S/D to move, 1/2/3 to shape-shift (1=Predator, 2=Prey, 3=Neutral), Q to quit.\n")

def main():
    # Initialize grid, positions, and walls
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    player_pos = (1, 1)
    player_type = "Prey"  # Default type
    enemies = [(GRID_SIZE - 2, GRID_SIZE - 2), (GRID_SIZE - 2, 1)]
    orbs = {"positions": [], "collected": 0}

    # Place walls and orbs
    for i in range(3, 10):
        grid[7][i] = 1
    for _ in range(ENERGY_ORBS):
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        while grid[y][x] == 1 or (x, y) == player_pos:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        orbs["positions"].append((x, y))

    score = 0
    running = True

    while running:
        display_grid(grid, player_pos, enemies, orbs, player_type)

        # Check for collisions
        if player_pos in enemies:
            if player_type == "Predator":
                enemies.remove(player_pos)  # Predator eats enemies
                print("Enemy defeated!")
            else:
                print("Game Over! An enemy caught you!")
                break

        # Check for orb collection
        if player_pos in orbs["positions"] and player_type == "Prey":
            orbs["positions"].remove(player_pos)
            orbs["collected"] += 1
            if orbs["collected"] == ENERGY_ORBS:
                print("Congratulations! You collected all the orbs!")
                break

        # Get user input
        move = input("Your move: ").upper()
        if move == 'Q':
            print(f"Thanks for playing! Final Score: {orbs['collected']}")
            break
        elif move in "WASD":
            dx, dy = DIRECTIONS["WASD".index(move)]
            new_pos = (player_pos[0] + dx, player_pos[1] + dy)
            if 0 <= new_pos[0] < GRID_SIZE and 0 <= new_pos[1] < GRID_SIZE and grid[new_pos[1]][new_pos[0]] != 1:
                player_pos = new_pos
        elif move in "123":
            player_type = PLAYER_TYPES[int(move) - 1]

        # Enemy logic: chase or avoid player
        for i, enemy_pos in enumerate(enemies):
            if player_type == "Predator":
                path = a_star(enemy_pos, (0, 0), grid)  # Enemy avoids player by moving to (0, 0)
                if len(path) > 1:
                    enemies[i] = path[1]
            else:
                path = a_star(enemy_pos, player_pos, grid)  # Enemy chases player
                if len(path) > 1:
                    enemies[i] = path[1]

        time.sleep(0.2)

if __name__ == "__main__":
    main()
