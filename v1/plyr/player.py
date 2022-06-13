import pygame
import random as rd
import numpy as np

from shps.ships import *
from brd.board  import *

GRID_SIZE = 10

pygame.init()
pygame.font.init()

dictionary={b"A":b"1", b"B":b"2", b"C":b"3", b"D":b"4", b"E":b"5", b"F":b"6", b"G":b"7", b"H":b"8", b"I":b"9", b"J":b"10"}

class Player(object):
    """ The Player class is one of the two players of a classic battleship game on one own.
    It stores all the necessary identifier of the player which are constantly updated during the game, together
    with the main functions for placing and calling the shots to be alternated with the one of the subclass Random(Player).
    Each player is endowed with 10 ships of varying dimensions and a 10x10 board matrix.

    Attributes
    -------
    boats_list: list
        list of the available Ships
    boats: Pygame Group
        attribute containing all the Ships (as Pygame objects)
    own_board: object
        personal instantiation of Board object for Player
    hit_cells: list
        list containing the coordinates (row and column indexes) of the hit cells
    number_ships_sunk: int
        the variable responsible for ending the main loop of the game, whenever the number of ships sunk of a
        certain player is equivalent to the total number of ships available (10).
        it is based on the previous one, since number_ships_sunk increases by 1 every time the remaining lives of
        one of the ships stored in placed_ships go to 0.
    """
    def __init__(self):
        self.aircraft_carrier = AircraftCarrier()
        self.battle_ship1 = Battleship()
        self.destroyer1 = Destroyer(); self.destroyer2 = Destroyer()
        self.submarine1 = Submarine(); self.submarine2 = Submarine(); self.submarine3 = Submarine()
        self.patrol1 = PatrolBoat(); self.patrol2 = PatrolBoat(); self.patrol3 = PatrolBoat()
        self.boats_list = [self.aircraft_carrier, self.battle_ship1, self.destroyer1, self.destroyer2, self.submarine1,
                         self.submarine2, self.submarine3, self.patrol1, self.patrol2, self.patrol3]
        self.own_board = Board()
        self.boats = pygame.sprite.Group()
        self.boats.add(self.boats_list)
        self.hit_cells = []
        self.number_ships_sunk = 0

