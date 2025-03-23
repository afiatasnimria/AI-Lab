import heapq
import os
import time

# Constants
GRID_SIZE = 10
DIRECTIONS = {'W': (0, -1), 'S': (0, 1), 'A': (-1, 0), 'D': (1, 0)}

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

def display_grid(grid, pacman_pos, ghost_pos):
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if (x, y) == pacman_pos:
                print("P", end=" ")  # Pac-Man
            elif (x, y) == ghost_pos:
                print("G", end=" ")  # Ghost
            elif grid[y][x] == 1:
                print("#", end=" ")  # Wall
            else:
                print(".", end=" ")  # Empty space
        print()
    print("\nMove Pac-Man with W/A/S/D keys. Press Q to quit.\n")

def main():
    # Initialize grid, positions, and walls
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    pacman_pos = (1, 1)
    ghost_pos = (8, 8)

    # Add some walls
    for i in range(3, 7):
        grid[5][i] = 1

    while True:
        display_grid(grid, pacman_pos, ghost_pos)

        # Check for game over
        if pacman_pos == ghost_pos:
            print("Game Over! The ghost caught Pac-Man!")
            break

        # Get user input for Pac-Man's movement
        move = input("Your move (W/A/S/D): ").upper()
        if move == 'Q':
            print("Thanks for playing!")
            break
        if move in DIRECTIONS:
            new_pos = (pacman_pos[0] + DIRECTIONS[move][0], pacman_pos[1] + DIRECTIONS[move][1])
            if 0 <= new_pos[0] < GRID_SIZE and 0 <= new_pos[1] < GRID_SIZE and grid[new_pos[1]][new_pos[0]] != 1:
                pacman_pos = new_pos

        # Ghost movement using A* pathfinding
        path = a_star(ghost_pos, pacman_pos, grid)
        if len(path) > 1:
            ghost_pos = path[1]

        time.sleep(0.2)

if __name__ == "__main__":
    main()
