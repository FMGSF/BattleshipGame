from ships.ships import *
from players.players import *

import random as rd
import numpy as np
import time

grid_size = 10
grid = np.zeros((grid_size, grid_size), dtype=int)
# grid_opp = np.zeros((grid_size, grid_size), dtype=int)
alphabet = "ABCDEFGHIJ"
dictionary = {i: int(alphabet.index(i)) for i in alphabet}

rd.seed(time.time())  # tell python we want randomness based on timing program, if run multiple times in rows

opp_winning_shots = []
possible_directions = ['up', 'down', 'left', 'right']
found_ship = False
local_search = 0

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
    for i in range(len(opponent.occupied_positions)):
        if idx in opponent.occupied_positions[i]:
            hit_ship = i
    opponent.placed_ships[hit_ship][-1] -= 1  # the hit ship loses one life
    if opponent.placed_ships[hit_ship][-1] == 0:
        opponent.number_ships_sunk += 1

def main():
    global found_ship
    global local_search
    global opp_winning_shots
    player1 = Player(grid)
    player2 = Random(grid_opp)
    player1.opponent = player2
    player2.opponent = player1
    print("!!!      WELCOME TO BATTLESHIP      !!!\n")
    time.sleep(2)
    player2.place_ship()
    visualize_grid(player2.board, camu=False)
    print('\n!!!    TIME TO PLACE YOUR SHIPS    !!!\n')
    time.sleep(2)
    player1.place_ship()
    game = True
    while game:
        while (player1.number_ships_sunk < 10) & (player2.number_ships_sunk < 10):
            print("")
            visualize_grid(player2.board, camu=True)
            shot = player1.shoot()
            while not accept_shot_placement(shot, player2.board):
                shot = player1.shoot()
            print("")
            time.sleep(2)
            print('Your cannons are shooting\n')
            time.sleep(2)
            if shoot_bullet(shot, player2.board):
                print('YES, you hit one!!!')
                update_hit_ship(shot, player2)
            else:
                print('NOPE, you hit only some random waves !!!')
            time.sleep(2)
            visualize_grid(player2.board, camu=True)
            time.sleep(2)
            print('\n!!!    THE ENEMIES ARE SHOOTING    !!!')
            time.sleep(2)

            if found_ship == True:
                try:
                    last_two_shots = [opp_winning_shots[-2], opp_winning_shots[-1]]
                    if find_new_shot(last_two_shots):
                        opp_shot = find_new_shot(last_two_shots)   # we find new shot on basis of last two (we keep direction)
                        if not accept_shot_placement(opp_shot, player1.board, camu=True):
                            opp_shot = player2.shoot(player1.board)   # shoot random if the implied index has already been shot
                    else:
                        opp_shot = player2.shoot(player1.board)    # shoot random se esce fuori dalla grid seguendo gli ultimi due
                except:
                    if local_search > 0:
                        last_winning = opp_winning_shots[-1]
                        direction = rd.choice(possible_directions)
                        opp_shot = find_new_shot_direction(last_winning, direction)
                        if not accept_shot_placement(opp_shot, player1.board, camu=True):
                            opp_shot = player2.shoot(player1.board)   # shoot random if the index given by localized random search is not valid
                            # but still next round he will shoot close to that, until all 4 directions are done
                        possible_directions.remove(direction)
                        local_search -= 1
                    else:
                        opp_shot = player2.shoot(player1.board)

            if found_ship == False:  # two cases either we are trying all directions around a previously found ship or not
                if local_search > 0:
                    last_winning = opp_winning_shots[-1]
                    direction = rd.choice(possible_directions)
                    opp_shot = find_new_shot_direction(last_winning, direction)
                    if not accept_shot_placement(opp_shot, player1.board, camu=True):
                        opp_shot = player2.shoot(player1.board)   # shoot random if the index given by localized random search is not valid
                        # but still next round he will shoot close to that, until all 4 directions are done
                    possible_directions.remove(direction)
                    local_search -= 1
                else:
                    opp_shot = player2.shoot(player1.board)

            if shoot_bullet(opp_shot, player1.board):
                print(f'\nOUCH, the enemies have hit in {alphabet[opp_shot[1]]}, {opp_shot[0]+1}!')
                time.sleep(2)
                update_hit_ship(opp_shot, player1)
                found_ship = True
                opp_winning_shots.append(opp_shot)
                local_search = 4
                possible_directions = ['up', 'down', 'left', 'right']
            else:
                print(f'\nFIUU, the enemies have missed in {alphabet[opp_shot[1]]}, {opp_shot[0]+1}!')
                time.sleep(2)
                found_ship = False
            visualize_grid(player1.board, camu=False)
            time.sleep(2)

        if player1.number_ships_sunk == 10:
            time.sleep(2)
            print('\n!!!      GAME OVER      !!!\n')
            time.sleep(1)
            print('       YOUR ARMY HAS BEEN DEFEATED       ')
        if player2.number_ships_sunk == 10:
            time.sleep(2)
            print('\n!!!      YOU WON      !!!\n')
            time.sleep(1)
            print('       YOU SAVE THE PLANET, my Honour       \n')
        another = input("\n Do you want to play another game (y/n)? ")
        while another not in ['y', 'n', 'yes', 'no', 'Yes', 'No']:
            time.sleep(1)
            print('Not a valid input, your troops are waiting')
            time.sleep(1)
            another = input("\n Do you want to play another game (y/n)? ")
        if another in ['y', 'yes', 'Yes']:
            continue
        if another in ['n', 'no', 'No']:
            game = False

if __name__=="__main__":
    main()
