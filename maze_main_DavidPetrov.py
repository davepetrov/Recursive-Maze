#Recursion: Solving a Maze
#By David P
#Solves an automically generated maze

from time import sleep
import maze_generator
from random import randint, choice
import pygame
pygame.init()

#-------------------------------------------------------------------------- Variables --------------------------------------------------------------------------#
width = None       # Width of Screen
height = None      # Height of Screen
end_x = None       # X coordinate of 'G'
end_y = None       # Y coordinate of 'G'
start_x = None     # X coordinate of 'S'
start_y = None     # Y coordinate of 'S'
ppb = 10           # Pixels Per Block

#Colours
BROWN =  (118, 178, 149)
D_BROWN =  (194, 234, 235)
DD_BROWN =  (129, 216, 212)
L_GREEN =  (  199,   234, 70)
GREEN = (0, 59,   31)
D_GREEN = (0, 79,   21)
YELLOW = (249,166,2)
L_YELLOW = (249,180,2)
RED = (120, 120, 120)

#-------------------------------------------------------------------------- Start (load), end functions --------------------------------------------------------------------------#
def load_maze(file_name='map.txt'):
    '''
    (file)--> (list,int,int)

    Returns the maze and the dimentions given the file
    
    Loads the maze with the use of the maze generator imported module
    Reads the maze file and uses it to set it into a 2D list (map)'''
    file_in = open(file_name,'r')                                                           # readlines()
    lines = file_in.readlines()                                                             # Returns a list with each line as an element.      
    maze = [list(lines[i][:-1]) for i in range(len(lines))]
    file_in.close()
    height=len(maze)*ppb                                                                    #Sets the height of the screen (y*pixels per block)
    width=len(maze[0])*ppb                                                                  #Sets the width of the screen (x*pixels per block)
    return maze,height,width
    
def check_win(maze,x,y,end_y,end_x):
    '''
    (list, int, int, int, int)--> (True)

    Returns True if the function is called
    
    Returns the maze and the dimentions given the file
    Checks if the selected block is on the coordinates of the goal'''
    if maze[y][x]==maze[end_y][end_x]:
        print('Complete')
        pygame.draw.rect(screen, L_YELLOW, [end_x*ppb, end_y*ppb, ppb, ppb])            #Draws the gold square on the 'G' when the maze is completed

        pygame.display.update()
        maze[start_y][start_x]='S'
        print_maze(maze)
        return True

#-------------------------------------------------------------------------- Coordinate/Position Gunctions --------------------------------------------------------------------------#
    
def random_coordinates_generator(maze):
    '''
    (list)--> (list, int, int, int, int)

    Returns the maze and the start & end coordinates
    
    Sets random coordinates for the start and goal block within the open spaces of the maze'''
    open_coords=[(row,col) for row in range(len(maze)) for col in range(len(maze[row])) if maze[row][col]!= '#']    #sets  x & y coordinates not placed over a # sign

    start = choice(open_coords)
    maze[start[0]][start[1]] = 'S'                                                                                  #sets 'S' over the the start coordinates that were picked at random
    open_coords.remove(start)

    goal = choice(open_coords)
    maze[goal[0]][goal[1]] = 'G'                                                                                     #sets 'G' over the the goal coordinates that were picked at random

    return maze, start[1], start[0], goal[1],  goal[0]
    
def update_pos(maze,y,x,type_of_move):
    '''
    (file)--> ()

    Does not return anything but it updates the maze
    
    Updates the position of the block depending on the type of move'''
    if type_of_move == 'regular': maze[y][x] = '•'                                                                  #Regular: Replaces the seleted block with a red square
    elif type_of_move == 'backtrack': maze[y][x] = '-'                                                              #Backtrack: Replaces the seleted block with a Grey square
    display(maze)
    #sleep(.05)

#-------------------------------------------------------------------------- Print/Display --------------------------------------------------------------------------#
def print_maze(maze):
    '''
    (list)--> ()

    Does not return anything but it prints maze in the console

    Prints the maze using map (2D matrix) on python console'''
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            print(maze[row][col], end='')
        print()
    print('-'*60)

def display(maze):
    '''
    (list)--> ()

    Does not return anything but it displays maze in the screen

    Displays the maze using map (2D matrix) on pygame screen'''
    ev = pygame.event.poll()
    ev.type == pygame.QUIT
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == '#':
                if col%2==0: pygame.draw.rect(screen, GREEN, [col*ppb, row*ppb, ppb, ppb])
                if col%2==1: pygame.draw.rect(screen, D_GREEN, [col*ppb, row*ppb, ppb, ppb])
            elif maze[row][col] == '•':
                if col%2==0: pygame.draw.rect(screen, D_BROWN, [col*ppb, row*ppb, ppb, ppb])
                if col%2==1: pygame.draw.rect(screen, DD_BROWN, [col*ppb, row*ppb, ppb, ppb])
            elif maze[row][col] == 'G': pygame.draw.rect(screen, YELLOW, [col*ppb, row*ppb, ppb, ppb])
            elif maze[row][col] == ' ': pygame.draw.rect(screen, BROWN, [col*ppb, row*ppb, ppb, ppb])
            elif maze[row][col] == '-': pygame.draw.rect(screen, RED, [col*ppb, row*ppb, ppb, ppb])
    pygame.draw.rect(screen, L_GREEN, [start_x*ppb, start_y*ppb, ppb, ppb])                                             #Automaticaly colours the start block in green
    pygame.display.update()

#-------------------------------------------------------------------------- Main solver --------------------------------------------------------------------------#
def maze_solver(maze, y, x, end_y, end_x):
    '''
    (list,int,int,int,int)--> ()

    Solves the maze using all the methods in one'''
    if maze[y][x] == '#':  return False                                                                                 # Stop recursion from going forward and must return a result: - Hit a wall
    elif check_win(maze,x,y, end_y, end_x):return True                                                                  #                                                             - Reached the target(goal)
    elif maze[y][x] == ('•'):return False                                                                               #                                                             - Went into a location which had already been visited

    update_pos(maze,y,x,'regular')                                                                                      # Updates the position using update_pos method - updates, prints and displays

    if maze_solver(maze, y-1, x, end_y, end_x): return True                                                             # Moves North
    elif maze_solver(maze, y, x+1, end_y, end_x): return True                                                           # Moves East
    elif maze_solver(maze, y+1, x, end_y, end_x): return True                                                           # Moves South
    elif maze_solver(maze, y, x-1, end_y, end_x): return True                                                           # Moves West

    update_pos(maze,y,x,'backtrack')                                                                                    # If path does not exist from any of the four locations, unmarks current location as part of the solution path
    return False

#------------------------------------------------ Objects, Declerations (main) ------------------------------------------------#
maze, height, width = load_maze()
screen=pygame.display.set_mode((width, height))
maze, start_x, start_y, end_x, end_y=random_coordinates_generator(maze)         # Generates start and end coordinates                                                             # Prints the starting maze
maze_solver(maze, start_y, start_x, end_y, end_x)                               # Solves the maze
