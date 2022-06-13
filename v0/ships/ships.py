import numpy as np

grid_size = 10
grid = np.zeros((grid_size, grid_size), dtype=int)
grid_opp = np.zeros((grid_size, grid_size), dtype=int)
alphabet = "ABCDEFGHIJ"
row_dictionary = {i: alphabet.index(i) for i in alphabet}

class Ship(object):
    """ The Ship class represents the abstraction of the concept of Ship on the board, which is then applied in practice
    by storing a certain value (1) in the entries of the matrices onto which a certain Ship is placed.
    The Ship is conceived as a attribute of the class Player in a precise number depending on the size (and the number
    of lives) of the Ship, for a total number of 10 ships per player.

    Parameters
    ----------
    start_idx: list
        2-member list comprising the row and column indexes of the matrix entry where the ship start from.
    end_idx: list
        2-member list comprising the row and column indexes of the matrix entry where the ship end to.

    Attributes
    ----------
    start_row: int
        the row index of the matrix entry where the ship starts from, i.e. start_idx[0]
    start_col: int
        the row index of the matrix entry where the ship starts from, i.e. start_idx[1]
    end_row: int
        the row index of the matrix entry where the Ship ends to, i.e. end_idx[0]
    end_col: int
        the col index of the matrix entry where the Ship ends to, i.e. end_idx[1]
    dead: bool
        a value set to False until the remaining lives of the instance of Ship arrive to 0
    list_coordinates: list
        a list of lists comprising all the pairs row-col indexes of each square of the board
        onto which the Ship is placed
    shadow: list
        a list of lists comprising all the pairs row-col indexes lying along any placed ship
        (i.e. along the borders)
    vertical: bool
        a boolen standing for whether the Ship is horizontal or vertical
    size: int
        an attribute storing the length of the Ship
    life: int
        an attribute storing the number of lives available to each Ship, which is at first set equal
        to the size and then automatically updated whenever the Ship is hit
    name: str
        the attribute storing the name of the Ship, used to uniquely identify the type of the Ship
        and automatically generated whenever a Ship is placed
    """
    def __init__(self, start_idx, end_idx):
        self.start_row = start_idx[0]
        self.start_col = start_idx[1]
        self.end_row = end_idx[0]
        self.end_col = end_idx[1]
        self.list_coordinates = []
        self.shadow = []
        # we store evert index of matrix on which ship lies, together with their type, and their remaining lives

        if self.start_col < self.end_col:
            self.vertical = False
            self.size = int(self.end_col - self.start_col + 1)
            self.list_coordinates = [[self.start_row, i] for i in range(self.start_col, self.end_col + 1)]
            for i in range(self.start_row - 1, self.start_row + 2):
                for j in range(self.start_col - 1, self.end_col + 2):
                    self.shadow.append([i, j])
            for occupied in self.list_coordinates:
                self.shadow.remove(occupied)
        if self.start_col > self.end_col:
            self.vertical = False
            self.size = int(self.start_col - self.end_col + 1)
            self.list_coordinates = [[self.start_row, i] for i in range(self.end_col, self.start_col + 1)]
            for i in range(self.start_row - 1, self.start_row + 2):
                for j in range(self.end_col - 1, self.start_col + 2):
                    self.shadow.append([i, j])
            for occupied in self.list_coordinates:
                self.shadow.remove(occupied)
        if self.start_row < self.end_row:
            self.vertical = True
            self.size = int(self.end_row - self.start_row + 1)
            self.list_coordinates = [[i, self.start_col] for i in range(self.start_row, self.end_row + 1)]
            for i in range(self.start_col - 1, self.start_col + 2):
                for j in range(self.start_row - 1, self.end_row + 2):
                    self.shadow.append([j, i])
            for occupied in self.list_coordinates:
                self.shadow.remove(occupied)
        if self.start_row > self.end_row:
            self.vertical = True
            self.size = int(self.start_row - self.end_row + 1)
            self.list_coordinates = [[i, self.start_col] for i in range(self.end_row, self.start_row + 1)]
            for i in range(self.start_col - 1, self.start_col + 2):
                for j in range(self.end_row - 1, self.start_row + 2):
                    self.shadow.append([j, i])
            for occupied in self.list_coordinates:
                self.shadow.remove(occupied)
        if (self.start_row == self.end_row) and (self.start_col == self.end_col):
            self.vertical = False
            self.size = 1
            self.list_coordinates = [[self.start_row, self.start_col]]
            for i in range(self.start_row - 1, self.start_row + 2):
                for j in range(self.start_col - 1, self.start_col + 2):
                    self.shadow.append([i, j])
            self.shadow.remove([self.start_row, self.start_col])
        self.life = self.size

        self.name = ""
        if self.size == 5:
            self.name = "AircraftCarrier"
        if self.size == 4:
            self.name = "Battleship"
        if self.size == 3:
            self.name = "Destroyer"
        if self.size == 2:
            self.name = "Submarine"
        if self.size == 1:
            self.name = "PatrolBoat"

