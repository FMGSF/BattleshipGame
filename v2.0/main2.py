import sys
import pygame
from plyr.player import Player as Player
from plyr.player import Player_ as Player_
import numpy as np
from game_functions.game_fun import *
from my_network.network import Network as Network1
from shps.ships import BLACK, DARK_RED




pygame.init()
pygame.display.init() 
black = (255, 255, 255)
white = (0,0,0)
green = (0, 255, 0)
red = (255, 0, 0)
block_size = 40
fps = 200
screen_width = 1320
screen_height = 660
grid_opp = np.zeros((10, 10), dtype = int)
dictionary = {b"A":b"1", b"B":b"2", b"C":b"3", b"D":b"4", b"E":b"5", b"F":b"6", b"G":b"7", b"H":b"8", b"I":b"9", b"J":b"10"}
keys = [k for k in dictionary.keys()]
values = [v for v in dictionary.values()]
grid = np.zeros((10, 10), dtype=int)
found_ship = False
x_start = float()
y_start = float()




def client():
    """
    Game/Client loop
    """
    global found_ship
    global x_start
    global y_start
    transmitted = False
    okay = True
    opponent_lives_counter = 0
    run = True
    clock = pygame.time.Clock()
    round = 0
    n0 = Network1()
    while True:
        try:
            n0.connect()
            break
        except TimeoutError as e:
            print(e)  
    info = n0.recv()
    n_player = int(info[0])
    n_game = int(info[2]) 
    player = Player()
    player2 = Player_()
    pygame.display.set_caption(f"battleship_game, game :  {n_game},  player:  {n_player}  ")   
    while run:
        print(player.own_board.placed_ships)
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:              
               pygame.quit()
               run = False            
            if player.own_board.state == 0:
                player.own_board.draw_menu()
            if player.own_board.state == 1:
                coord = []
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x0 = pygame.mouse.get_pos()[0]
                    y0 = pygame.mouse.get_pos()[1]
                    coord.append([x0, y0])
                    if player.own_board.draw_menu_click(coord) == (True, True):                       
                        pygame.display.update()
                        player.own_board.draw_screen_game()
                        continue
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x0 = pygame.mouse.get_pos()[0]
                    y0 = pygame.mouse.get_pos()[1]
                    coord.append([x0, y0])
                    if player.own_board.draw_menu_click(coord) == (True, False):
                        player.own_board.item.fill(pygame.Color("black"), (0, 0,screen_width,block_size*2))
                        player.own_board.display_help_message()
                if event.type == pygame.MOUSEBUTTONUP:
                    player.own_board.delete_help_message()
            elif len(player.boats.sprites()) > 0 and player.own_board.state == 2:
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    pos_start = pygame.mouse.get_pos()
                    x_start = pos_start[0]
                    y_start = pos_start[1]
                    player.own_board.check_undo_click(pos_start, player)
                if (event.type == pygame.MOUSEBUTTONUP):
                    pos_end = pygame.mouse.get_pos()
                    x_end = pos_end[0]
                    y_end = pos_end[1]
                    if player_placement(x_start, y_start, x_end, y_end, player):
                        trip, vertical, length = player_placement(x_start, y_start, x_end, y_end, player)
                        for boat in player.boats:
                            if boat.size == length:
                                boat.vertical = vertical
                                boat.set_gridpos([str(trip[0][0], encoding = 'utf-8'), trip[0][1]])
                                player.own_board.insert_boat(boat)
                                break
                        for placed in player.own_board.located_boats:
                            for boat in player.boats:
                                if placed == boat:
                                    player.boats.remove(placed)
                                    break
                    else:
                        x_start, y_start = float(), float()
                    st_occ_cell = np.array2string(player.own_board.occupied_cells)
            elif  len(player.boats.sprites()) == 0 and player.own_board.state == 2 and transmitted == False:
                player.own_board.draw_game_message("WAITING FOR OPPONENT'S ARMY", DARK_RED)
                try:
                    n0.send(str(n_player) + st_occ_cell)
                    data = n0.recv()
                    print("Data sent:   ", str(n_player) + st_occ_cell)
                    print("Data received:   ", data)
                except Exception as e:
                    print(e)
                if data != "still nothing yet":
                    try:
                        reduced_string = data.translate({ord(']'): None,ord('['): None, ord('\n'):None})#cleaning the incoming signal
                        arr=np.fromstring(reduced_string, dtype=float, sep= " ").reshape(10, 10)
                        player2.own_board = arr
                        transmitted = True
                        player.own_board.draw_game_message("THE ENEMY HAS COME", DARK_RED)
                        pygame.time.delay(1500)
                    except Exception as e:                        
                        print(e)       
            elif  len(player.boats.sprites()) == 0 and player.own_board.state==2 and transmitted==True:
                if okay==True:
                    if (event.type == pygame.MOUSEBUTTONDOWN):
                        player.own_board.item.fill(pygame.Color("black"), (0, 13.1*block_size,screen_width,4*block_size))
                        pygame.display.flip()
                        pos_start = pygame.mouse.get_pos()
                        x_start = pos_start[0]
                        y_start = pos_start[1]
                    if (event.type == pygame.MOUSEBUTTONUP):
                        pos_end = pygame.mouse.get_pos()
                        x_end = pos_end[0]
                        y_end = pos_end[1]
                        if player_shoot(x_start, y_start, x_end, y_end, player):
                            coord_start, idxes = player_shoot(x_start, y_start, x_end, y_end, player)
                            if coord_start not in player.own_board.hit_cells:
                                round_played = True
                                if shoot_bullet(idxes, player2.own_board):
                                    player.own_board.mark_hit_cell(coord_start, True, found_ship)
                                    round += 1
                                    opponent_lives_counter += 1
                                    okay = False
                                else:  
                                    player.own_board.mark_hit_cell(coord_start, False, found_ship)
                                    round += 1
                                    okay = False                             
                                info_shot = "$" + f"*{n_player}*" + str(coord_start[0], encoding="utf-8") + str(coord_start[1]) + f"#{round}#" 
                                if round_played == True:
                                    try:
                                        n0.send(info_shot)
                                        shot_opp = n0.recv()
                                        print("Data sent:   ", info_shot)
                                        print("Data received:   ", shot_opp)                                      
                                        if shot_opp[2] != info_shot[2]:
                                            if shot_opp[6] == "0":
                                                col = int(shot_opp[5:7])
                                            else:
                                                col = int(shot_opp[5])
                                            cell = [bytes(shot_opp[4].upper(), encoding = "utf-8"), col]
                                            cell_corr = [bytes(shot_opp[4], encoding = "utf-8"), col]
                                            if get_num_coord_opp(cell_corr) in player.own_board.occupied_positions:
                                                player.own_board.mark_hit_cell(cell, None, 1)
                                                pygame.time.delay(1500)
                                                update_hit_ship(get_num_coord_opp(cell_corr), player)
                                            else:
                                                player.own_board.mark_hit_cell(cell, None, 0)
                                                pygame.time.delay(1500)
                                            okay = True
                                        else:
                                            player.own_board.draw_game_message("WAITING FOR OPPONENT'S SHOT", DARK_RED)                                     
                                    except IndexError as idxERR:
                                        print(idxERR, "look up line 216")
                                    except Exception as ex:
                                        print(ex, "look up line 216")
                else:
                    try:
                        shot = coord_start
                        info_shot = "$" + f"*{n_player}*" + str(shot[0], encoding="utf-8") + str(shot[1]) + f"#{round}#"                       
                        n0.send(info_shot)
                        shot_opp = n0.recv()
                        print("Data sent:   ", info_shot)
                        print("Data received:   ", shot_opp)                     
                        if shot_opp[2] != info_shot[2] and shot_opp != "still nothing yet":
                            if shot_opp[6] == "0":
                                col = int(shot_opp[5:7])
                            else:
                                col = int(shot_opp[5])
                            cell = [bytes(shot_opp[4].upper(), encoding="utf-8"), col]
                            cell_corr = [bytes(shot_opp[4], encoding="utf-8"), col]                          
                            if get_num_coord_opp(cell_corr) in player.own_board.occupied_positions:
                                player.own_board.mark_hit_cell(cell, None, 1)
                                pygame.time.delay(1500)
                                update_hit_ship(get_num_coord_opp(cell_corr), player)
                            else:
                                player.own_board.mark_hit_cell(cell , None, 0)
                                pygame.time.delay(1500)
                            okay = True
                            break
                        else:
                            player.own_board.draw_game_message("WAITING FOR OPPONENT'S SHOT'", DARK_RED)                                   
                    except Exception as e:
                        print(e, "look up try statement at line 190")
                        break
                    except IndexError as idx:                      
                        print(idx, "Index error, look up try statement at line 190")              
                if player.number_ships_sunk == 10:                   
                    player.own_board.endScreen(False)
                if opponent_lives_counter == 24:                 
                    player.own_board.endScreen(True)
            elif player.own_board.state == 3:
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        x_start=pygame.mouse.get_pos()[0]
                        y_start=pygame.mouse.get_pos()[1]
                    if player.own_board.endScreen_restart(x_start, y_start) == True:
                        n0.close()
                        client()
                    if player.own_board.endScreen_restart(x_start, y_start) == False:                              
                        player.own_board.item.fill(BLACK)
                        pygame.quit()
                        run=False
                        sys.exit()              

                                
                    

                        


            
             

if __name__ == '__main__': client()