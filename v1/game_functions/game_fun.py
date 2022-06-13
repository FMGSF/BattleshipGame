
from plyr.player import Player as Player
from plyr.player import Random as Random
from board_functions.board_funs import *
import random as rd

dictionary={b"A":b"1", b"B":b"2", b"C":b"3", b"D":b"4", b"E":b"5", b"F":b"6", b"G":b"7", b"H":b"8", b"I":b"9", b"J":b"10"}
keys=[k for k in dictionary.keys()]
values=[v for v in dictionary.values()]
block_size=40


def accept_shot_placement(idx, board, invalid, camu = False):
    """
    This function checks both whether the provided idx is in fact a feasible index of the board
    and whether a shot was not already placed in the same spot. If either case happens,
    the input is returned as being invalid (False) otherwise True is returned.

    Parameters
    ----------
    idx: list
        a list with two entries (the entry of the numpy array to be checked)
    board: array
        represents in the main loop the board of the opponent where to check the disposition
        of the previous shots
    invalid: list
        list comprising all the indexes of the matrix that are parallel to a series of winning shots
        made on the same row/column, i.e. this variable and the way it is constructed is a proxy of
        the reasoning made by a human player not to hit a square near a sunk ship (since that would be
        a wasted shot, for the rule that no ship can be placed on a adjacent square with respect to an
        already placed ship)
    camu: bool
        variable for visualization, depends on whether the function is called for the Player or for the Random

    Returns
    -------
    True, False: bool
        the output of the function represents the potential validation of the shot about to be made
    """
    idx = list(idx)  # type casting
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
    for index in invalid:
        if idx == index:
            if camu == False:
                print('Invalid shot, near what should be a boat')
            return False
    return True

def player_placement(x_start, y_start, x_end, y_end, player):
    """ The method is functional for the graphical insertion of the ships on the Player board.
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
            if (trip[0][0] == trip[1][0] and trip[0][1] > trip[1][1]) or (trip[0][1] == trip[1][1] and axes.index(trip[0][0]) > axes.index(trip[1][0])):
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
    """ The method is similar to player_placement(x_start, y_start, x_end, y_end, player)
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
    if x_start > block_size * 16 and x_start < block_size * 26 and y_start > block_size * 3 and y_start < block_size * 13:
        if x_end > block_size * 16 and x_end < block_size * 26 and y_end > block_size * 3 and y_end < block_size * 13:
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

def find_new_shot(one_to_last, winning_shots):
    """ The function allows the Random Player to deduce the correct next shot on the basis
    of the last two he made. It takes into consideration the feasible dimensions of the board and
    the direction that was being followed in the last shots.

    Parameters
    ----------
    one_to_last: list
        list of indexes (grid coordinates) obtained after calling the method check_near_winning.
        It is one of the winning shots (throughout the entire) that is on the
        same row/column and not further than one index from the last winning shot
    winning_shots: list
        a list comprising all the indexes of the winning shots made by the Random player throughout
        the duration of the game. In case the last two shots have been consecutive ones, this variable allows
        to follow the same direction.

    Returns
    -------
    opp_shot: list
        the next shot of the Random player is returned.
        Otherwise, the boolean value False is returned in case the player is dealing with a randomized local
        search, i.e. it still needs to find a winning direction to be followed out of an isolated winning shot.
    followed: str
        one of four possible string values (up, down, left, right) that stands for the direction followed
        this round. this variable is necessary to make the decision next round to follow the opposite direction
    """
    one_to_last, last = list(one_to_last), list(winning_shots[-1])   # type casting
    for i, shot in enumerate(winning_shots):
        if type(shot) == list:
            continue
        else:
            winning_shots[i] = list(winning_shots[i])
    if one_to_last[0] == last[0]:   # followed the same row
        row_idx = last[0]
        if one_to_last[1] > last[1]:   # went left
            col_idx = last[1] - 1 if (last[1] - 1 >= 0) else last[1]
            followed = 'left'
            if col_idx == last[1]:    # can go out of the grid -> follows the same row in the other direction
                while [row_idx, col_idx] in winning_shots:
                    col_idx += 1
                    followed = None
        if one_to_last[1] < last[1]:   # went right
            col_idx = last[1] + 1 if (last[1] + 1 <= 9) else last[1]
            followed = 'right'
            if col_idx == last[1]:    # can go out of the grid -> follows the same row in the other direction
                while [row_idx, col_idx] in winning_shots:
                    col_idx -= 1
                    followed = None
    if one_to_last[1] == last[1]:   # followed the same col
        col_idx = last[1]
        if one_to_last[0] > last[0]:  # went up
            row_idx = last[0] - 1 if (last[0] - 1 >= 0) else last[0]
            followed = 'up'
            if row_idx == last[0]:    # can go out of the grid -> follows the same col in the other direction
                while [row_idx, col_idx] in winning_shots:
                    row_idx += 1
                    followed = None
        if one_to_last[0] < last[0]:  # went down
            row_idx = last[0] + 1 if (last[0] + 1 <= 9) else last[0]
            followed = 'down'
            if row_idx == last[0]:   # can go out of the grid -> follows the same col in the other direction
                while [row_idx, col_idx] in winning_shots:
                    row_idx -= 1
                    followed = None
    opp_shot = [row_idx, col_idx]
    return opp_shot, followed

