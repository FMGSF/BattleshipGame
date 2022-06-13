import pygame
from board_functions.board_funs import *

GRAY = (200,200,200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_RED = (180, 0, 0)
WHITE = (255,255,255)
BLUE = (0,0,255)
BLACK = (0, 0, 0)

block_size = 40
pygame.init()
pygame.font.init()

dictionary = {b"A":b"1", b"B":b"2", b"C":b"3", b"D":b"4", b"E":b"5", b"F":b"6", b"G":b"7", b"H":b"8", b"I":b"9", b"J":b"10"}
dictionary_opponent = {b"a":b"1", b"b":b"2", b"c":b"3", b"d":b"4", b"e":b"5", b"f":b"6", b"g":b"7", b"h":b"8", b"i":b"9", b"j":b"10"}


class Ship(pygame.sprite.Sprite):
    """ The Ship class is the graphical representation of the concept of Ship on the board.
    The Ship is conceived as a attribute of the class Player in a precise number depending on the size (and the number
    of lives) of the Ship, for a total number of 10 ships per player.

    Parameters
    ----------
    ship_size: int
        attribute variable representing the length of the Ship (with board squares as unit of measure)

    Attributes
    ----------
    image: pygame.Surface
        definition of the image attribute of the pygame.sprite object, which will be a surface object
        it is a square in this version
    rect: pygame object
        rectangular coordinates of the ship object
    dead: bool
        a value set to False until the remaining lives of the instance of Ship arrive to 0
    size: int
        an attribute storing the length of the Ship
    life: int
        an attribute storing the number of lives available to each Ship, which is at first set equal
        to the size and then automatically updated whenever the Ship is hit
    name: str
        the attribute storing the name of the Ship, used to uniquely identify the type of the Ship
        and automatically generated whenever a Ship is placed
    """
    def __init__(self, ship_size):
        pygame.sprite.Sprite.__init__(self) # initialize the instance of the pygame.sprite.Sprite object (parent)
        self.image = pygame.Surface((block_size, block_size*ship_size))
        self.image.fill(GREEN) # fill it with a gorgeous green
        self.rect = self.image.get_rect()
        self.life = ship_size
        self.size = ship_size
        self.name = "Ship"
        self.coordinates = []

    def set_gridpos(self, grid_pos):
        """
        This method is used for setting up the rect coordinates and the dimensions of the Ship

        Parameters
        ----------
        grid_pos: list
            list of the coordinates of the Ship (the first entry)

        Returns
        -------
        Referencing the dictionary of the coordinates, the attribute vertical and the Ship.size attribute we create
        the rectangular coordinates of the Pygame.sprite.object (Ship)
        """
        self.grid_pos = grid_pos
        self.coordinates = get_num_coord(self.grid_pos, bool(self.vertical), self.size)
        self.x = return_x_val(bytes(self.grid_pos[0].upper(), encoding="utf-8")) 
        self.y = return_y_val(self.grid_pos[1]) 
        self.rect.x = self.x 
        self.rect.y = self.y 
        if self.vertical == False: 
            self.image = pygame.Surface((block_size*self.size, block_size))
        else:
            self.image = pygame.Surface((block_size, block_size * self.size))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        x = self.x
        y = self.y
        self.rect.x = x
        self.rect.y = y
        self.x = self.rect.x
        self.y = self.rect.y
        del x, y

    def get_shadow(self):
        """
        This method is called whenever a Ship is placed in order to initialize the shadow attribute
        of each ship, which gathers all the board indexes that are adjacent to the placed ship. This
        attribute is then stored in the occupied_shadow attribute of the board associated with Player.
        """
        self.shadow = []
        self.start_row = self.coordinates[0][0]
        self.start_col = self.coordinates[0][1]
        self.end_row = self.coordinates[-1][0]
        self.end_col = self.coordinates[-1][1]
        if self.size == 1:
            for i in range(self.start_row - 1, self.start_row + 2):
                for j in range(self.start_col - 1, self.start_col + 2):
                    self.shadow.append([i, j])
            self.shadow.remove([self.start_row, self.start_col])
        else:
            if self.vertical == False:
                for i in range(self.start_row - 1, self.start_row + 2):
                    for j in range(self.start_col - 1, self.end_col + 2):
                        self.shadow.append([i, j])
                for occupied in self.coordinates:
                    self.shadow.remove(occupied)
            if self.vertical == True:
                for i in range(self.start_col - 1, self.start_col + 2):
                    for j in range(self.start_row - 1, self.end_row + 2):
                        self.shadow.append([j, i])
                for occupied in self.coordinates:
                    self.shadow.remove(occupied)

class AircraftCarrier(Ship):
    """
    Child class of Ship representing the longest Ship, with size 5 (only one quantity available to each Player)
    """
    def __init__(self, ship_size = 5):
        super().__init__(ship_size)
        self.name = 'Aircraft Carrier'

class Battleship(Ship):
    """
    Child class of Ship representing the Ship with size 4 (only one quantity available to each Player)
    """
    def __init__(self, ship_size = 4):
        super().__init__(ship_size)
        self.name = 'Battleship'
        
class Destroyer(Ship):
    """
    Child class of Ship representing the Ship with size 3 (two available to each Player)
    """
    def __init__(self, ship_size = 3):
        super().__init__(ship_size)
        self.name = 'Destroyer'

class Submarine(Ship):
    """
    Child class of Ship representing the Ship with size 2 (three available to each Player)
    """
    def __init__(self, ship_size = 2):
        super().__init__(ship_size)
        self.name = 'Submarine'

class PatrolBoat(Ship):
    """
    Child class of Ship representing the Ship with size 1 (three available to each Player)
    """
    def __init__(self, ship_size = 1):
        super().__init__(ship_size)
        self.name = 'Patrol'
