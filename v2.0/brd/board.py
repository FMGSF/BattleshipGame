
import pygame
import numpy as np
from shps.ships import *

screen_width=1120
screen_height=680
pygame.init()
pygame.font.init()



class Board(object):

    """
    The Board class is the object which stores the Pygame display with which the user interacts directly
    for playing the game.

    Attributes
    -------
    located_boats: Pygame.sprite.group
        Sprite group that contains all the boats that are already blitted on the Board
    occupied_cells: numpy array
        the variable represents the positions of the Ships placed. The numpy matrix is filled with 0s at
        initialization and it is updated with 1s in the cells where there is a Boat.
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
        pygame.display.set_caption("battleship_game") 
        self.located_boats = pygame.sprite.Group()
        self.occupied_cells = np.zeros((10, 10))
        self.occupied_shadow=[]
        self.hit_cells = [] 
        self.occupied_positions=[]
        self.item = pygame.display.set_mode((screen_width, screen_height)) 
        self.item.fill(BLACK)
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

    def draw_text(self, color, text, size, x, y, flag=0):

        """
        This method is an help function for the insertion of text string on the Pygame surface.
        It returns the graphical representation of the text across the iterations of the main
        loop

        Arguments
        ----------
        color: tuple
            attribute standing for the three RGB coordinates
        text: str
            variable representing the text string to be blitted on the surface
        size: int
            parameter used to set the size of the character for the blitted text
        x: int
            x-coordinates of the text to be blitted (in the Pygame surface) taking into
            consideration the midtop position of the rectangle
        y: int
            y-coordinates of the text to be blitted (in the Pygame surface) taking into
            consideration the midtop position of the rectangle
        """
        
        font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = font.render(text, True, color)       
        text_rect = text_surface.get_rect()
        if flag == 0:                       
            text_rect.center = (x, y)
        elif flag == 1:
            text_rect.topleft = (x , y)  
        elif flag==2:            
            text_rect.midtop = (x, y)       
        self.item.blit(text_surface, text_rect)
        pygame.display.update()

    def draw_menu(self):
        """ 
        GRAPHIC

        This method is used for drawing the initial menu where the Player can click the button
        to start the game.
        """
        self.state = 1
        text = "WELCOME TO THE BATTLESHIP GAME"
        self.draw_text( RED, text, 50, screen_width//2, screen_height//2 - 2*block_size)
        text1 = " CLICK HERE TO PLAY "
        button = pygame.Surface((block_size*4, block_size))   # messo 4
        button.fill(BLACK)
        button_rect = button.get_rect()
        button_rect.center = (screen_width//2, screen_height//2 + 2*block_size)
        self.item.blit(button, button_rect)
        self.draw_text( RED, text1, 30, screen_width//2, screen_height//2 + 2.3*block_size)
        pygame.draw.line(self.item, RED, (screen_width//2- 6*block_size, screen_height//2 + 2.8*block_size),\
            (screen_width//2+ 6*block_size, screen_height//2 + 2.8*block_size))  
        pygame.draw.line(self.item, RED, (screen_width//2- 6*block_size, screen_height//2 + 1.8*block_size),\
            (screen_width//2+ 6*block_size, screen_height//2 + 1.8*block_size))
        pygame.draw.line(self.item, RED, (screen_width//2- 6*block_size, screen_height//2 + 2.8*block_size),\
            (screen_width//2- 6*block_size, screen_height//2 + 1.8*block_size))
        pygame.draw.line(self.item, RED, (screen_width//2+ 6*block_size, screen_height//2 + 2.8*block_size),\
            (screen_width//2+ 6*block_size, screen_height//2 + 1.8*block_size))
        text_help="?"
        self.draw_text(RED, text_help, 40, screen_width - block_size//2, 0, flag=2)
        pygame.display.update()

    def display_help_message(self):
        """
        GRAPHIC
        This method is called for displaying the help message in the initial menu
        """
        help_message1="•Click and drag the mouse over the left side Board for placing your Army•"
        help_message2= "•Remember, Boats cannot be adjacent•"
        help_message3="•Click a cell on the right side Board for shooting it• "
        self.draw_text( RED, help_message1, 20, screen_width//2, block_size//2, flag=2)
        self.draw_text( RED, help_message2, 20, screen_width //2, block_size, flag=2)
        self.draw_text(RED, help_message3, 20, screen_width //2, block_size*1.5, flag=2)
        pygame.display.update()

    def blit_surface(self, size:tuple, COLOR, x, y):
        """
        GRAPHIC

        This method is called for blitting Surfaces on the display
        """
        sur=pygame.Surface(size)
        sur.fill(COLOR)
        sur_rect=sur.get_rect()
        sur_rect.x=x
        sur_rect.y=y
        self.item.blit(sur, sur_rect)

    def draw_undo_button(self):
        """ 
        GRAPHIC

        This method is called visualizing the Undo button on the main screen
        of the game.
        """
        self.undo = pygame.draw.circle(self.item, GRAY, (1.2*block_size, 1.2*block_size), 32)
        txt = 'UNDO'
        self.draw_text(DARK_RED,txt, 18, 1.2*block_size, 1.2*block_size)

    def check_undo_click(self, mouse, player):
        """ 
        This method is called within the main loop every time an event MOUSEBUTTONDOWN is caught
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
        if len(self.placed_ships)==0:
            return
        if self.undo.collidepoint(mouse):
            self.remove_last_boat(self, player)

    def delete_help_message(self):
        """
        GRAPHIC

        this method is called for deleting the help message from the initial menu
        """
        self.item.fill(pygame.Color("black"), (0, 0,screen_width,block_size*2))
        text_help="?"
        self.draw_text(RED, text_help, 40, screen_width - block_size//2, 0, flag=2)
        pygame.display.update()

    def draw_game_message(self, what, COLOR):
        """
        GRAPHIC

        This method is called to display messages during the game at a fixed position on the screen
        (right below the two grids)

        Arguments
        ----------
        what: string
            The text to be drawn 

        COLOR: tuple 
            The color used for the text :
        """
        if type(what)==str:
            text_board=what
            font = pygame.font.Font('freesansbold.ttf', 40)
            txt=font.render(text_board, True, COLOR)
            txt_rect = txt.get_rect()
            txt_rect.center = (screen_width//2, 15*block_size)       
            self.item.fill(pygame.Color("black"), (0, 13.1*block_size,screen_width,4*block_size))
            self.item.blit(txt, txt_rect)
            pygame.display.update()
        else:
            print("Invalid  type: argument must be a string")
            return False


    def draw_menu_click(self, pos):
        """
        This method is called for checking whether the mouse input in the initial menu page happens onto a button

        Arguments
         
        ----
        pos:
            the position of the mouse input
        """  
        if (pos[0][0] > screen_width // 2 - 4.5 * block_size) and (pos[0][0] < screen_width // 2 + 4.5 * block_size) \
            and (pos[0][1] < screen_height // 2 + 2.8 * block_size) and (pos[0][1] > screen_height // 2 + 1.8 * block_size):
            self.item.fill(BLACK)
            return (True, True)
        elif (pos[0][0] > screen_width - block_size)  and (pos[0][1] <  block_size) :
            self.item.fill(pygame.Color("black"), (0, 0,screen_width,block_size))
            return (True, False)
        else:
            return False
    def draw_screen_game(self):
        '''
        
        GRAPHIC

        This method is used for drawing the game interface.
        It also contains the instructions to draw the counters of the placed Ships, i.e. the boats already
        placed by the Player.
        '''
        self.state = 2
        for y in range(block_size*2, block_size*14, block_size):          
            x = block_size*2
            pygame.draw.line(self.item, RED, (x, y), (x+440, y))
        pygame.display.flip() 
        for x in range(block_size*2, block_size*14, block_size):
            y = block_size*2
            pygame.draw.line(self.item, RED, (x, y), (x, y+440))
        pygame.display.flip()        
        for y in range(block_size*2, block_size*14, block_size):            
            x = block_size*15
            pygame.draw.line(self.item, RED, (x, y), (x+440, y))
        pygame.display.flip()
        for x in range(block_size*15, block_size*27, block_size): 
            y = block_size*2
            pygame.draw.line(self.item, RED, (x, y), (x, y+440))
        pygame.display.flip() 
        l = []       
        for k in self.coord_dictionary.keys():            
            l.append(k) 
            self.draw_text(RED, k, 15, (l.index(k)+3.5)*block_size, block_size*2.5, flag=1 )
        pygame.display.flip()
        m = []
        for v in self.coord_dictionary.values():
            m.append(v)
            self.draw_text(RED, v, 15, block_size*2.5 , (m.index(v)+3.5)*block_size, flag=1)
        pygame.display.flip()
        l=[]
        for k in self.coord_dictionary_mark.keys():
            l.append(k)
            self.draw_text(RED, k , 15, (l.index(k)+16.5)*block_size, block_size*2.5, flag=1)
        pygame.display.flip()
        m=[]
        for v in self.coord_dictionary_mark.values():
            m.append(v)
            self.draw_text(RED, v, 15, block_size*15.5, (m.index(v)+3.5)*block_size, flag=1)
        pygame.display.flip()      
        header = "BATTLESHIP GAME"
        self.draw_text(RED, header, 35, block_size*9.5, block_size*0.5, flag=1 )
        pygame.time.delay(400)
        info_text = "TIME TO PLACE YOUR TROOPS"
        self.draw_game_message(info_text, GRAY)
        pygame.time.delay(700)
        self.item.fill(pygame.Color("black"), (0, 13.5 * block_size, screen_width, 4 * block_size))
        pygame.display.update()
        self.draw_undo_button()       
        self.counter_Aircraft = self.counter_Patrol = self.counter_Submarine = self.counter_Destroyer = self.counter_Battleship = 0    
        txtCarr = f"Aircraft carrier {self.counter_Aircraft}/1"
        self.draw_text( GRAY, txtCarr, 18, 4.5*block_size, 14*block_size)      
        self.blit_surface((block_size*5, block_size), GREEN, 2*block_size, 14.5*block_size )
        sizCarr = "5 blocks"
        self.draw_text(GRAY, sizCarr, 16, 4.5 * block_size, 16*block_size)   
        txtBatt = f"Battleship {self.counter_Battleship}/1"
        self.draw_text( GRAY, txtBatt, 18, 11*block_size, 14*block_size)
        self.blit_surface((block_size*4, block_size), GREEN,9*block_size, 14.5*block_size)
        sizBatt = "4 blocks"
        self.draw_text(GRAY, sizBatt, 16, 11 * block_size, 16*block_size)     
        txtDestr = f"Destroyer {self.counter_Destroyer}/2"
        self.draw_text( GRAY, txtDestr, 18, 16.5*block_size, 14*block_size)
        self.blit_surface((block_size*3, block_size), GREEN, 15*block_size, 14.5*block_size)
        sizDestr = "3 blocks"
        self.draw_text(GRAY, sizDestr, 16, 16.5 * block_size, 16*block_size)    
        txtSub = f"Sub {self.counter_Submarine}/3"
        self.draw_text( GRAY, txtSub, 18, 21*block_size, 14*block_size, 0)
        self.blit_surface((block_size*2, block_size), GREEN, 20*block_size, 14.5*block_size)
        sizSubm = "2 blocks"
        self.draw_text(GRAY, sizSubm, 16, 21 * block_size, 16*block_size)       
        txtPat = f"Patrol {self.counter_Patrol}/3"
        self.draw_text(GRAY, txtPat, 18, 24.5*block_size, 14*block_size)
        self.blit_surface((block_size*1, block_size), GREEN, 24*block_size, 14.5*block_size)
        sizPatrol = "1 block"
        self.draw_text(GRAY, sizPatrol, 16, 24.5 * block_size, 16*block_size)
        pygame.display.update()
    
    def update_counters(self):
        '''

        GRAPHIC
        This method is called each time a Ship is drawn onto the screen.
        It updates the images of the counters on the screen.
        '''   
        self.item.fill(pygame.Color("black"), (0, 13.1*block_size,screen_width,1.1*block_size))
        txtCarr = f"Aircraft carrier {self.counter_Aircraft}/1"
        txtBatt = f"Battleship {self.counter_Battleship}/1"
        txtDestr = f"Destroyer {self.counter_Destroyer}/2"
        txtSub = f"Sub {self.counter_Submarine}/3"
        txtPat = f"Patrol {self.counter_Patrol}/3"
        self.draw_text(GRAY, txtCarr, 18, 4.5*block_size, 14*block_size)
        self.draw_text( GRAY, txtBatt, 18, 11*block_size, 14*block_size)
        self.draw_text( GRAY, txtDestr, 18, 16.5*block_size, 14*block_size)
        self.draw_text( GRAY, txtSub, 18, 21*block_size, 14*block_size)
        self.draw_text( GRAY, txtPat, 18, 24.5*block_size, 14*block_size)
        pygame.display.update()

    def get_coord(self, a, b):
        """ 
        This method is used for translating, when it is possible, the coordinates of the mouse from the
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

    def insert_boat(self, Ship):
        """ 
        This method is used to draw the given Ship on the Board. It also calls Board.update_counters.
        In order to use this method the Ship must already have been passed together with its
        coordinates and whether it is vertical or not.

        Parameters
        ----------
        Ship: object
            the Ship instantiation to be blitted
        """
        Ship.coordinates=get_num_coord(Ship.grid_pos, bool(Ship.vertical), Ship.size)
        if self.located_boats.has == False: 
            self.item.blit(Ship.image, Ship.rect)
            self.located_boats.add(Ship)
            pygame.display.flip()         
        else:    
            for i in self.located_boats:              
                if pygame.sprite.collide_rect(i, Ship) == True and i is not Ship:
                    return
            for point in Ship.coordinates:
                for idx in range(len(self.occupied_shadow)):
                    if point in self.occupied_shadow[idx]:
                        return
            self.item.blit(Ship.image, Ship.rect)  
            self.located_boats.add(Ship)
            pygame.display.flip() 
        Ship.get_shadow()
        self.occupied_shadow.append(Ship.shadow)
        self.placed_ships.append([Ship.name, Ship.coordinates, Ship.life])
        for a in Ship.coordinates:
            self.occupied_positions.append(a)
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
        if self.counter_Aircraft == 1 and self.counter_Battleship == 1 and \
            self.counter_Destroyer == 2 and self.counter_Submarine == 3 and self.counter_Patrol == 3:
            self.item.fill(pygame.Color("black"), (0, 13.1 * block_size, screen_width, 4 * block_size))
            pygame.time.delay(600)
            text1 = "    YOUR TROOPS ARE READY    "
            self.draw_game_message(text1, GRAY)
            pygame.time.delay(900)
            self.item.fill(pygame.Color("black"), (0, 13.1 * block_size, screen_width, 4 * block_size))
            text2 = "  !!!     THE  WAR STARTS NOW      !!!  "
            self.draw_game_message(text2, DARK_RED)
            pygame.time.delay(900)
            self.item.fill(pygame.Color("black"), (0, 13.1 * block_size, screen_width, 4 * block_size))
            text3 = "          SHOOT, MY CAPTAIN          "
            self.draw_game_message(text3, GRAY)
          

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
        for y in range(block_size*2, block_size*14, block_size):            
            x = block_size*2
            pygame.draw.line(self.item, RED, (x, y), (x+440, y))
        for x in range(block_size*2, block_size*14, block_size): 
            y = block_size*2
            pygame.draw.line(self.item, RED, (x, y), (x, y+440))
        for ship in self.located_boats:
            self.item.blit(ship.image, ship.rect)
        pygame.display.flip()



    def mark_hit_cell(self, a, hit, random_hit):
        """ 
        This method is used for drawing a pointer (a red cross or a green block) on a given coordinate of
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

        x = return_x_val(a[0]) 
        y = return_y_val(a[1])
        text2 = "  !!!      YOU MISSED IT      !!!  "
        text1 = "  !!!      YOU HIT ONE      !!!  "
        text3 = "  !!!     YOU HAVE BEEN HIT, GET YOUR REVENGE     !!!  "
        text4 = "  !!!     YOU HAVE BEEN MISSED, TAKE THEIR HEAD    !!!  "
        if hit == False:
            self.hit_cells.append(a)  
            pygame.time.delay(300)
            self.item.fill(pygame.Color("black"), (0, 13.1*block_size,screen_width,4*block_size))
            self.draw_game_message(text2, GRAY)
            x = return_x_val(a[0])+ block_size 
            start_pos1 = (x, y)
            start_pos2 = (x, y + block_size)
            end_pos1 = (x + block_size, y + block_size)
            end_pos2 = (x + block_size, y)
            pygame.draw.line(self.item, (200,0,0), start_pos1, end_pos1, width=5)
            pygame.draw.line(self.item, (200,0,0), start_pos2, end_pos2, width=5)
            pygame.display.flip()
        elif hit == True:
            self.hit_cells.append(a)  
            pygame.time.delay(300)
            self.item.fill(pygame.Color("black"), (0, 13.1*block_size,screen_width,4*block_size))
            self.draw_game_message(text1, GREEN)
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
                self.draw_game_message(text3, RED)
                pygame.draw.line(self.item, RED, start_pos1, end_pos1, width=5)
                pygame.draw.line(self.item, RED, start_pos2, end_pos2, width=5)
                pygame.time.delay(300)
            else:
                self.draw_game_message(text4, GRAY)
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
        self.draw_text(BLACK, text, 50, screen_width//2, 2*block_size, flag=2)
        text0 = "DO YOU WANT TO PLAY AGAIN ?"
        text1 = "PLAY"
        text2 = "QUIT"
        text3 = "YOU SAVED THE PLANET"
        text4 = "YOU LOST, IT HAPPENS"
        self.draw_text( BLACK, text0, 30, screen_width//2, 330, flag=2)
        self.draw_text( BLACK, text1, 30, screen_width//2-6*block_size, 500, flag=2)
        self.draw_text( BLACK, text2, 30, screen_width//2+6*block_size, 500, flag=2)
        if win:
            self.draw_text(BLACK, text3, 40, screen_width//2, 5*block_size, flag=2)
        if not win:
            self.draw_text(BLACK, text4, 40, screen_width//2, 5*block_size, flag=2)       
        pygame.draw.line(self.item, BLACK, (screen_width//2 - 8.5*block_size, 490), (screen_width//2 - 3.5*block_size, 490))
        pygame.draw.line(self.item, BLACK, (screen_width//2 - 8.5*block_size, 535), (screen_width//2 - 3.5*block_size, 535))
        pygame.draw.line(self.item, BLACK, (screen_width//2 - 8.5*block_size, 535), (screen_width//2 - 8.5*block_size, 490))
        pygame.draw.line(self.item, BLACK, (screen_width//2 - 3.5*block_size, 490), (screen_width//2 - 3.5*block_size, 535))      
        pygame.draw.line(self.item, BLACK, (screen_width//2 + 3.5*block_size, 490), (screen_width//2 + 8.5*block_size,  490))
        pygame.draw.line(self.item, BLACK, (screen_width//2 + 3.5*block_size, 535), (screen_width//2 + 8.5*block_size,  535))
        pygame.draw.line(self.item, BLACK, (screen_width//2 + 3.5*block_size, 490), (screen_width//2 + 3.5*block_size, 535))
        pygame.draw.line(self.item, BLACK, (screen_width//2 + 8.5*block_size,  490), (screen_width//2 + 8.5*block_size, 535))
        pygame.display.update()

    def endScreen_restart(self, x_start, y_start):
        """"

         his method is called for checking whether the mouse input in the final menu page happens onto a button

        Arguments
         
        ----
        x_start:
            the x-position of the mouse input
        
        y_start:
            the y-position of the mouse input
        
        """
        if (x_start < screen_width // 2 - 3.5 * block_size) and (x_start > screen_width // 2 - 8.5 * block_size) and \
                (y_start < 535 and y_start > 490):
            return True
        if (y_start < 535 and y_start > 490) and (x_start > screen_width // 2 + 3.5) and \
                (x_start < screen_width // 2 + 8.5 * block_size):
            return False
        else:
            return None



