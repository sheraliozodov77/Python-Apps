# Author: Sherali Ozodov
# File name: word_grid.py
# Course: CSC 120
# Purpose: This program generates a grid of size grid_size x grid_size
# filled with random lowercase letters from the alphabet. The user is prompted
# to input the grid size and a seed value for the random number generator. The
# grid is then printed in the format of a list of lists, with elements
# separated by commas.


import random
import string

def init():
    """
    Initializes the random seed with user input.
    """
    seed_value = input()
    random.seed(seed_value)

def make_grid(grid_size):
    """
    Creates a grid of size grid_size x grid_size and fills it with random
    lowercase letters from the alphabet.
    Parameters: grid_size (int)
    Returns: return_grid (list)
    """
    return_grid = []
    for i in range(grid_size):
        row = []
        for j in range(grid_size):
            row.append(string.ascii_lowercase[random.randint(0, 25)])
        return_grid.append(row)
    return return_grid

def print_grid(grid):
    """
    Prints the grid in the format of a list of lists, with elements separated
    by commas.
    Parameters: grid (list)
    """
    for row in grid:
        if len(grid) == 1:
            print(row[0])
        else:
            print(','.join(row[:-1]) + ',' + row[-1])

def main():
    """
    Prompts user for grid size and seed value, initializes the random seed,
    generates the grid, and prints it.
    """
    grid_size = int(input())
    init()
    grid = make_grid(grid_size)
    print_grid(grid)

# call the main
main()