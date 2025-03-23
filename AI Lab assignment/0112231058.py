import heapq

def heuristic(a, b):
    
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(maze, start, end):
    if maze[start[0]][start[1]] != 0 or maze[end[0]][end[1]] != 0:
        return "No path found"
    rows, cols = len(maze), len(maze[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    cost = {start: heuristic(start,end)}
    while open_set:
        current = heapq.heappop(open_set)[1]
        
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        
        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] == 0:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return None


rows = int(input("Enter number of rows: "))
cols = int(input("Enter number of columns: "))
maze = []
print("Enter the maze row by row (0 for open cell, 1 for blocked cell):")
for i in range(rows):
  row = list(map(int, input().split()))
  if len(row) != cols:
    print("Invalid row length. Please enter the row again.")
    row = list(map(int, input().split()))
  maze.append(row)
start = tuple(map(int, input("Enter the start point (row and column): ").split()))
end = tuple(map(int, input("Enter the end point (row and column): ").split()))
path = a_star_search(maze, start, end)
if path:
    total_cost = len(path) - 1
    print("Path found:", path)
    print("Cost:", total_cost)
else:
    print("No path found")

