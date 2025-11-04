import pygame

#DFS implementation first

wall_color = (50, 50, 50)
floor_color = (255, 255, 255)
outline_color = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

# need an all node list to pop from
def dfs(current_row_idx, current_col_idx, visited, path, maze_num_rows, maze_num_cols, maze, goal_row_idx, goal_col_idx):
    #Add current cell to visited
    visited.append((current_row_idx, current_col_idx))
    if current_row_idx == goal_row_idx and current_col_idx == goal_col_idx:
        return path
    next_neighbors = next_step(current_row_idx, current_col_idx, visited, path, maze_num_rows, maze_num_cols, maze)
    for next_neighbor in next_neighbors: #next neighbor is not visited and not a wall
        path[next_neighbor] = (current_row_idx, current_col_idx)
        dfs(*next_neighbor, visited, path, maze_num_rows, maze_num_cols, maze, goal_row_idx, goal_col_idx)
        if (goal_row_idx, goal_col_idx) in path:
            break
    return path

#takes next step in DFS or BFS looks in visited and only return not visited neighbors
def next_step(current_row_idx, current_col_idx, visited, path, maze_num_rows, maze_num_cols, maze):
    neighbors_list = get_neighbors(current_row_idx, current_col_idx, maze_num_rows, maze_num_cols, maze)
    # print(neighbors_list)
    can_visit_neighbors = []
    for neigh in neighbors_list:
        if neigh not in visited: #do not go to this neighbor becuase it is visited
            can_visit_neighbors.append(neigh)
    return can_visit_neighbors

#get neighbors that are not floor tiles and not walls
def get_neighbors(current_row_idx, current_col_idx, num_rows, num_cols, maze):
    #tile that you can visit: not visited and not a wall
    left = (current_row_idx, current_col_idx - 1)
    right = (current_row_idx, current_col_idx + 1)
    up = (current_row_idx - 1, current_col_idx)
    down = (current_row_idx + 1, current_col_idx)
    neighbors = []
    if up[0] >= 0 and on_floor(*up, maze):
        neighbors.append(up)
    if down[0] < num_rows and on_floor(*down, maze):
        neighbors.append(down)
    if left[1] >= 0 and on_floor(*left, maze):
        neighbors.append(left)
    if right[1] < num_cols and on_floor(*right, maze):
        neighbors.append(right)
    return neighbors

def get_start_or_goal_index(maze, num_rows, num_cols, option): #option is 'start' or 'goal'
    assert( option == "start" or option == "goal" )
    comparator = "B"
    if option == "start":
        comparator = "A"

    for row_idx in range(num_rows):
        for col_idx in range(num_cols):
            if maze[row_idx][col_idx] == comparator:
                return (row_idx, col_idx) 
    return (None, None)

#on a cell that is not a wall
def on_floor(row_idx, col_idx, maze):
    is_floor = (maze[row_idx][col_idx] == " " or maze[row_idx][col_idx] == "A" or  maze[row_idx][col_idx] == "B")
    return is_floor

def draw_cell(maze_content, screen, at_x, at_y, rect_width, rect_height): #rect_info is a tuple: (screen, outline_color, wall_color, rect_width*i, rect_height*j, rect_width, rect_height)
    fill_color = wall_color
    if maze_content == "#": #wall
        fill_color = wall_color
    elif maze_content == " ":
        fill_color = floor_color
    elif maze_content == "A":
        fill_color = red
    elif maze_content == "B":
        fill_color = green
    draw_rect(screen, outline_color, fill_color, at_x, at_y, rect_width, rect_height)

def draw_path(screen, outline_color, path, start_cell, goal_cell, rect_width, rect_height):
    for from_cell, to_cell in reversed(path): #path is list that stores (from_cell, to_cell) items
        from_row_idx, from_col_idx = from_cell
        to_row_idx, to_col_idx = to_cell
        if from_cell == (-1, -1) or from_cell == start_cell:
            continue
        blue = (0, 0, 255)
        draw_rect(screen, outline_color, blue, from_col_idx*rect_width, from_row_idx*rect_height, rect_width, rect_height)

def create_maze_from_file(file_name):
    maze = []
    with open(file_name, 'r') as file:
        for line in file:
            maze.append(line)
    return maze

def draw_rect(screen, outline_color, fill_color, upper_left_x, upper_left_y, width, height):
    border_width = 3
    square = pygame.Rect(upper_left_x, upper_left_y, width, height)
    pygame.Surface.fill(screen, fill_color, square)
    pygame.draw.rect(screen, outline_color, square, border_width)

def main():
    pygame.init()
    width = height = 800
    screen_dims = (width, height)
    screen = pygame.display.set_mode(screen_dims)
    pygame.display.set_caption('BFS and DFS visualizer: Red: Start, green: Goal') 
    clock = pygame.time.Clock()
    running = True

    maze = create_maze_from_file("maze2.txt")
    num_rows = len(maze)
    assert(num_rows > 0)
    num_cols = len(maze[0])-1

    rect_width = width / num_cols
    rect_height = height / num_rows

    start_row_idx, start_col_idx = get_start_or_goal_index(maze, num_rows, num_cols, "start")
    goal_row_idx, goal_col_idx = get_start_or_goal_index(maze, num_rows, num_cols, "goal")

    assert(start_row_idx != None or start_col_idx != None or goal_row_idx != None or goal_col_idx != None)

    visited = [] # LIFO stack
    path = {(start_row_idx, start_col_idx): (-1,-1)} #key: to cell, value: from cell. This var is reversed from result_path

    path = dfs(start_row_idx, start_col_idx, visited, path, num_rows, num_cols, maze, goal_row_idx, goal_col_idx)

    #Backtrack from goal to start
    to_cell = (goal_row_idx, goal_col_idx)
    result_path = []
    print(to_cell, end=", ")
    while True:
        if to_cell == (-1, -1): 
            break
        from_cell = path[to_cell]
        result_path.append((from_cell, to_cell)) #remember that the path starts in the end. reverse list or iterate from end
        to_cell = from_cell
    print("")

    while running:
        #listen for quit-event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(outline_color)

        #Draw maze
        for row_idx in range(num_rows):
            at_y = rect_height*row_idx
            for col_idx in range(num_cols):
                at_x = rect_width*col_idx
                draw_cell(maze[row_idx][col_idx], screen, at_x, at_y, rect_width, rect_height)

        draw_path(screen, outline_color, result_path, (start_row_idx, start_col_idx), (goal_row_idx, goal_col_idx), rect_width, rect_height)

        pygame.display.flip()
        clock.tick(60) #60 fps
    pygame.quit()


if __name__ == "__main__":
    main()
