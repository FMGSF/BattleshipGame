import random as rd
import numpy as np
import re
from ships.ships import *
import time

alphabet = "ABCDEFGHIJ"
dictionary = {i: int(alphabet.index(i)) for i in alphabet}

def decode_input(x):
    """ After receiving as input the index given by the Player to either shoot or place a ship,
    this function returns the index of grid if the input is correct, otherwise returns False.

    Parameters
    ----------
    x: str
        x is of the form 'A1' and it is the input received by the Player

    Returns
    -------
    row_index, col_index: int
        the references to the shot interpreted as indices of the numpy matrix board,
        after filtering x with a regular expression and converting it into indices by using the global variable dictionary
    False: bool
        returned in case of no valid input
    """
    global dictionary
    first = re.compile(r'[\d]+')
    second = re.compile(r'[A-Z]')
    try:
        row_label = first.search(x).group()
        row_index = int(row_label) - 1
        col_label = second.search(x).group()
        col_index = int(dictionary.get(col_label))
        return row_index, col_index
    except:
        return False

def accept_shot_placement(idx, board, camu = False):
    """ This function checks both whether the provided idx is in fact a feasible index of the board
    and whether a shot was not already placed in the same spot. If either case happens,
    the input is returned as being invalid (False) otherwise True is returned.

    Parameters
    ----------
    idx: list
        a list with two entries (the entry of the numpy array to be checked)
    board: array
        represents in the main loop the board of the opponent where to check the disposition
        of the previous shots
    camu: bool
        variable for visualization, depends on whether the function is called for the Player or for the Random

    Returns
    -------
    True, False: bool
        the output of the function represents the potential validation of the shot about to be made
    """
    if (idx[0] < 0) or (idx[1] < 0):
        if camu == False:
            print('The index is out of bounds')
        return False
    elif (idx[0] > 9) or (idx[1] > 9):
        if camu == False:
            print('The index is out of bounds')
        return False
    elif board[idx[0], idx[1]] == 2 or board[idx[0], idx[1]] == -1:
        if camu == False:
            print('You already made a shot here, try another place')
        return False
    else:
        return True

def shoot_bullet(idx, board):
    """ The function checks whether a valid shot hits any ship (or any wave) on the opponent's grid.
    It returns a boolean, either True in the former case or False in the latter.

    Parameters
    ----------
    idx: list
        a list with two entries (the entry of the numpy array)
    board: array
        the opponent's board on which to check the result of the shot just made

    Returns
    -------
    True, False: bool
        the first in case an opponent's shit has been hit, otherwise False
    """
    if board[idx[0], idx[1]] == 1:
        board[idx[0], idx[1]] = -1
        return True

    if board[idx[0], idx[1]] == 0:
        board[idx[0], idx[1]] = 2
        return False

# -----------------------------------------------------------------------------------#
# the following functions are made for the class Random

def get_indexes(start_idx, size, vertical=False):
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

def find_new_shot(x):
    """ The function allows the Random Player to deduce the correct next shot on the basis
    of the last two he made. It takes into consideration the feasible dimensions of the board and
    the direction that was being followed in the last shots.

    Parameters
    ----------
    x: list
        a list with 2 coordinates, that is comprising of 4 indexes (the last two shots made).
        out of x, it is deduced both the direction to be followed and whether it is feasible to stick with it

    Returns
    -------
    opp_shot: list
        the next shot of the Random player is returned
    """
    one_to_last = x[0]
    last = x[1]
    if one_to_last[0] == last[0]:   # followed the same row
        row_idx = last[0]
        if one_to_last[1] > last[1]:   # it went left
            col_idx = last[1]-1
        if one_to_last[1] < last[1]:   # it went right
            col_idx = last[1] + 1
    if one_to_last[1] == last[1]:   # followed the same col
        col_idx = last[1]
        if one_to_last[0] > last[0]:  # it went down
            row_idx = last[0] - 1
        if one_to_last[0] < last[0]:  # it went up
            row_idx = last[0] + 1
    if (row_idx < 0) or (col_idx < 0):   # if out of the grid, shoots random next time
        return False
    if (row_idx > 9) or (col_idx > 9):
        return False
    opp_shot = [row_idx, col_idx]
    return opp_shot

def find_new_shot_direction(x, direction):
    """ The function returns the coordinates of the next shot, starting from the last shot and one of the
    four possible directions.

    Parameters
    ----------
    x: list
        the list storing the row and column coordinates of the last winning shot
    direction: str
        one of the four possible directions ('up', 'down', 'left', 'right'). This parameter needs
        to be given since the method is used in the main loop to explore around a winning shot
        along the four possible directions that can be followed by the ship

    Returns
    -------
    shot: list
        the row and column index on which to place the next shot of the Random player
    """
    if direction == 'up':
        col_idx = x[1]
        row_idx = x[0] - 1
    if direction == 'down':
        col_idx = x[1]
        row_idx = x[0] + 1
    if direction == 'left':
        row_idx = x[0]
        col_idx = x[1] - 1
    if direction == 'right':
        row_idx = x[0]
        col_idx = x[1] + 1
    shot = [row_idx, col_idx]
    return shot

