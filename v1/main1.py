import sys
from game_functions.game_fun import *
from plyr.player import *
from brd.board import *

pygame.init()
fps=120
grid_opp = np.zeros((10, 10), dtype=int)
dictionary={b"A":b"1", b"B":b"2", b"C":b"3", b"D":b"4", b"E":b"5", b"F":b"6", b"G":b"7", b"H":b"8", b"I":b"9", b"J":b"10"}
keys=[k for k in dictionary.keys()]
values=[v for v in dictionary.values()]
WHITE=(0, 0, 0)

opp_winning_shots = []
possible_directions = []
invalid = []
found_ship = False
local_search = 0
following = False
followed = None
opp_shot = None
x_start = float()
y_start = float()

pygame.display.init()  # let's initialize the pygame.display object
pygame.display.set_caption("battleship_game")  # description of the window

def main():
    global found_ship; global x_start; global y_start; global invalid
    global following; global opp_shot; global local_search
    global opp_winning_shots; global possible_directions; global followed
    player = Player(); player2 = Random()
    run = True
    round_played = False
    player2.place_ship()
    clock = pygame.time.Clock()

    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
               run = False

            # MENU
            if player.own_board.state == 0:
                player.own_board.draw_menu()

            if player.own_board.state == 1:
                coord = []
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x0 = pygame.mouse.get_pos()[0]
                    y0 = pygame.mouse.get_pos()[1]
                    coord.append([x0, y0])
                    if player.own_board.draw_menu_click(coord):
                        pygame.display.update()
                        player.own_board.draw_screen_game()

            # BOAT INSERTION
            elif len(player.boats.sprites()) > 0 and player.own_board.state == 2:
                if (event.type==pygame.MOUSEBUTTONDOWN):
                    pos_start = pygame.mouse.get_pos()
                    player.own_board.check_undo_click(pos_start, player)
                    x_start = pos_start[0]
                    y_start = pos_start[1]
                if (event.type==pygame.MOUSEBUTTONUP):
                    pos_end = pygame.mouse.get_pos()
                    x_end = pos_end[0]
                    y_end = pos_end[1]
                    if player_placement(x_start, y_start, x_end, y_end, player):
                        trip, vertical, length = player_placement(x_start, y_start, x_end, y_end, player)
                        for boat in player.boats:
                            if boat.size == length:
                                boat.vertical = vertical
                                boat.set_gridpos([str(trip[0][0], encoding='utf-8'), trip[0][1]])
                                player.own_board.insert_boat(boat)
                                break
                        for placed in player.own_board.located_boats:
                            for boat in player.boats:
                                if placed == boat:
                                    player.boats.remove(placed)
                                    break
                    else:
                        x_start, y_start = float(), float()

            # BOAT INSERTION OVER, THE GAME BEGINS
            # PLAYER 1
            elif player.own_board.state == 2:
                if (event.type==pygame.MOUSEBUTTONDOWN):
                    player.own_board.item.fill(pygame.Color("black"), (0, 13.1*block_size,screen_width,4*block_size))
                    pygame.display.flip()
                    pos_start = pygame.mouse.get_pos()
                    x_start = pos_start[0]
                    y_start = pos_start[1]
                if (event.type==pygame.MOUSEBUTTONUP):
                    pos_end = pygame.mouse.get_pos()
                    x_end = pos_end[0]
                    y_end = pos_end[1]
                    if player_shoot(x_start, y_start, x_end, y_end, player):
                        coord_start, idxes = player_shoot(x_start, y_start, x_end, y_end, player)
                        if coord_start not in player.own_board.hit_cells:
                            round_played = True
                            if shoot_bullet(idxes, player2.own_board):
                                player.own_board.mark_hit_cell(coord_start, True, found_ship)
                                update_hit_ship(idxes, player2)
                            else:                                              
                                player.own_board.mark_hit_cell(coord_start, False, found_ship)
            # RANDOM PLAYER
                if round_played == True:
                    if found_ship == True:
                        near_winning_shots = check_near_winning(opp_winning_shots)
                        if near_winning_shots is None:
                            try:  # one detached winning shot as last one
                                opp_shot, local_search = localized_search(opp_winning_shots[-1], local_search, possible_directions, player, invalid)
                            except:  #  shoots random if localized search has already been exhausted
                                opp_shot, invalid = player2.shoot(player.own_board.occupied_cells)
                        else:
                            for candidate in near_winning_shots:
                                opp_shot, followed = find_new_shot(candidate, opp_winning_shots)  # we keep direction of winning shots that are near
                                if not accept_shot_placement(opp_shot, player.own_board.occupied_cells, invalid, camu = True):
                                    continue
                                else:
                                    following = True
                                    break
                            if following == False:
                                opp_shot, invalid = player2.shoot(player.own_board.occupied_cells)  # shoots random if all the implied indexes are not valid
                    if found_ship == False:     #  not hitting a ship can be part of the localized random search
                        if following == True:   #  the Player explores the other direction (the opposite to the one found before)
                            opp_shot = check_other_direction(followed, opp_winning_shots, player, invalid)
                        if following == False and local_search > 0:
                            try:
                                opp_shot, local_search = localized_search(opp_winning_shots[-1], local_search, possible_directions, player, invalid)
                            except:  # shoots random if localized search has already been exhausted
                                opp_shot, invalid = player2.shoot(player.own_board.occupied_cells)
                        if opp_shot == None:
                            opp_shot, invalid = player2.shoot(player.own_board.occupied_cells)  # shoots random if neither one winning direction nor the opposite is feasible
                    round_played = False

                    if shoot_bullet(opp_shot, player.own_board.occupied_cells):
                        update_hit_ship(opp_shot, player)
                        if found_ship == False:
                            local_search = 4
                        opp_winning_shots.append(opp_shot)
                        found_ship = True
                        following = False
                        possible_directions = ['up', 'down', 'left', 'right']
                    else:
                        found_ship = False
                        if followed == None:
                            following = False

                    # VISUALIZATION
                    vshot = [keys[opp_shot[1]], values[opp_shot[0]]]
                    player.own_board.mark_hit_cell(vshot, None, found_ship)
                    opp_shot = None

                # CRITERIUM FOR ENDING
                if player.number_ships_sunk == 10:
                    player.own_board.endScreen(False)
                if player2.number_ships_sunk == 10:
                    player.own_board.endScreen(True)
                        
            # END MENU
            elif player.own_board.state == 3:
                if event.type==pygame.MOUSEBUTTONDOWN:
                    x_start=pygame.mouse.get_pos()[0]
                    y_start=pygame.mouse.get_pos()[1]
                    if player.own_board.endScreen_restart(x_start, y_start) == True:
                        opp_winning_shots = []
                        possible_directions = []
                        found_ship = False
                        local_search = 0
                        main()
                    if player.own_board.endScreen_restart(x_start, y_start) == False:
                        player.own_board.item.fill(BLACK)
                        pygame.quit()
                        run=False
                        sys.exit()

def standalone():
    main()
    return

if __name__ == '__main__': standalone()




              
            
                      

                        

    
                       
            
               
