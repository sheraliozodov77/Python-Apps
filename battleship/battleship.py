
# Author: Sherali Ozodov
# File name: battleship.py
# Course: CSC 120
# Purpose: This program is a simplified version of the classic game
# Battleship, in which the player places a fleet of ships on a board
# and then takes turns guessing the locations of the opponent's ships.
# The program reads in a placement file with the starting locations of
# the ships, reads in a guess file with the player's guesses, and then
# processes each guess to determine whether it is a hit or a miss. The
# program continues until all of the opponent's ships have been sunk,
# at which point the game is over.

import sys

class GridPos:
    """This is a class for a grid position that represents each cell
    on the board
    """
    def __init__(self, x, y, ship=None):
        # Initialize the GridPos object with its x, y
        # position and whether it contains a ship or not
        self.x = x
        self.y = y
        self.ship = ship
        # Keep track of whether this position has been previously guessed
        # or not
        self.prev_guessed = False

    def __str__(self):
        if self.ship is None:
            return "."
        elif self.prev_guessed:
            return "X"
        else:
            return "O"


class Board:
    """This is a class for the game board.
    """
    def __init__(self):
        # Initialize the board as a 10x10 grid of GridPos objects
        self.grid = []
        for x in range(10):
            row = []
            for y in range(10):
                row.append(GridPos(x, y))
            self.grid.append(row)
        # Keep track of the ships that are placed on the board
        self.ships = []

    def place_ship(self, ship):
        """
        Places a ship object on the board.

        Parameters:
            ship : The ship object to place on the board.
        Returns:
            None
        """
        for x, y in ship.positions:
            self.grid[x][y].ship = ship
        self.ships.append(ship)

    def process_guess(self, x, y):
        """
        Processes a guess made by the player.

        Parameters:
            x : The x-coordinate of the guess.
            y : The y-coordinate of the guess.
        Returns:
            A boolean value indicating whether the guess was
            successful or not.
        """
        if not (0 <= x <= 9 and 0 <= y <= 9):
            print("illegal guess")
            return False

        pos = self.grid[x][y]

        if pos.prev_guessed:
            # if the position was already guessed and has a ship
            if pos.ship is not None:
                # inform the player that they've hit the same ship again
                print("hit (again)")
            else:
                print("miss (again)")
            return False

        pos.prev_guessed = True
        if pos.ship is None:
            print("miss")
        else:
            # if the position has a ship, decrease the number of
            # not-hit positions
            pos.ship.not_hit_pos -= 1
            if pos.ship.not_hit_pos == 0:
                print(f"{pos.ship.kind} sunk")
                # remove the ship from the list of ships
                self.ships.remove(pos.ship)
                # if there are no more ships left, the game is over
                if not self.ships:
                    print("all ships sunk: game over")
                    sys.exit(0)
            else:
                print("hit")

        return True

    def __str__(self):
        res = ""
        for row in self.grid:
            res += " ".join(str(pos) for pos in row) + "\n"
        return res


class Ship:
    """This class represents a ship on the board.

    The constructor creates a ship object with attributes for the kind
    of ship, given as a string,its size, given as an int, and its
    positions, which is a list of tuples indicating the
    positions of the ship on the board.
    """
    def __init__(self, kind, size, positions):
        # Initialize the ship kind, size, positions and not_hit_pos
        self.kind = kind
        self.size = size
        self.positions = positions
        self.not_hit_pos = size

    def __str__(self):
        return self.kind

def read_placement(placement_file):
    """Reads the placement file and returns its contents.

    Parameters:
        placement_file : A string containing the path of the placement file.
    Returns:
        A list of strings containing the contents of the placement file.
    """
    with open(placement_file, 'r') as file:
        lines = file.readlines()

    if len(lines) != 5:
        print("ERROR: fleet composition incorrect")
        sys.exit(0)

    return lines