class Random(object):
    """ The Random class represents the randomized player that constitutes a valid opponent of the user (Player)
        one of the two players of a classic battleship game on one own. In fact, the class Random inherits from Player
        all the behaviours, while redefining through Polymorphism the game behaviours of placing the ships and shooting,
        which clearly are now independent from any terminal input.

        Attributes
        -------
        number_ships: int
            attribute storing the total number of ships available to start with
        own_board: array
            the board variable is a pointer to the personal numpy matrix 10x10 which stores the positions of the placed ships
            together with the ones of the placed shots. It represents a counterpart, i.e. the opponent board for the user
        available_ships: list
            the list storing the names of the ships yet to be placed, it is the basis of the positioning phase which ends only
            when this list is empty. The number of ships is the same as the ones of Player
        available_ships_sizes: list
            the list storing the sizes of the ships yet to be placed and strictly linked to the previous one.
            this list is used to check whether the placed ships are among the available ones on the basis of their dimensions
        occupied_positions: list
            a storing list used to progressively append the coordinates of the placed ships.
            it is mainly used to check whether the positioned ships overlaps with one previously placed
        occupied_shadow: list
            a storing list used to progressively append the portion of the board that lie along the
            sides of any placed ships. it is mainly not to place any ship lying onto one of the indices
            right beside any already ship (i.e. a shadow of indices around the ship)
        placed_ships: list
            a list containing the names of all ships placed, together with their coordinates and their remaining lives.
            it is the main memory storage for the progressive execution of the game
        number_ships_sunk: int
            the variable responsible for ending the main loop of the game, whenever the number of ships sunk of a
            certain player is equivalent to the total number of ships available (10).
        it is based on the previous one, since number_ships_sunk increases by 1 every time the remaining lives of
            one of the ships stored in placed_ships go to 0.
        """
    def __init__(self):
        self.number_ships = 10
        self.own_board = np.zeros((10, 10))
        self.available_ships = ["AircraftCarrier", "Battleship", "Destroyer", "Destroyer", "Submarine",
                                "Submarine", "Submarine", "Patrol", "Patrol", "Patrol"]
        self.available_ships_sizes = [5, 4, 3,
                                      3, 2, 2,
                                      2, 1, 1, 1]
        self.occupied_positions = []
        self.occupied_shadow = []
        self.placed_ships = []
        self.number_ships_sunk = 0

    def validate_ship_position(self, start_row, end_row, start_col, end_col):
        """ At each step of the insertion phase, this function validates the positions given after checking
        both that the implied ship is within the boundaries of the game board and that there is no other ship
        placed there previously. The function is called after the indexes for the placement are either decoded
        (for the Player) or generated (for the Random).

        Parameters
        ----------
        start_row, start_col : int
            row and column index of the matrix entry where the positioned ships would start
        end_row, end_col: int
            row and column index of the matrix entry where the positioned ships would end

        Returns
        -------
        True or False : bool
            a boolean value is returned, after checking whether a ships is already placed on the input coordinates
            and whether the indexes spill out of the grid. In either case, the returned value is False
            otherwise it is True
        """
        if (start_row != end_row) and (start_col != end_col):  # no ship in diagonal
            return False
        if (start_row < 0) or (start_col < 0) or (end_row < 0) or (end_col < 0):  # negative indices
            return False
        if (start_row > 9) or (start_col > 9) or (end_row > 9) or (end_col > 9):  # negative indices
            return False
        location = []
        if start_row == end_row:
            if start_col < end_col:
                for i in range(start_col, end_col + 1):
                    location.append([start_row, i])
            if start_col > end_col:
                for i in range(end_col, start_col + 1):
                    location.append([start_row, i])
        if start_col == end_col:
            if start_row < end_row:
                 for i in range(start_row, end_row + 1):
                     location.append([i, start_col])
            if start_row > end_row:
                 for i in range(end_row, start_row + 1):
                     location.append([i, start_col])
        if (start_col == end_col) and (start_row == end_row):
                location.append([start_row, end_col])
        for i in location:
            for j in range(len(self.occupied_positions)):
                if i in self.occupied_positions[j]:
                    return False     # other ships in position
            for n in range(len(self.occupied_shadow)):
                if i in self.occupied_shadow[n]:
                    return False     # shadow of other ships in position
        return True

    def place_ship(self):
        """ This function is called once in the game during the insertion phase and consists in a loop in which
        at each iteration three pieces of information are drawn, all in a stochastic way: a starting index,
        one among the available ships and whether to place it vertically or not.
        The available starting indexes are previously filtered as those in which no other ships has been previously
        placed. The board indexes are updates every time a ship is placed and filled with 1, together with all the
        remaining attributes of the instantiation of Random that constitute the storage basis for the remaining part
        of the game.
        """
        while len(self.available_ships) > 0:
            start_idx = [rd.randint(0, GRID_SIZE - 1), rd.randint(0, GRID_SIZE - 1)]
            vertical = bool(rd.getrandbits(1))
            size = rd.choice(self.available_ships_sizes)
            start_row, start_col, end_row, end_col = self.get_indexes(start_idx, size, vertical)
            start_idx = [start_row, start_col]
            end_idx = [end_row, end_col]
            if self.validate_ship_position(start_row, end_row, start_col, end_col):
                ship = Ship_(start_idx, end_idx)
                try:
                    self.available_ships.remove(ship.name)
                    self.available_ships_sizes.remove(ship.size)
                    self.occupied_positions.append(ship.list_coordinates)
                    self.occupied_shadow.append(ship.shadow)
                    self.placed_ships.append([ship.name, ship.list_coordinates, ship.life])  # storing
                    for idx in ship.list_coordinates:
                        self.own_board[idx[0], idx[1]] = 1
                except Exception as e:
                    print(e)
                    continue
            else:
                continue
        print('Your opponent has placed everything')   # !!!!
        print('This is his board')   # !!!!!
        visualize_grid(self.own_board)   # !!!!!!

    def get_indexes(self, start_idx, size, vertical = False):
        """ The function returns the coordinates necessary to position a ship once given the starting index
        and the size. It returns start_row, end_row, start_col, end_col given a starting index and a size.
        Everything still has to be validated to check whether it is actually possible to place a ship of a
        given size starting from start_idx.

        Parameters
        ----------
        start_idx: list
            a list with row and column index of the starting entry of the matrix on which the Random wants to place a ship
        size: int
            a given size among the available ships yet to be placed
        vertical: bool
            boolean variable to characterize whether the to-be-placed ship is vertical or not. In both cases, the direction
            to be followed from the starting index is randomized, so that depending on the cases start_idx can actually become
            the ending index as well

        Returns
        -------
        start_row, start_col, end_row, end_col: int
            the generated positions necessary to place a ship of a given size following a certain direction either vertically
            (if vertical) or horizontally (if not vertical)
        """
        start_row = start_idx[0]
        start_col = start_idx[1]
        direction = rd.choice((-1, +1))
        if vertical:
            if direction == 1:
                end_row = start_row + (direction * size) - 1
            if direction == -1:
                end_row = start_row + (direction * size) + 1
            end_col = start_col
            return start_row, start_col, end_row, end_col
        end_row = start_row
        if direction == 1:
            end_col = start_col + direction * size - 1
        if direction == -1:
            end_col = start_col + direction * size + 1
        return start_row, start_col, end_row, end_col

    def shoot(self, board):
        """ This function defined the same behaviour for the class Random as the one for Player, by redefining
        the stochastic basis of the choice regarding where to shoot every round. This method takes as input
        the opponent's board (the one of Player) and by filtering the positions that have not already been shot at
        (independently of whether they were winning ones or not) chooses a completely random index as the next target.
        This function is called inside the main loop only under certain circumstances, that is when the Random player
        is not targeting any specific set of squares but needs to perform randomized search to explore the opponent's
        board.

        Parameters
        ----------
        board: array
            the opponent's board, which is unexplored except for the known positions where we previously shoot

        Returns
        -------
        shot: list
            list containing the row and column indexes of the stochastic shot made by Random
        """
        valid_idx1 = set(list(zip(np.where((board != -1))[0], np.where((board != -1))[1])))
        valid_idx2 = set(list(zip(np.where((board != 2))[0], np.where((board != 2))[1])))
        valids = list(valid_idx1.intersection(valid_idx2))  # random player does not shoot where he already did
        for i, shot in enumerate(valids):  # type casting
            if type(shot) == list:
                continue
            else:
                valids[i] = list(valids[i])
        sequential_col = []
        for i in range(10):
            winning_c = np.array(np.where(board[i] == -1)).tolist()  # indices of columns, we take consecutive ones
            winning_col = [x for sublist in winning_c for x in sublist]
            col_in_row = set()
            for idx in range(len(winning_col) - 1):
                if winning_col[idx] + 1 == winning_col[idx + 1]:
                    col_in_row.update([winning_col[idx], winning_col[idx + 1]])
                else:
                    if len(col_in_row) != 0:
                        sequential_col.append([[i, x] for x in sorted(col_in_row)])
                    col_in_row = set()
                    continue
                if (idx == len(winning_col) - 2) and len(col_in_row) > 0:
                    sequential_col.append([[i, x] for x in sorted(col_in_row)])
        sequential_row = []
        for i in range(10):
            winning_r = np.array(np.where(board[:, i] == -1)).tolist()  # indices of columns, we take consecutive ones
            winning_row = [x for sublist in winning_r for x in sublist]
            row_in_col = set()
            for idx in range(len(winning_row) - 1):
                if winning_row[idx] + 1 == winning_row[idx + 1]:
                    row_in_col.update([winning_row[idx], winning_row[idx + 1]])
                else:
                    if len(row_in_col) != 0:
                        sequential_row.append([[x, i] for x in sorted(row_in_col)])
                    row_in_col = set()
                    continue
                if (idx == len(winning_row) - 2) and len(row_in_col) > 0:
                    sequential_row.append([[x, i] for x in sorted(row_in_col)])
        invalid = []
        for i in sequential_col:
            row = i[0][0]
            max_col, min_col = i[-1][1], i[0][1]
            if row - 1 >= 0:
                invalid += [[row - 1, x] for x in range(min_col, max_col + 1)]
            if row + 1 <= 9:
                invalid += [[row + 1, x] for x in range(min_col, max_col + 1)]
        for i in sequential_row:
            col = i[0][1]
            max_row, min_row = i[-1][0], i[0][0]
            if col - 1 >= 0:
                invalid += [[x, col - 1] for x in range(min_row, max_row + 1)]
            if col + 1 <= 9:
                invalid += [[x, col + 1] for x in range(min_row, max_row + 1)]
        for index in invalid:
            for idx in valids:
                if index == idx:
                    valids.remove(idx)
        shot = rd.choice(valids)
        return shot, invalid

# VISUALIZE   !!!!!
def visualize_grid(grid, camu=False):
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
    grid_visual = [list(grid[i]) for i in range(GRID_SIZE)]

    for row in range(GRID_SIZE + 1):
        print(row_indexes[row], end="\t")
        for col in range(GRID_SIZE):
            if row == 0:
                print(alphabet[col], end=" ")
                continue
            if not camu:
                if grid_visual[row - 1][col] == 1:
                    print("O", end=" ")
                if grid_visual[row - 1][col] == -1:
                    print("X", end=" ")
                if grid_visual[row - 1][col] == 2:  # we store the shots in the water
                    print("#", end=" ")
                if grid_visual[row - 1][col] == 0:
                    print(".", end=" ")
            if camu:
                if grid_visual[row - 1][col] == 1:
                    print(" ", end=" ")
                if grid_visual[row - 1][col] == -1:
                    print("X", end=" ")
                if grid_visual[row - 1][col] == 2:  # we store the shots in the water
                    print("#", end=" ")
                if grid_visual[row - 1][col] == 0:
                    print(" ", end=" ")
        print("")