# -------------------------------------------------------------------------------------------------#

class Player(object):
    """ The Player class is one of the two players of a classic battleship game on one own.
    It stores all the necessary identifier of the player which are constantly updated during the game, together
    with the main functions for placing and calling the shots to be alternated with the one of the subclass Random(Player).
    Each player is endowed with 10 ships of varying dimensions and a 10x10 board matrix.

    Parameters
    ----------
    board: array
        the board variable is a pointer to the personal numpy matrix 10x10 which stores the positions of the placed ships
        together with the ones of the placed shots
    id: str
        a string identifier, more important when the network will be added

    Attributes
    -------
    id: str
        a string identifier, more important when the network will be added
    board: array
        the board variable is a pointer to the personal numpy matrix 10x10 which stores the positions of the placed ships
        together with the ones of the placed shots
    available_ships: list
        the list storing the names of the ships yet to be placed, it is the basis of the positioning phase which ends only
        when this list is empty
    available_ships_sizes: list
        the list storing the sizes of the ships yet to be placed and strictly linked to the previous one.
        this list is used to check whether the placed ships are among the available ones on the basis of their dimensions
    occupied_positions: list
        a storing list used to progressively append the coordinates of the placed ships.
        it is mainly used to check whether the positioned ships overlaps with one previously placed
    placed_ships: list
        a list containing the names of all ships placed, together with their coordinates and their remaining lives.
        it is the main memory storage for the progressive execution of the game
    number_ships_sunk: int
        the variable responsible for ending the main loop of the game, whenever the number of ships sunk of a
        certain player is equivalent to the total number of ships available (10).
        it is based on the previous one, since number_ships_sunk increases by 1 every time the remaining lives of
        one of the ships stored in placed_ships go to 0.
    """
    def __init__(self, board, id = 'player1'):  # opponent is a Player
        self.id = id
        self.number_ships = 10
        self.board = board
        self.available_ships = ["AircraftCarrier", "Battleship", "Destroyer", "Destroyer", "Submarine",
                                "Submarine", "Submarine", "PatrolBoat", "PatrolBoat", "PatrolBoat"]
        self.available_ships_sizes = [AircraftCarrier().size, Battleship().size, Destroyer().size, Destroyer().size,
                                      Submarine().size, Submarine().size, Submarine().size,
                                      PatrolBoat().size, PatrolBoat().size, PatrolBoat().size]
        self.occupied_positions = []
        self.occupied_shadow = []
        self.placed_ships = []
        self.number_ships_sunk = 0

    def update_show_info(self):
        """ A function used to inform the player about the names, the sizes and the quantities of the remaining ships.
        It does so by updating every time the information stored inside a dictionary, and printing the keys and values
        and every step of the ships' insertion.
        Since it is a function for the display, it does not take any parameter

            Returns
            -------
            The function prints all the information necessary for the placements of the ships, at every step of the
            insertion phase
            """
        self.ships_quantities = {x: self.available_ships.count(x) for x in self.available_ships}
        self.player_info = {(self.available_ships[i], self.available_ships_sizes[i]):
                                self.ships_quantities.get(self.available_ships[i]) for i in range(len(self.available_ships_sizes))}
        for k, v in self.player_info:
            print(f"{k}, with size {v}: {self.player_info[(k, v)]} available")

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
        if (start_row != end_row) & (start_col != end_col):  # no ship in diagonal
            return False
        if (start_row < 0) or (start_col < 0) or (end_row < 0) or (end_col < 0):
            return False
        if (start_row > 9) or (start_col > 9) or (end_row > 9) or (end_col > 9):
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
        at each iteration the starting and ending index of the to-be-placed ship are asked using an input on the
        terminal. The loop ends only when all the 10 ships available to the player are correctly placed on the board.
        The function takes no input as it is conceived as representing an entire phase of the game to be called inside
        the main loop.

        Returns
        -------
        The main loop of the function ends when all the available ships have been placed by the player which the method is
        called onto, so that the phase of the actual shoot-get_shot can start. Along the way, all the attributes of the
        instantiation of Player (f.i., self.board and self.placed_ships) are updated to constitute the storage basis for the
        remaining phase of the game.
        """
        while len(self.available_ships) > 0:
            print('\nYou have remaining troops, dispose of them: \n')
            self.update_show_info()
            #print(self.player_info)
            visualize_grid(self.board)
            start = str(input('Insert the starting index (ex. A1): '))
            if not decode_input(start):
                time.sleep(1)
                print('Wrong input, follow the rules')
                time.sleep(1)
                continue
            start_row, start_col = decode_input(start)
            start_idx = [start_row, start_col]
            end = str(input('Insert the end index (ex. A5): '))
            if decode_input(end) == False:
                time.sleep(1)
                print('Wrong input, follow the rules')
                time.sleep(1)
                continue
            end_row, end_col = decode_input(end)
            end_idx = [end_row, end_col]
            if self.validate_ship_position(start_idx[0], end_idx[0], start_idx[1], end_idx[1]):
                ship = Ship(start_idx, end_idx)
                try:
                    self.available_ships.remove(ship.name)
                    self.available_ships_sizes.remove(ship.size)
                    self.occupied_positions.append(ship.list_coordinates)
                    self.placed_ships.append([ship.name, ship.list_coordinates, ship.life])  # storing
                    for idx in ship.list_coordinates:
                        self.board[idx[0], idx[1]] = 1
                    time.sleep(1)
                    print('\nHere goes your ship')
                    time.sleep(1)
                    visualize_grid(self.board)
                except ValueError:
                    time.sleep(1)
                    print('\nSorry, the dimensions do not correspond to an available ship\n')
                    time.sleep(1)
                    continue
            else:
                time.sleep(1)
                print('\nSorry, either a ship is already placed here or the input is not valid \n')
                time.sleep(1)
                continue
        time.sleep(2)
        print('\nGREAT JOB!!! NOW THE WAR BEGINS')
        time.sleep(1)

    def shoot(self):
        """ This function is called onto the non-randomized player at each round of the shoot-get_shot game phase.
        It calls the method decode_input in order to convert the input string representing the square to be shot
        into a index-referencing list to be applied on the opponent's board. Whenever this is not possible, the
        request is repeated until a valid input is provided.

        Returns
        -------
        shot: list
            list containing the row and column indexes of the shot made by Player, which is then called inside the
            main loop onto the opponent's board to update the potentially hit ship together with their remaining lives.
        """
        index = str(input('\nInsert where you want to shoot (ex. A1): '))
        while not decode_input(index):
            index = str(input('\nThat is not a valid index, try again (ex. A1): '))
        row_index, col_index = decode_input(index)
        shot = [row_index, col_index]
        return shot

class Random(Player):
    """ The Random class represents the randomized player that constitutes a valid opponent of the user (Player)
    one of the two players of a classic battleship game on one own. In fact, the class Random inherits from Player
    all the behaviours, while redefining through Polymorphism the game behaviours of placing the ships and shooting,
    which clearly are now independent from any terminal input.

    Parameters
    ----------
    board: array
        the board variable is a pointer to the personal numpy matrix 10x10 which stores the positions of the placed ships
        together with the ones of the placed shots. It represents a counterpart, i.e. the opponent board for the user
    id: str
        a string identifier, by default 'random'

    Attributes
    -------
    id: str
        a string identifier, by default 'random'
    board: array
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
    def __init__(self, board, id = 'random'):
        self.id = id
        self.board = board

        self.available_ships = ["AircraftCarrier", "Battleship", "Destroyer", "Destroyer", "Submarine",
                                "Submarine", "Submarine", "PatrolBoat", "PatrolBoat", "PatrolBoat"]
        # self.ships_quantities = {x: self.available_ships.count(x) for x in self.available_ships}
        self.available_ships_sizes = [AircraftCarrier().size, Battleship().size, Destroyer().size, Destroyer().size,
                                      Submarine().size, Submarine().size, Submarine().size,
                                      PatrolBoat().size, PatrolBoat().size, PatrolBoat().size]
        self.occupied_positions = []
        self.occupied_shadow = []
        self.placed_ships = []
        self.number_ships_sunk = 0

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
            start_idx = [rd.randint(0, grid_size - 1), rd.randint(0, grid_size - 1)]
            vertical = bool(rd.getrandbits(1))
            size = rd.choice(self.available_ships_sizes)
            start_row, start_col, end_row, end_col = get_indexes(start_idx, size, vertical)
            start_idx = [start_row, start_col]
            end_idx = [end_row, end_col]
            if super().validate_ship_position(start_row, end_row, start_col, end_col):
                ship = Ship(start_idx, end_idx)
                try:
                    self.available_ships.remove(ship.name)  # qua sei sicuro che stia generando la barca giusta quindi non serve try
                    self.available_ships_sizes.remove(ship.size)
                    self.occupied_positions.append(ship.list_coordinates)
                    self.occupied_shadow.append(ship.shadow)
                    self.placed_ships.append([ship.name, ship.list_coordinates, ship.life])  # storing
                    for idx in ship.list_coordinates:
                        self.board[idx[0], idx[1]] = 1
                except:
                    continue
            else:
                continue
        print("All the troops of the enemy are placed, it's your turn")

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
        valids = list(valid_idx1.intersection(valid_idx2))
        shot = rd.choice(valids)
        return shot

