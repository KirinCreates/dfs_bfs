import random

def create_maze(width, height):
    """
    Generates a maze using the Depth-First Search algorithm.
    Width and height must be odd numbers.
    """
    if width % 2 == 0 or height % 2 == 0 or width < 3 or height < 3:
        raise ValueError("Width and height must be odd and at least 3.")

    # Initialize the grid with walls ('#')
    # Use a list of lists for easy 2D manipulation
    maze = [['#' for _ in range(width)] for _ in range(height)]

    # Start and Goal points for carving and final placement
    # Must be on open path cells (odd indices)
    start_x, start_y = 1, 1
    goal_x, goal_y = width - 2, height - 2

    # DFS function to carve paths
    def visit(x, y):
        maze[y][x] = ' ' # Carve out the current cell (floor)
        
        # Define possible directions and shuffle them for randomness
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # (dx, dy)
        random.shuffle(directions)

        for dx, dy in directions:
            next_x, next_y = x + 2 * dx, y + 2 * dy
            wall_x, wall_y = x + dx, y + dy

            # Check if the next cell is within bounds and is still a wall
            if 0 <= next_x < width and 0 <= next_y < height and maze[next_y][next_x] == '#':
                maze[wall_y][wall_x] = ' ' # Carve out the wall between
                visit(next_x, next_y)      # Recursively visit the next cell

    # Start the carving from the start point
    visit(start_x, start_y)

    # Place the start and goal markers
    maze[start_y][start_x] = 'A'
    maze[goal_y][goal_x] = 'B'

    return maze

def save_maze_to_file(maze, filename="maze4.txt"):
    """
    Saves the maze (list of lists of characters) to a .txt file.
    """
    with open(filename, 'w') as f:
        for row in maze:
            f.write(''.join(row) + '\n')
    print(f"Maze saved to {filename}")

# --- Configuration and Execution ---

# Set the dimensions (must be odd)
MAZE_WIDTH = 79
MAZE_HEIGHT = 79

try:
    # 1. Generate the maze
    new_maze = create_maze(MAZE_WIDTH, MAZE_HEIGHT)

    # 2. Save the maze to a .txt file
    save_maze_to_file(new_maze)

    # Optional: Print the maze to the console for a quick view
    print("\nGenerated Maze Preview:")
    for row in new_maze:
        print(''.join(row))

except ValueError as e:
    print(f"Error: {e}")