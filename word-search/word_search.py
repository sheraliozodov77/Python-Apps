
# Author: Sherali Ozodov
# File name: word_search.py
# Course: CSC 120
# Purpose: The purpose of this program is to find words in a
# grid of letters by reading the contents of two input files:
# one containing a list of words, and the other containing the
# grid of letters. It then checks if the substring is present in
# the word list or not, converts the columns of grid into a list,
# and finds the words in the grid by checking horizontally, vertically,
# and diagonally. The found words are then returned in a sorted list and
# printed out.


def main():
    """
    The main function which calls other functions and prints the output
    """
    lis = input("Name of word-list file: ")
    grid = input("Name of grid-of-letters file: ")
    word_lis = read_grid("dict.txt", lis)[0]
    grid_letter = read_grid("dict.txt", grid)[1]
    for i in (find_word(word_lis, grid_letter)):
        print(i)

def read_grid(word_list, grid_letters):
    """
    Reads the contents of the two input files and returns the two
    lists: one contains the words,
    and one contains the grid of letters.
    Parameters: two input files
    Returns: two lists: one contains the words, and one contains the
    grid of letters.
    """
    word_file = open(word_list, 'r')
    lines = word_file.readlines()
    world_list = []
    for line in lines:
        world_list.append(line.strip())

    grid_file = open(grid_letters, 'r')
    lines = grid_file.readlines()
    grid_list = []
    for line in lines:
        grid_list.append(line.strip().split())

    return world_list ,grid_list


def occurs_in(substr, word_list):
    """
    Check if the substring is present in the word list or not
    arguments: a substring and list of words.
    Parameters: substr, word_list - a list of words
    Returns: a boolean that checks if a substring in list of words
    """
    return substr in word_list


def column2list(grid, n):
    """
    Converts the columns of grid into list.
    Parameters: grid, n
    Returns: return_list
    """
    return_list = []
    for lis in grid:
        return_list.append(lis[n])
    return return_list


def find_word(word_list, grid):
    """
    Finds the words in the grid.
    Parameters: word_list - a list words, grid
    Returns: found words list
    """
    found_words = []
    for word in word_list:
        # Ignores words less than 3 or longer than grid length
        if len(word) < 3 or len(word) > len(grid):
            continue
        # check horizontally
        for row in range(len(grid)):
            # from left to right
            sub_str = "".join(grid[row])
            # from right to left
            sub_str_reverse = "".join(grid[row][::-1])
            if occurs_in(word, sub_str) or \
                    occurs_in(word, sub_str_reverse):
                found_words.append(word)

        # check vertically
        for col in range(len(grid[0])):
            # from top to bottom
            sub_str = "".join(column2list(grid, col))
            # from bottom to top
            sub_str_reverse = "".join(column2list(grid, col)[::-1])
            if occurs_in(word, sub_str) or\
                    occurs_in(word, sub_str_reverse):
                found_words.append(word)

        # check diagonally
        for row in range(len(grid) - len(word) + 1):
            for col in range(len(grid[row]) - len(word) + 1):
                sub_list = []
                for i in range(len(word)):
                    sub_list.append(grid[row +i][col +i])
                sub_str = "".join(sub_list)
                if occurs_in(word, sub_str):
                    found_words.append(word)

    return sorted(found_words)


# call to main function
main()
