#!/usr/bin/env python3
import sys
import random

walls_horizontal = []
walls_vertical = []


class Node:
    left = None
    right = None
    door = None
    region = [[], []]


# recursively populates a binary tree, also populate globals: walls_horizontal, walls_vertical
def bsp(node):
    if node is None:
        return

    direction = random.randrange(2)  # 0 = horizontal/row split, 1 = vertical/column split
    region_size = node.region[1][direction] - node.region[0][direction]
    if region_size < 1:  # cannot divide any further
        return

    split = random.randrange(region_size)
    split_loc = split + node.region[0][direction]
    node.left = Node()
    node.right = Node()

    direction_perpendicular = int(not direction)  # door is perpendicular to split direction
    range_perpendicular = node.region[1][direction_perpendicular] - node.region[0][direction_perpendicular]
    node.door = random.randrange(range_perpendicular + 1) + node.region[0][direction_perpendicular]

    wall_entry = node.region[0][direction_perpendicular]
    wall_length = range_perpendicular + 1

    if direction == 0:  # horizontal/row split
        node.left.region = [[node.region[0][0], node.region[0][1]], [node.region[0][0] + split, node.region[1][1]]]
        node.right.region = [[node.region[0][0] + (split + 1), node.region[0][1]], [node.region[1][0], node.region[1][1]]]
        walls_horizontal.append([split_loc, wall_entry, wall_length, node.door])
        sys.stdout.write('horizontal ')
    else:  # vertical/column split
        node.left.region = [[node.region[0][0], node.region[0][1]], [node.region[1][0], node.region[0][1] + split]]
        node.right.region = [[node.region[0][0], node.region[0][1] + (split + 1)], [node.region[1][0], node.region[1][1]]]
        walls_vertical.append([split_loc, wall_entry, wall_length, node.door])
        sys.stdout.write('vertical ')
    sys.stdout.write('split = ' + str(split_loc) + ', door = ' + str(node.door))
    print(', wall_length = ' + str(wall_length) + ', wall_entry = ' + str(wall_entry))
    print('left = ' + str(node.left.region))
    print('right = ' + str(node.right.region))

    # now do it recursively..
    bsp(node.left)
    bsp(node.right)
    return


# using wall/door data populated by bsp, create a matrix representing the maze layout
def walls_and_doors(rows, cols):
    horizontal_matrix = [[0 for x in range(cols)] for y in range(rows - 1)]
    vertical_matrix = [[0 for x in range(cols - 1)] for y in range(rows)]
    matrix = [horizontal_matrix, vertical_matrix]
    walls = [walls_horizontal, walls_vertical]
    for i in range(2):
        for wall in walls[i]:
            split_loc = wall[0]
            wall_start = wall[1]
            wall_length = wall[2]
            door = wall[3]
            for j in range(wall_length):
                y = j + wall_start
                if y != door:
                    if i == 0:
                        matrix[i][split_loc][y] = 1
                    else:
                        matrix[i][y][split_loc] = 1
        # print('matrix[' + str(i) + '] = ' + str(matrix[i]))
    return matrix


# S for start, X for exit. "-" and "|" represent walls, and "+" are corners
def draw(rows, cols, dungeon_matrix):
    horizontal_matrix = dungeon_matrix[0]
    vertical_matrix = dungeon_matrix[1]

    for x in range(0, 2*rows + 1):
        if x == 0 or x == 2*rows:  # draw our top and bottom line
            for y in range(0, cols):
                sys.stdout.write("+-")
            print("+")  # far write character
        else:  # draw the innards of our rectangle
            for y in range(0, 2*cols + 1):
                if y == 0:  # left wall
                    if x % 2 == 0:
                        sys.stdout.write("+")
                    else:
                        sys.stdout.write("|")
                elif y == 2*cols:  # right wall
                    if x % 2 == 0:
                        print("+")
                    else:
                        print("|")
                else:
                    y_cord = int((y-1)/2)
                    x_cord = int((x-1)/2)
                    if x % 2 == 0:  # corner, horizontal border, or portal
                        if y % 2 == 0:  # corner
                            sys.stdout.write("+")
                        else:
                            if horizontal_matrix[x_cord][y_cord]:
                                sys.stdout.write('-')
                            else:
                                sys.stdout.write(' ')
                    else:  # vertical wall, or cell
                        if y % 2 == 0:
                            if vertical_matrix[x_cord][y_cord]:
                                sys.stdout.write('|')
                            else:
                                sys.stdout.write(' ')
                        else:  # start, exit, or empty cell
                            # Label the upper left cell with “S” for start and the lower right cell with “X”.
                            if x == 1 and y == 1:
                                sys.stdout.write("S")
                            elif x == (2*rows - 1) and y == (2*cols - 1):
                                sys.stdout.write("X")
                            else:
                                sys.stdout.write(" ")


def main():
    # Request user input for row and column size
    rows = int(input("Enter the number of rows: "))
    cols = int(input("Enter the number of columns: "))

    # Instantiate our maze, assign it a single region
    dungeon = Node()
    dungeon.region = [[0, 0], [rows - 1, cols - 1]]

    # Create a randomly generated maze through a recursive Binary Space Partitioning algorithm
    # end up with walls_horizontal and walls_vertical populated
    bsp(dungeon)

    # walls_and_doors utilizes walls_horizontal and walls_vertical populated above by bsp
    dungeon_matrix = walls_and_doors(rows, cols)

    # draw is provided with everything it uses
    draw(rows, cols, dungeon_matrix)

    # walls should match up with what was spit out by draw
    print('walls_horizontal (split, entry, length, door) = ' + str(walls_horizontal))
    print('walls_vertical (split, entry, length, door)   = ' + str(walls_vertical))


if __name__ == '__main__':
    main()