def validate_and_extract_ship(line, size_ship):
    """Validates and extracts the information from a line in the placement
    file.

    Parameters:
        line : A string containing information about a single ship
        size_ship : A dictionary containing the sizes of each kind of ship.

    Returns:
        A tuple containing the kind of the ship, and its positions as
        (x1, y1) and (x2, y2).
    """
    kind = line[0]

    # Check if the ship type is valid
    if kind not in {'A', 'B', 'S', 'D', 'P'}:
        print(f"ERROR: incorrect ship type: {' '.join(line)}")
        sys.exit(0)

    x1, y1, x2, y2 = map(int, line[1:])

    # Check if the ship is within bounds
    if not (0 <= x1 <= 9 and 0 <= y1 <= 9 and 0 <= x2 <= 9 and 0 <= y2 <= 9):
        print(f"ERROR: ship out-of-bounds: {' '.join(line)}")
        sys.exit(0)

    # Check if the ship is horizontal or vertical
    if x1 != x2 and y1 != y2:
        print(f"ERROR: ship not horizontal or vertical: {' '.join(line)}")
        sys.exit(0)

    # Check if the ship has length greater than 1
    if (x1, y1) == (x2, y2):
        print(f"ERROR: ship with length 1: {' '.join(line)}")
        sys.exit(0)

    # Check if the ship size matches the expected size
    length = abs(x1 - x2) + abs(y1 - y2) + 1
    if length != size_ship[kind]:
        print(f"ERROR: incorrect ship size: {' '.join(line)}")
        sys.exit(0)

    # Calculate and return the ship's positions
    return kind, x1, y1, x2, y2

def calculate_positions(x1, y1, x2, y2):
    """Calculates the positions of a ship given its endpoints.

     Parameters:
        x1, y1: the coordinates of the first endpoint
        x2, y2: the coordinates of the second endpoint
     Returns:
        A list of tuples representing the positions of the ship on
        the board.
     """
    positions = []
    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            positions.append((x1, y))
    else:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            positions.append((x, y1))
    return positions


def process_placement(placement_file, size_ship):
    """Processes the ship placement file and returns a list of Ship objects.

    Parameters:
        placement_file: The path to the ship placement file
        size_ship: A dictionary mapping ship kinds to their sizes

    Returns:
        A list of Ship objects representing the ships placed on the board.
    """
    lines = read_placement(placement_file)

    ships = []
    occupied_positions = set()

    for line in lines:
        line = line.strip().split()
        kind, x1, y1, x2, y2 = validate_and_extract_ship(line, size_ship)
        positions = calculate_positions(x1, y1, x2, y2)

        # check for overlapping ships
        for position in positions:
            if position in occupied_positions:
                print(f"ERROR: overlapping ship: {' '.join(line)}")
                sys.exit(0)
            occupied_positions.add(position)

        # create the ship object and add it to the list
        ship = Ship(kind, size_ship[kind], positions)
        ships.append(ship)

    return ships

def process_guess(self, x, y):
    """Processes a player guess and updates the game state accordingly.

    Parameters:
        x, y: The coordinates of the guess on the board
    Returns:
        None
    """

    # check if the guess is legal
    if not (0 <= x < 10 and 0 <= y < 10):
        print("illegal guess")
        return
    # get the position on the board and check if it has already been guessed
    pos = self.grid[x][y]
    if pos.prev_guessed:
        print("miss (again)")
        return
    # update the board state and print a message accordingly
    pos.prev_guessed = True
    if pos.ship is None:
        print("miss")
    else:
        pos.ship.not_hit_pos -= 1
        if pos.ship.not_hit_pos == 0:
            print(f"{pos.ship.kind} sunk")
            self.ships.remove(pos.ship)
        else:
            print("hit")


def main():
    """The main function that runs the Battleship game.
    """
    placement_file = input()
    guess_file = input()

    size_ship = { 'A': 5, 'B': 4, 'S': 3, 'D': 3, 'P': 2}

    # Create a new board and place the ships
    board = Board()
    ships = process_placement(placement_file,size_ship)
    for ship in ships:
        board.place_ship(ship)
    # Play the game using guesses from guess file
    with open(guess_file) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 2 or not all(part.isdigit() for part in parts):
                print("illegal guess")
                continue

            x, y = map(int, parts)
            if not (0 <= x <= 9 and 0 <= y <= 9):
                print("illegal guess")
                continue
            board.process_guess(x, y)

main()