class AircraftCarrier(Ship):
    """
    Child class of Ship representing the longest Ship, with size 5 (only one quantity available to each Player)
    """
    def __init__(self):
        self.size = 5
        self.name = "AircraftCarrier"

class Battleship(Ship):
    """
    Child class of Ship representing the Ship with size 4 (only one quantity available to each Player)
    """
    def __init__(self):
        self.size = 4
        self.name = "Battleship"

class Destroyer(Ship):
    """
    Child class of Ship representing the Ship with size 3 (two available to each Player)
    """
    def __init__(self):
         self.size = 3
         self.name = "Destroyer"

class Submarine(Ship):
    """
    Child class of Ship representing the Ship with size 2 (three available to each Player)
    """
    def __init__(self):
         self.size = 2
         self.name = "Submarine"

class PatrolBoat(Ship):
    """
    Child class of Ship representing the Ship with size 1 (three available to each Player)
    """
    def __init__(self):
         self.size = 1
         self.name = "PatrolBoat"

# VISUALIZE
def visualize_grid(grid, camu = False):
    """ This is the main function for visualization. It is called whenever an information/change regarding the board
    of any player is concerned. It outputs on the Terminal the board, in plain sight or in camouflage mode depending
    on whether it is the own board of the Player or the Opponent's one.

    Parameters
    ----------
    grid: array
        the numpy 10x10 matrix representing the board (attribute of Player) which has to be visualized

    camu: bool
        boolean value that determines how the matrix is represented.
        if set to False, it means we are referencing the Player's board and both the placed ships and the positions
        which have been targeted by the opponent since the beginning of the game are printed.
        if set to True, we want to visualize the opponent's grid in order to provide the Player with a visual help
        on where to place the next shot. in this case, only the shots made since the beginning of the game are visible
        (and whether they were on point or not)

    LEGEND
    ------
    "0" = placed ship (1)
    "X" = hit ship (-1)
    "#" = shot in the water (2)
    "." = water (0)
    """
    alphabet = "ABCDEFGHIJ"

    row_indexes = list(range(1, 11))
    row_indexes.insert(0, " ")
    grid_visual = [list(grid[i]) for i in range(grid_size)]

    for row in range(grid_size + 1):
        print(row_indexes[row], end = "\t")
        for col in range(grid_size):
            if row == 0:
                print(alphabet[col], end = " ")
                continue
            if not camu:
                if grid_visual[row-1][col] == 1:
                    print("O", end = " ")
                if grid_visual[row-1][col] == -1:
                    print("X", end=" ")
                if grid_visual[row-1][col] == 2:  # we store the shots in the water
                    print("#", end=" ")
                if grid_visual[row-1][col] == 0:
                    print(".", end=" ")
            if camu:
                if grid_visual[row-1][col] == 1:
                    print(" ", end = " ")
                if grid_visual[row-1][col] == -1:
                    print("X", end=" ")
                if grid_visual[row-1][col] == 2:  # we store the shots in the water
                    print("#", end=" ")
                if grid_visual[row-1][col] == 0:
                    print(" ", end=" ")
        print("")