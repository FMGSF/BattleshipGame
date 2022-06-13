import pygame
import numpy as np
from shps.ships import *
from board_functions.board_funs import *
from game_functions.game_fun import *

screen_width=1120
screen_height=680
pygame.init()
pygame.font.init()


class Board(object):
    """ The Board class is the object which stores the Pygame display with which the user interacts directly
    for playing the game.

    Attributes
    -------
    located_boats: Pygame.sprite.group
        Sprite group that contains all the boats that are already blitted on the Board
    occupied_cells: numpy array
        the variable represents the positions of the Ships placed. The numpy matrix is filled with 0s at
        initialization and it is updated with 1s in the cells where there is a Boat.
    occupied_shadow: list
        a list of list storing all the grid indexes that are adjacent to an already placed ship, necessary
        to enforce a distance of at least one square during the player's insertion phase
    hit_cells: list
        the list containing the coordinates of all the cells hit by the Player.
    item: Pygame.surface
        the variable is the actual Pygame.surface representing the screen.
    placed_ships: list
        a storing list in which each element of the list contains respectively the name of the Ship, a list with
        all the numerical coordinates occupied by the Ship and the Ship's remaining life.
    state: int
        variable representing the current state of the Board (used for differentiating whether we are in the
        menus, or whether we are playing etc...)
    coord_dictionary(_mark): dict
        dictionary with the coordinates of the Players'/Opponents' board
    """
    def __init__(self):
        self.located_boats = pygame.sprite.Group() # list containing all the boats placed on the board
        self.occupied_cells = np.zeros((10, 10))
        self.occupied_shadow = []
        self.hit_cells = [] # list containing all the cell hit by a shot declared by the player
        self.item = pygame.display.set_mode((screen_width, screen_height)) # setting display's dimensions
        self.item.fill(BLACK) # we fill the display with our color
        self.placed_ships = []
        self.state = 0
        self.coord_dictionary = {b"A":b"1",
                                 b"B":b"2",
                                 b"C":b"3",
                                 b"D":b"4",
                                 b"E":b"5",
                                 b"F":b"6",
                                 b"G":b"7",
                                 b"H":b"8",
                                 b"I":b"9",
                                 b"J":b"10"}
        self.coord_dictionary_mark = {b"a":b"1",
                                      b"b":b"2",
                                      b"c":b"3",
                                      b"d":b"4",
                                      b"e":b"5",
                                      b"f":b"6",
                                      b"g":b"7",
                                      b"h":b"8",
                                      b"i":b"9",
                                      b"j":b"10"}
    def get_coord(self, a, b):
        """ This method is used for translating, when it is possible, the coordinates of the mouse from the
        pixel representation to a more user-friendly representation which is the grid-based one drawn with
        the Board.draw_screen method.

        Parameters
        ----------
        a: int
            the x-coordinates of the mouse cursor over the screen
        b: int
            the y-coordinates of the mouse cursor over the screen

        Returns
        -------
        coord: list
            the Board's cells over which the mouse input was encountered
        """
        coord = []
        if a > block_size*3 and a < block_size*13 and b > block_size*3 and b < block_size*13:
            x_val = (a - block_size*2)//block_size
            y_val = (b - block_size*2)//block_size
            axis = [k for k in self.coord_dictionary.keys()]
        elif a > block_size * 16 and a < block_size * 26 and b > block_size * 3 and b < block_size * 13:
            x_val = (a - block_size * 15) // block_size
            y_val = (b - block_size * 2) // block_size
            axis = [k for k in self.coord_dictionary_mark.keys()]
        else:
            return False
        for c in axis:
            if axis.index(c) + 1 == x_val:
                coord.append(c)
                coord.append(y_val)
                return coord

    def draw_menu(self):
        """ This method is used for drawing the initial menu where the Player can click the button
        to start the game.
        """
        self.state = 1
        text = "WELCOME TO THE BATTLESHIP GAME"
        draw_text(self.item, RED, text, 50, screen_width//2, screen_height//2 - 2*block_size)
        text1 = " CLICK HERE TO PLAY "
        button = pygame.Surface((block_size*4, block_size))   # messo 4
        button.fill(BLACK)
        button_rect = button.get_rect()
        button_rect.center = (screen_width//2, screen_height//2 + 2*block_size)
        self.item.blit(button, button_rect)
        pygame.draw.line(self.item, RED, (screen_width//2- 6*block_size, screen_height//2 + 2.8*block_size),(screen_width//2+ 6*block_size, screen_height//2 + 2.8*block_size))   # era 4.5
        pygame.draw.line(self.item, RED, (screen_width//2- 6*block_size, screen_height//2 + 1.8*block_size),(screen_width//2+ 6*block_size, screen_height//2 + 1.8*block_size))
        pygame.draw.line(self.item, RED, (screen_width//2- 6*block_size, screen_height//2 + 2.8*block_size),(screen_width//2- 6*block_size, screen_height//2 + 1.8*block_size))
        pygame.draw.line(self.item, RED, (screen_width//2+ 6*block_size, screen_height//2 + 2.8*block_size), (screen_width//2+ 6*block_size, screen_height//2 + 1.8*block_size))
        draw_text(self.item, RED, text1, 30, screen_width//2, screen_height//2 + 2*block_size)
        pygame.display.update()

    def draw_menu_click(self, pos):
        """ This method is used to check whether the mouse position, caught during the main loop, is located
        on the starting button within the welcoming screen menu of the game.
        """
        if (pos[0][0] > screen_width // 2 - 4.5 * block_size) and (pos[0][0] < screen_width // 2 + 4.5 * block_size) \
                    and (pos[0][1] < screen_height // 2 + 2.8 * block_size) and (pos[0][1] > screen_height // 2 + 1.8 * block_size):
            self.item.fill(BLACK)
            return True
        else:
            return False

    def draw_screen_game(self):
        """
        This method is used for drawing the game interface.
        It also contains the instructions to draw the counters of the placed Ships, i.e. the boats already
        placed by the Player together with their stylized images and their respective sizes.
        """
        self.state = 2
        for y in range(block_size*2, block_size*14, block_size): # loop over the y-axis
            x = block_size*2
            pygame.draw.line(self.item, RED, (x, y), (x+440, y))
        pygame.display.flip() # updating the display object
        for x in range(block_size*2, block_size*14, block_size): # same loop but on the x-axis
            y = block_size*2
            pygame.draw.line(self.item, RED, (x, y), (x, y+440))
        pygame.display.flip() # updating the display object
        for y in range(block_size*2, block_size*14, block_size): # loop over width and height of the second half of the screen
            x = block_size*15
            pygame.draw.line(self.item, RED, (x, y), (x+440, y))
        pygame.display.flip() # updating the display object
        for x in range(block_size*15, block_size*27, block_size):
            y = block_size*2
            pygame.draw.line(self.item, RED, (x, y), (x, y+440))
        pygame.display.flip() # updating the display object
        l = []
        for k in self.coord_dictionary.keys(): # keys reference columns
            l.append(k)
            x = (l.index(k)+3.5)*block_size # x coord for each key in the list
            font = pygame.font.Font('freesansbold.ttf',15) # we choose the font and the dimension of the text
            text = font.render(k, True, RED) # we pass the k object through a font's method
            textRect = text.get_rect() # rectangualr coords of the text object
            textRect.x = x # x attribute of the rect object
            textRect.y = block_size*2.5 # y attribute of the rect
            self.item.blit(text, (textRect.x, textRect.y)) # draw the surface on the display
        pygame.display.flip() # update the display
        m = []
        for v in self.coord_dictionary.values(): # same as before but for the numbers, that reference rows
            m.append(v)
            y = (m.index(v)+3.5)*block_size
            font = pygame.font.Font('freesansbold.ttf', 15)
            text1 = font.render(v, True, RED)
            textRect1 = text1.get_rect()
            textRect1.x = block_size*2.5
            textRect1.y = y
            self.item.blit(text1, (textRect1.x, textRect1.y))
        pygame.display.flip()
        l=[]
        for k in self.coord_dictionary_mark.keys(): # we do the same thing but for the right side of the screen
            l.append(k)
            x = (l.index(k)+16.5)*block_size
            font = pygame.font.Font('freesansbold.ttf',15)
            text = font.render(k, True, RED)
            textRect = text.get_rect()
            textRect.x = x
            textRect.y = block_size*2.5
            self.item.blit(text, (textRect.x, textRect.y))
        pygame.display.flip()
        m=[]
        for v in self.coord_dictionary_mark.values():
            m.append(v)
            y = (m.index(v)+3.5)*block_size
            font = pygame.font.Font('freesansbold.ttf',15)
            text1 = font.render(v, True, RED)
            textRect1 = text1.get_rect()
            textRect1.x = block_size*15.5
            textRect1.y = y
            self.item.blit(text1, (textRect1.x, textRect1.y))
        pygame.display.flip()

        # HEADER
        header = "BATTLESHIP GAME"
        font1 = pygame.font.Font('freesansbold.ttf',35)
        textH = font1.render(header, True, RED)
        textH_rect = textH.get_rect()
        textH_rect.x = block_size*9.5
        textH_rect.y = block_size*0.5
        self.item.blit(textH, (textH_rect.x, textH_rect.y))
        pygame.display.flip()

        # SHIP-COUNTERS REPRESENTATION
        font = pygame.font.Font('freesansbold.ttf',40)
        # Info text
        info_text = "TIME TO PLACE YOUR TROOPS"
        info = font.render(info_text, True, GRAY)
        info_rect = info.get_rect()
        info_rect.center = (screen_width//2, 15 * block_size)
        pygame.time.delay(400)
        self.item.blit(info, info_rect)
        pygame.display.flip()
        pygame.time.delay(700)
        self.item.fill(pygame.Color("black"), (0, 13.5 * block_size, screen_width, 4 * block_size))
        pygame.display.flip()
        self.draw_undo_button()
        font = pygame.font.Font('freesansbold.ttf', 18)
        font2 = pygame.font.Font('freesansbold.ttf', 16)
        pygame.time.delay(300)
        self.counter_Aircraft, self.counter_Patrol, self.counter_Submarine, self.counter_Destroyer, self.counter_Battleship = 0, 0, 0, 0, 0
        # Aircraft carrier text
        txtCarr = "Aircraft carrier {}/1".format(self.counter_Aircraft)
        textCarr = font.render(txtCarr, True, GRAY)
        textCarr_rect = textCarr.get_rect()
        textCarr_rect.center = (4.5*block_size, 14*block_size)
        self.item.blit(textCarr, textCarr_rect)
        # Aircraft Carrier model
        Carrier_model = pygame.Surface((block_size*5, block_size))
        Carrier_model.fill(GREEN)
        Carrier_rect = Carrier_model.get_rect()
        Carrier_rect.y = 14.5*block_size
        Carrier_rect.x = 2*block_size
        self.item.blit(Carrier_model, Carrier_rect)
        # Aircraft Carrier size
        sizCarr = "5 blocks"
        sizeCarr = font2.render(sizCarr, True, GRAY)
        sizeCarr_rect = sizeCarr.get_rect()
        sizeCarr_rect.center = (4.5 * block_size, 16*block_size)
        self.item.blit(sizeCarr, sizeCarr_rect)
        # Battleship text
        txtBatt = "Battleship {}/1".format(self.counter_Battleship)
        textBatt = font.render(txtBatt, True, GRAY)
        textBatt_rect = textBatt.get_rect()
        textBatt_rect.center = (11*block_size, 14*block_size)
        self.item.blit(textBatt, textBatt_rect)
        # Battleship model
        Battleship_model = pygame.Surface((block_size*4, block_size))
        Battleship_model.fill(GREEN)
        Battleship_rect = Battleship_model.get_rect()
        Battleship_rect.y = 14.5*block_size
        Battleship_rect.x = 9*block_size
        self.item.blit(Battleship_model, Battleship_rect)
        # Battleship size
        sizBatt = "4 blocks"
        sizeBatt = font2.render(sizBatt, True, GRAY)
        sizeBatt_rect = sizeBatt.get_rect()
        sizeBatt_rect.center = (11*block_size, 16*block_size)
        self.item.blit(sizeBatt, sizeBatt_rect)
        # Destroyer text
        txtDestr = "Destroyer {}/2".format(self.counter_Destroyer)
        textDestr = font.render(txtDestr, True, GRAY)
        textDestr_rect = textDestr.get_rect()
        textDestr_rect.center = (16.5*block_size, 14*block_size)
        self.item.blit(textDestr, textDestr_rect)
        # Destroyer model
        Destroyer_model = pygame.Surface((block_size*3, block_size))
        Destroyer_model.fill(GREEN)
        Destroyer_rect = Destroyer_model.get_rect()
        Destroyer_rect.y = 14.5*block_size
        Destroyer_rect.x = 15*block_size
        self.item.blit(Destroyer_model, Destroyer_rect)
        # Destroyer size
        sizDestr = "3 blocks"
        sizeDestr = font2.render(sizDestr, True, GRAY)
        sizeDestr_rect = sizeDestr.get_rect()
        sizeDestr_rect.center = (16.5*block_size, 16*block_size)
        self.item.blit(sizeDestr, sizeDestr_rect)
        # Submarine text
        txtSub = "Sub {}/3".format(self.counter_Submarine)
        textSub = font.render(txtSub, True, GRAY)
        textSub_rect = textSub.get_rect()
        textSub_rect.center = (21*block_size, 14*block_size)
        self.item.blit(textSub, textSub_rect)    
        # Submarine model
        Submarine_model = pygame.Surface((block_size*2, block_size))
        Submarine_model.fill(GREEN)
        Submarine_rect = Submarine_model.get_rect()
        Submarine_rect.y = 14.5*block_size
        Submarine_rect.x = 20*block_size
        self.item.blit(Submarine_model, Submarine_rect)
        # Submarine size
        sizSubm = "2 blocks"
        sizeSubm = font2.render(sizSubm, True, GRAY)
        sizeSubm_rect = sizeSubm.get_rect()
        sizeSubm_rect.center = (21*block_size, 16*block_size)
        self.item.blit(sizeSubm, sizeSubm_rect)
        # Patrol text
        txtPat = "Patrol {}/3".format(self.counter_Patrol)
        textPat = font.render(txtPat, True, GRAY)
        textPat_rect = textPat.get_rect()
        textPat_rect.center = (24.5*block_size, 14*block_size)
        self.item.blit(textPat, textPat_rect) 
        # Patrol model
        Patrol_model=pygame.Surface((block_size*1, block_size))
        Patrol_model.fill(GREEN)
        Patrol_rect = Patrol_model.get_rect()
        Patrol_rect.y = 14.5*block_size
        Patrol_rect.x = 24*block_size
        self.item.blit(Patrol_model, Patrol_rect)
        # Patrol size
        sizPatrol = "1 block"
        sizePatrol = font2.render(sizPatrol, True, GRAY)
        sizePatrol_rect = sizePatrol.get_rect()
        sizePatrol_rect.center = (24.5*block_size, 16*block_size)
        self.item.blit(sizePatrol, sizePatrol_rect)

        pygame.display.flip()
    
    def update_counters(self):
        """
        This method is called each time a Ship is drawn onto the screen.
        It updates the images of the counters on the screen.
        """
        font = pygame.font.Font('freesansbold.ttf', 18)
        self.item.fill(pygame.Color("black"), (0, 13.1 * block_size, screen_width, 1.1 * block_size))
        # Aircraft text
        txtCarr = "Aircraft carrier {}/1".format(self.counter_Aircraft)
        textCarr = font.render(txtCarr, True, GRAY)
        textCarr_rect = textCarr.get_rect()
        textCarr_rect.center = (4.5*block_size, 14*block_size)
        self.item.blit(textCarr, textCarr_rect)
        # Battleship Text
        txtBatt = "Battleship {}/1".format(self.counter_Battleship)
        textBatt = font.render(txtBatt, True, GRAY)
        textBatt_rect = textBatt.get_rect()
        textBatt_rect.center = (11*block_size, 14*block_size)
        self.item.blit(textBatt, textBatt_rect)
        # Destroyer text
        txtDestr = "Destroyer {}/2".format(self.counter_Destroyer)
        textDestr = font.render(txtDestr, True, GRAY)
        textDestr_rect = textDestr.get_rect()
        textDestr_rect.center = (16.5*block_size, 14*block_size)
        self.item.blit(textDestr, textDestr_rect)
        # Submarine text
        txtSub = "Sub {}/3".format(self.counter_Submarine)
        textSub = font.render(txtSub, True, GRAY)
        textSub_rect = textSub.get_rect()
        textSub_rect.center = (21*block_size, 14*block_size)
        self.item.blit(textSub, textSub_rect) 
        # Patrol text
        txtPat = "Patrol {}/3".format(self.counter_Patrol)
        textPat = font.render(txtPat, True, GRAY)
        textPat_rect = textPat.get_rect()
        textPat_rect.center = (24.5*block_size, 14*block_size)
        self.item.blit(textPat, textPat_rect)
        pygame.display.update()

    def remove_last_boat(self, Ship, player):
        """ This method is called whenever the Player clicks on the UNDO button on the main screen of
        the game and it enables the Player to undo the placement of the last ship. It updates all the
        attributes of the Player instantiation, together with those of Player.own_board, and it is in
        fact a rollback of the respective method insert_boat. It also deals with visualization, by
        removing the plotted green image of the last placed ship and redrawing the board of the player.

        Parameters
        ----------
        Ship: object
            instantiation of the last Ship placed, accessed through the board.located_boats attribute
        player: object
            instantiation of the Player class, necessary to update the attribute player.boats which
            stores the available ships yet to be placed
        """
        ship = self.located_boats.sprites()[-1]
        player.boats.add(ship)
        self.located_boats.remove(ship)
        self.placed_ships.pop()
        self.occupied_shadow.pop()
        for a in ship.coordinates:
            self.occupied_cells[a[0], a[1]] = 0
        if ship.size == 5:
            self.counter_Aircraft -= 1
        elif ship.size == 4:
            self.counter_Battleship -= 1
        elif ship.size == 3:
            self.counter_Destroyer -= 1
        elif ship.size == 2:
            self.counter_Submarine -= 1
        else:
            self.counter_Patrol -= 1
        self.update_counters()
        ship.image.fill(BLACK)
        self.item.blit(ship.image, ship.rect)
        for y in range(block_size*2, block_size*14, block_size): # loop over the y-axis
            x = block_size*2
            pygame.draw.line(self.item, RED, (x, y), (x+440, y))
        for x in range(block_size*2, block_size*14, block_size): # loop over width and height of the second half of the screen
            y = block_size*2
            pygame.draw.line(self.item, RED, (x, y), (x, y+440))
        for ship in self.located_boats:
            self.item.blit(ship.image, ship.rect)
        pygame.display.flip()

    def draw_undo_button(self):
        """ This method is functional for the graphical visualization of the Undo button on the main screen
        of the game.
        """
        self.undo = pygame.draw.circle(self.item, GRAY, (1.2*block_size, 1.2*block_size), 32)
        txt = 'UNDO'
        font = pygame.font.Font('freesansbold.ttf', 18)
        text = font.render(txt, True, DARK_RED)
        text_rect = text.get_rect()
        text_rect.center = self.undo.center
        self.item.blit(text, text_rect)

    def check_undo_click(self, mouse, player):
        """ This method is called within the main loop every time an event MOUSEBUTTONDOWN is caught
        and it checks whether this click is placed onto the Undo button. If this is the case, it
        calls the method remove_last_boat to deal with the storing update and the graphical reset
        of the removed ship.

        Parameters
        ----------
        mouse: tuple
            the mouse position caught during the main loop, associated with a click on the screen
        player: object
            instantiation of the Player class
        """
        if self.undo.collidepoint(mouse):
            self.remove_last_boat(self, player)

    def insert_boat(self, Ship):
        """ This method is used to draw the given Ship on the Board. It also calls Board.update_counters.
        In order to use this method the Ship must already have been passed together with its
        coordinates and whether it is vertical or not.

        Parameters
        ----------
        Ship: object
            the Ship instantiation to be blitted
        """
        Ship.coordinates = get_num_coord(Ship.grid_pos, bool(Ship.vertical), Ship.size)
        if self.located_boats.has == False: # when there are no boats on the display, the first boat can go anywhere
            self.item.blit(Ship.image, Ship.rect)
            self.located_boats.add(Ship)
            pygame.display.flip() # update display
        else:  # we loop over the already located boats and get their shadow, in order to avoid collision
            for i in self.located_boats:
                if pygame.sprite.collide_rect(i, Ship) == True and i is not Ship:
                    return  # colliding with other (graphical) Ships
            for point in Ship.coordinates:
                for idx in range(len(self.occupied_shadow)):
                    if point in self.occupied_shadow[idx]:
                        return  # shadow of other ships in position
            self.item.blit(Ship.image, Ship.rect)  # we blit the Ship on the display since there is no collision
            self.located_boats.add(Ship)
            pygame.display.flip()
        Ship.get_shadow()
        self.occupied_shadow.append(Ship.shadow)
        self.placed_ships.append([Ship.name, Ship.coordinates, Ship.life])
        for a in Ship.coordinates:
            self.occupied_cells[a[0], a[1]] = 1
        if Ship.size == 5:
            self.counter_Aircraft += 1
        elif Ship.size == 4:
            self.counter_Battleship += 1
        elif Ship.size == 3:
            self.counter_Destroyer += 1
        elif Ship.size == 2:
            self.counter_Submarine += 1
        else:
            self.counter_Patrol += 1
        self.update_counters()
        pygame.display.flip()

        # WAR starts when the insertion is completed
        if self.counter_Aircraft == 1 and self.counter_Battleship == 1 and self.counter_Destroyer == 2 and self.counter_Submarine == 3 and self.counter_Patrol == 3:
            font = pygame.font.Font('freesansbold.ttf', 40)
            self.item.fill(pygame.Color("black"), (0, 13.1 * block_size, screen_width, 4 * block_size))
            pygame.time.delay(600)
            text1 = "    YOUR TROOPS ARE READY    "
            txt1 = font.render(text1, True, GRAY)
            txt1_rect = txt1.get_rect()
            txt1_rect.center = (screen_width // 2, 15 * block_size)
            self.item.blit(txt1, txt1_rect)
            pygame.display.flip()
            pygame.time.delay(900)

            self.item.fill(pygame.Color("black"), (0, 13.1 * block_size, screen_width, 4 * block_size))
            text2 = "  !!!     THE  WAR STARTS NOW      !!!  "
            txt2 = font.render(text2, True, RED)
            txt2_rect = txt2.get_rect()
            txt2_rect.center = (screen_width//2, 15*block_size)
            self.item.blit(txt2, txt2_rect)
            pygame.display.flip()
            pygame.time.delay(900)

            self.item.fill(pygame.Color("black"), (0, 13.1 * block_size, screen_width, 4 * block_size))
            text3 = "          SHOOT, MY CAPTAIN          "
            txt3 = font.render(text3, True, GRAY)
            txt3_rect = txt3.get_rect()
            txt3_rect.center = (screen_width // 2, 15 * block_size)
            self.item.blit(txt3, txt3_rect)
            pygame.display.flip()

    def mark_hit_cell(self, a, hit, random_hit):
        """ This method is used for drawing a pointer (a red cross or a green block) on a given coordinate of
        the Board's grids.

        Parameters
        ----------
        a: list
            the list representing the hit coordinate
        hit: bool or None
            the variable is True when the shot is made by the Player and it is successful.
            its value is False when the shot is made by the Player and it is not successful.
            its value is None when the shot is made by the Random instantiation
        random_hit: bool
            the variable is called in the function only in case it is the Random player shooting.
            It evaluates to True when the shot has hit a ship, otherwise it is False. It is
            functional for different board visualizations during the game.
        """
        x = return_x_val(a[0]) # we call this function for the upper-left corner of the area at which we have to draw the lines
        y = return_y_val(a[1])
        font = pygame.font.Font('freesansbold.ttf',40)
        text2 = "  !!!      YOU MISSED IT      !!!  "
        txt2 = font.render(text2, True, GRAY)
        txt2_rect = txt2.get_rect()
        txt2_rect.center = (screen_width//2, 15*block_size)
        text1 = "  !!!      YOU HIT ONE      !!!  "
        txt1 = font.render(text1, True, GREEN)
        txt1_rect = txt1.get_rect()
        txt1_rect.center = (screen_width//2, 15*block_size)
        text3 = "  !!!     YOU HAVE BEEN HIT     !!!  "
        txt3 = font.render(text3, True, RED)
        txt3_rect = txt3.get_rect()
        txt3_rect.center = (screen_width // 2, 15 * block_size)
        text4 = "  !!!     YOU HAVE BEEN MISSED     !!!  "
        txt4 = font.render(text4, True, GRAY)
        txt4_rect = txt4.get_rect()
        txt4_rect.center = (screen_width // 2, 15 * block_size)

        if hit == False:
            self.hit_cells.append(a)  # storing
            pygame.time.delay(300)
            self.item.fill(pygame.Color("black"), (0, 13.1*block_size,screen_width,4*block_size))
            self.item.blit(txt2, txt2_rect)
            x = return_x_val(a[0])+ block_size # we call this function for the upper-left corner of the area at which we have to draw the lines
            start_pos1 = (x, y)
            start_pos2 = (x, y + block_size)
            end_pos1 = (x + block_size, y + block_size)
            end_pos2 = (x + block_size, y)
            pygame.draw.line(self.item, (200,0,0), start_pos1, end_pos1, width=5)
            pygame.draw.line(self.item, (200,0,0), start_pos2, end_pos2, width=5)
            pygame.display.flip()
        elif hit == True:
            self.hit_cells.append(a)  # storing
            pygame.time.delay(300)
            self.item.fill(pygame.Color("black"), (0, 13.1*block_size,screen_width,4*block_size))
            self.item.blit(txt1, txt1_rect)
            rect = pygame.Rect(x + block_size, y, block_size, block_size)
            pygame.draw.rect(self.item, GREEN, rect)
            pygame.display.flip()
        elif hit == None:
            start_pos1 = (x, y)
            start_pos2 = (x, y + block_size)
            end_pos1 = (x + block_size, y + block_size)
            end_pos2 = (x + block_size, y)
            pygame.time.delay(300)
            self.item.fill(pygame.Color("black"), (0, 13.1 * block_size, screen_width, 4 * block_size))
            if random_hit:
                self.item.blit(txt3, txt3_rect)
                pygame.draw.line(self.item, RED, start_pos1, end_pos1, width=5)
                pygame.draw.line(self.item, RED, start_pos2, end_pos2, width=5)
                pygame.time.delay(300)
            else:
                self.item.blit(txt4, txt4_rect)
                pygame.draw.line(self.item, BLUE, start_pos1, end_pos1, width=5)
                pygame.draw.line(self.item, BLUE, start_pos2, end_pos2, width=5)
                pygame.time.delay(300)
            pygame.display.flip()
        
    def endScreen(self, win):
        """ This method is used for drawing the final menu after the game is over.

        Parameters
        ----------
        win: bool
            this value is True when the Player has just won the finished game.
            it is False when the Player has lost.
            it is referenced for writing different texts on the end menu depending on the result of the game.

        """
        self.state = 3
        self.item.fill(GREEN)
        pygame.time.delay(300)
        text = "  !!!     GAME  OVER      !!!  "
        draw_text(self.item, BLACK, text, 50, screen_width//2, 2*block_size)
        text0 = "DO YOU WANT TO PLAY AGAIN ?"
        text1 = "PLAY"
        text2 = "QUIT"
        text3 = "YOU SAVED THE PLANET"
        text4 = "YOU LOST, IT HAPPENS"
        draw_text(self.item, BLACK, text0, 30, screen_width//2, 330)
        draw_text(self.item, BLACK, text1, 30, screen_width//2-6*block_size, 500)
        draw_text(self.item, BLACK, text2, 30, screen_width//2+6*block_size, 500)
        if win:
            draw_text(self.item, BLACK, text3, 40, screen_width//2, 5*block_size)
        if not win:
            draw_text(self.item, BLACK, text4, 40, screen_width//2, 5*block_size)
        # PLAY AGAIN BUTTON
        pygame.draw.line(self.item, BLACK, (screen_width//2 - 8.5*block_size, 490), (screen_width//2 - 3.5*block_size, 490))
        pygame.draw.line(self.item, BLACK, (screen_width//2 - 8.5*block_size, 535), (screen_width//2 - 3.5*block_size, 535))
        pygame.draw.line(self.item, BLACK, (screen_width//2 - 8.5*block_size, 535), (screen_width//2 - 8.5*block_size, 490))
        pygame.draw.line(self.item, BLACK, (screen_width//2 - 3.5*block_size, 490), (screen_width//2 - 3.5*block_size, 535))
        # QUIT BUTTON
        pygame.draw.line(self.item, BLACK, (screen_width//2 + 3.5*block_size, 490), (screen_width//2 + 8.5*block_size,  490))
        pygame.draw.line(self.item, BLACK, (screen_width//2 + 3.5*block_size, 535), (screen_width//2 + 8.5*block_size,  535))
        pygame.draw.line(self.item, BLACK, (screen_width//2 + 3.5*block_size, 490), (screen_width//2 + 3.5*block_size, 535))
        pygame.draw.line(self.item, BLACK, (screen_width//2 + 8.5*block_size,  490), (screen_width//2 + 8.5*block_size, 535))

        pygame.display.update()

    def endScreen_restart(self, x_start, y_start):
        if (x_start < screen_width // 2 - 3.5 * block_size) and (x_start > screen_width // 2 - 8.5 * block_size) and \
                (y_start < 535 and y_start > 490):
            return True
        if (y_start < 535 and y_start > 490) and (x_start > screen_width // 2 + 3.5) and \
                (x_start < screen_width // 2 + 8.5 * block_size):
            return False
        else:
            return None