def check_other_direction(previous_direction, winning_shots, player, invalid):   # player is opponent
    """ This function is called inside the main loop during the shooting phase of the Random player, in case
    a direction was being followed, having found some winning shots on the same row/column, and the previous shot
    was not a winning one (found_ship = False). It allows to follow the opposite direction, to explore where the
    partially hit ship could be placed.

    Parameters
    ----------
    previous_direction: str
        one of four possible string values (up, down, left, right) stored in the previous round of the shooting phase.
        It allows to explore the opposite direction, since following previous_direction has led to a non-winning
        shot in the previous round
    winning_shots: list
        a list comprising all the indexes of the winning shots made by the Random player throughout
        the duration of the game, necessary to draw conclusion on any pattern found at different rounds
        of the game
    player: object
        instantiation of the opponent, i.e. the Player for the Random.
    invalid: list
        list comprising all the indexes of the matrix that are parallel to a series of winning shots
        made on the same row/column, i.e. this variable and the way it is constructed is a proxy of
        the reasoning made by a human player not to hit a square near a sunk ship (since that would be
        a wasted shot, for the rule that no ship can be placed on a adjacent square with respect to an
        already placed ship)

    Returns
    -------
    opp_shot: list
        the next shot of the Random player is returned.
        Otherwise, the boolean value False is returned in case the direction opposite to previous_direction is
        not feasible (either for grid dimensions or for an already shot position).
    """
    try:
        last = list(winning_shots[-1])  # type casting
        row_idx, col_idx = last[0], last[1]
        for i, shot in enumerate(winning_shots):
            if type(shot) == list:
                continue
            else:
                winning_shots[i] = list(winning_shots[i])
        if previous_direction == "up":   # it always goes in the opposite direction to the one followed previously
            while [row_idx ,col_idx] in winning_shots:
                row_idx += 1
        if previous_direction == "down":
            while [row_idx ,col_idx] in winning_shots:
                row_idx -= 1
        if previous_direction == "left":
            while [row_idx ,col_idx] in winning_shots:
                col_idx += 1
        if previous_direction == "right":
            while [row_idx ,col_idx] in winning_shots:
                col_idx -= 1
        opp_shot = [row_idx, col_idx]
        if not accept_shot_placement(opp_shot, player.own_board.occupied_cells, invalid, camu = True):
            return None
        return opp_shot
    except:
        return None

def check_near_winning(opp_winning_shots):
    """ The function is functional for the mechanisms of the random engine in predicting the next
        shot to be done. It gathers those winning shots made throughout the game that are on the
        same row/column and not further than one index from the last winning shot

        Parameters
        ----------
        opp_winning_shots: list
            a list comprising all the indexes of the winning shots made by the Random player throughout
            the duration of the game. In case the last two shots have been consecutive ones, this variable allows
            to follow the same direction.

        Returns
        -------
        near: list
            the list gathers those winning shots made throughout the game that are on the
            same row/column and not further than one index from the last winning shot
        """
    near = []
    last = opp_winning_shots[-1]
    for idx in opp_winning_shots[:-1]:
        if (last[0] == idx[0]) and -1 <= last[1] - idx[1] <= 1:
            near.append(idx)
        if (last[1] == idx[1]) and -1 <= last[0] - idx[0] <= 1:
            near.append(idx)
    if len(near) == 0:
        return None
    else:
        return near

def localized_search(last_winning, local_search, possible_directions, player, invalid):
    """ The function is functional for the mechanisms of the random engine in predicting the next
        shot to be done. It targets each time one of the four possible directions around the
        last (isolated) winning shots. It also handles the validation for what regards proposing
        a shot that is indeed a feasible shot given the dimensions of the board.

        Parameters
        ----------
        last_winning: list
            a list comprising the indexes of the last winning shot
        local_search: int
            an integer value that is decreased each time the function is performed (given the same
            isolated winning shot). It goes from 4 to 1, and parallel the number of possible directions
            from that winning shot
        possible_directions: list
            a list comprising the four possible directions in which a Ship could be placed given
            a starting point, i.e. up down left and right
        player: class
            the instantiation of the Player class, i.e. the opponent for the Random player
        invalid: list
            list comprising all the indexes of the matrix that are parallel to a series of winning shots
            made on the same row/column, i.e. this variable and the way it is constructed is a proxy of
            the reasoning made by a human player not to hit a square near a sunk ship (since that would be
            a wasted shot, for the rule that no ship can be placed on a adjacent square with respect to an
            already placed ship)

        Returns
        -------
        shot: list
            the list comprising the indexes of the next predicted shot, given the aim of targetting
            an area around an isolated winning shot
        local_search: int
            the decreased amount of local search, which is also given as input, necessary to store it
        False: bool
            the value is returned as an alternative to the first two whenever the randomized local search
            has been exhausted

    """
    while local_search > 0:
        row_idx, col_idx = last_winning[0], last_winning[1]
        local_search -= 1
        direction = rd.choice(possible_directions)
        possible_directions.remove(direction)
        if direction == 'up':
            row_idx -= 1
        if direction == 'down':
            row_idx += 1
        if direction == 'left':
            col_idx -= 1
        if direction == 'right':
            col_idx += 1
        shot = [row_idx, col_idx]
        if accept_shot_placement(shot, player.own_board.occupied_cells, invalid, camu = True):
            return shot, local_search
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
    """ This function is called whenever a Ship has been hit, and it updates the remaining lives of the hit ship.
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
        if type(opponent) == Random:
            for i in range(10):
                if idx in opponent.occupied_positions[i]:
                    opponent.placed_ships[i][-1] -= 1  # the hit ship loses one life
                    if opponent.placed_ships[i][-1] == 0:
                        opponent.number_ships_sunk += 1
                    break
        if type(opponent) == Player:
            for i in range(10):
                if idx in opponent.own_board.placed_ships[i][1]:
                    opponent.own_board.placed_ships[i][-1] -= 1  # the hit ship loses one life
                    if opponent.own_board.placed_ships[i][-1] == 0:
                        opponent.number_ships_sunk += 1 
                    break
    except Exception as e:
        print(e)








