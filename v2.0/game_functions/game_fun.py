
from plyr.player import Player as Player
from plyr.player import Player_ as Player_
from board_functions.board_funs import *
import random as rd

dictionary={b"A":b"1", b"B":b"2", b"C":b"3", b"D":b"4", b"E":b"5", b"F":b"6", b"G":b"7", b"H":b"8", b"I":b"9", b"J":b"10"}
keys=[k for k in dictionary.keys()]
values=[v for v in dictionary.values()]
block_size=40
grid_size=10

def player_placement(x_start, y_start, x_end, y_end, player):
   
    """
     The method is functional for the graphical insertion of the ships on the Player board.
    It checks the relative position of the 2 clicks of the mouse (down and up) inside the
    Pygame screen, it converts them and returns the features of the Ship together with
    the information of whether the Ship is actually feasible there

    Parameters
    ----------
    x_start, y_start: int
        the x and y position of the MOUSEBUTTONDOWN pygame even
    x_end, y_end: int
        the x and y position of the MOUSEBUTTONUP pygame even
    player: object
        the instantiation of the Graphical player (i.e. the user)

    Returns
    -------
    trip: list
        list comprising the indexes of initial and starting index of the to-be-placed ship
    vertical: bool
        storing the information of whether the ship is vertical or not
    length: int
        storing the length of the Ship
    False: bool
        returned in case the physical placement of the ship during the main loop is not
        conformant to what it should be
    """
    if x_start > block_size * 3 and x_start < block_size * 13 and y_start > block_size * 3 and y_start < block_size * 13:
        if x_end > block_size * 3 and x_end < block_size * 13 and y_end > block_size * 3 and y_end < block_size * 13:
            coord_start = player.own_board.get_coord(x_start, y_start)
            coord_end = player.own_board.get_coord(x_end, y_end)
            if not (coord_start[0] == coord_end[0] or coord_start[1] == coord_end[1]):
                return False
            trip = [coord_start, coord_end]
            if (trip[0][0] == trip[1][0] and trip[0][1] > trip[1][1]) \
                or (trip[0][1] == trip[1][1] and axes.index(trip[0][0]) > axes.index(trip[1][0])):              
                trip[0], trip[1] = trip[1], trip[0]
            length = abs(trip[0][1] - trip[1][1]) + 1 if (trip[0][0] == trip[1][0]) else abs(axes.index(trip[0][0]) - axes.index(trip[1][0])) + 1           
            if length > 5:        
                return False               
            vertical = True if trip[0][0] == trip[1][0] else False
            return trip, vertical, length
        else:
            return False
    else:
        return False
def player_shoot(x_start, y_start, x_end, y_end, player):
    """
     The method is similar to player_placement(x_start, y_start, x_end, y_end, player)
    but used during the shoot-shot phase, so that the conditions according to which
    the mouse click is appropriate change
    changes

    Parameters
    ----------
    x_start, y_start: int
        the x and y position of the MOUSEBUTTONDOWN pygame even
    x_end, y_end: int
        the x and y position of the MOUSEBUTTONUP pygame even.
        In this case, it must match the above one
    player: object
        the instantiation of the Graphical player (i.e. the user)

    Returns
    -------
    coord_start: list
        list comprising the indexes of initial and starting index of the to-be-placed shot (in B5 format)
    idxes: bool
        list comprising the indexes of initial and starting index of the to-be-placed shot (in indexes format)
    False: bool
        returned in case the physical placement of the shot during the main loop is not
        conformant to what it should be
    """
    if x_start > block_size * 16 and x_start < block_size * 26 \
        and y_start > block_size * 3 and y_start < block_size * 13:
        if x_end > block_size * 16 and x_end < block_size * 26 \
            and y_end > block_size * 3 and y_end < block_size * 13:
            coord_start = player.own_board.get_coord(x_start, y_start)
            coord_end = player.own_board.get_coord(x_end, y_end)
            if not (coord_start == coord_end):
                return False
            idxes = get_num_coord_opp(coord_start)
            return coord_start, idxes
        else:
            return False
    else:
        return False



def shoot_bullet(idx, board):
    """ The function checks whether a valid shot hits any ship (or any wave) on a grid, and it updates it.
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

def update_hit_ship(idx, opponent: object):

    """ 
    
    This function is called whenever a Ship has been hit, and it updates the remaining lives of the hit ship.
    After updating, it removes a Ship from the available ones whenever the ship has been hit fully.
    This function represents in fact the main mechanism of the game, since the game loop ends only when the
    number of ships sunk of one player (updated when this method is called) is equal to the total number of ships
    available (which is 10).

    Parameters
    ----------
    idx: list
        a 2-member list representing the row and the column index of the square where the winning shot has been placed
    opponent: object
        the opponent, in this version represented by the class Random

    Returns
    -------
    The function updates the attributes the opponent responsible for storing the information regarding
    the placed ships and their remaining lives. Whenever the ship after the update has 0 remaining lives,
    the number of ships sunk of the Player is increased (and this variable is responsible for ending the game)
    
    """
    idx = list(idx)
    try:
        if type(opponent) == Player_:
            for i in range(10):
                if idx in opponent.occupied_positions[i]:
                    opponent.placed_ships[i][-1] -= 1  
                    if opponent.placed_ships[i][-1] == 0:
                        opponent.number_ships_sunk += 1
                    break
        if type(opponent) == Player:
            for i in range(10):
                if idx in opponent.own_board.placed_ships[i][1]:
                    opponent.own_board.placed_ships[i][-1] -= 1 
                    if opponent.own_board.placed_ships[i][-1] == 0:
                        opponent.number_ships_sunk += 1 
                    break
    except Exception as e:
        print(e)
