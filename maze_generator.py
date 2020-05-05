#########################################
# Programmer: Nathan Moore
# Adaptation: Mrs.G 
# File Name: maze_generator.py
# Description: This program generates a maze of arbitrary size and saves it in a file.
# Source: http://natewm.com/blog/2012/01/python-recursive-maze-example/
#########################################
import random
 
def makeMaze(width, height):            # maze dimensions are doubled, to include the walls
    maze = [[0 for j in range(width*2)] for i in range(height*2)]
    recurseMaze(maze, (width // 2) * 2, (height // 2) * 2, 0, 0)
    return maze                         # begin recursion starting in the center

def recurseMaze(maze, x, y, dirx, diry):
    if not 0 <= y < len(maze) or not 0 <= x < len(maze[0]) or maze[y][x] != 0:
        return                          # base case: returns if reaches the borders
                                        # or if current location is not a wall
    maze[y-diry][x-dirx] = 1            #
    maze[y][x] = 1                      # mark current location and the previous one as alley
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    random.shuffle(directions)
    for dx, dy in directions:           # recurse in the four directions
        recurseMaze(maze, x + dx * 2, y + dy * 2, dx, dy)

def mazeString(maze, chars):            # converts zeroes to walls and ones to alleys
    s = chars[0] * (len(maze[0]) + 1) + "\n" # adds border at the top
    for row in maze:                    # adds border to the left
        s += chars[0]
        for cell in row:
            s += chars[cell]
        s += "\n"
    return s

#---------------------------------------#
# main program                          #
#---------------------------------------#
width = int(input("Enter width (number of alleys): "))
height = int(input("Enter height (number of alleys): "))
maze = makeMaze(width,height)

maze_string = mazeString(maze, ("#", " "))

file_out = open('map.txt','w')
file_out.write(maze_string)
file_out.close()
