import pygame

wall_color = (50, 50, 50)
floor_color = (255, 255, 255)
outline_color = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

def get_neighboring_cell(at_now):
    pass

def can_visit(): #cannot visit if already visited
    pass

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

def create_maze_from_file(file_name):
    maze = []
    with open(file_name, 'r') as file:
        for line in file:
            maze.append(line)
    return maze


def pretty_print_2d_list(l):
    for i in range(len(l)):
        print(l[i])

def draw_rect(screen, outline_color, fill_color, upper_left_x, upper_left_y, width, height):
    border_width = 3
    square = pygame.Rect(upper_left_x, upper_left_y, width, height)
    pygame.Surface.fill(screen, fill_color, square)
    pygame.draw.rect(screen, outline_color, square, border_width)

def main():
    pygame.init()
    width = height = 720
    screen_dims = (width, height)
    screen = pygame.display.set_mode(screen_dims)
    pygame.display.set_caption('BFS and DFS visualizer: Red: Start, green: Goal') 
    clock = pygame.time.Clock()
    running = True

    maze = create_maze_from_file("maze.txt")
    num_rows = len(maze)
    assert(num_rows > 0)
    num_cols = len(maze[0])-1

    rect_width = width / num_cols
    rect_height = height / num_rows

    start_row_idx, start_col_idx = get_start_or_goal_index(maze, num_rows, num_cols, "start")
    goal_row_idx, goal_col_idx = get_start_or_goal_index(maze, num_rows, num_cols, "goal")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(outline_color)

        #Render game here
        for row_idx in range(num_rows):
            at_y = rect_height*row_idx
            for col_idx in range(num_cols):
                at_x = rect_width*col_idx
                draw_cell(maze[row_idx][col_idx], screen, at_x, at_y, rect_width, rect_height)
                print(on_floor(row_idx, row_idx, maze))

        pygame.display.flip()
        clock.tick(60) #60 fps
    pygame.quit()


if __name__ == "__main__":
    main()
