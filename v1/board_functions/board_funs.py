import pygame

pygame.init()
pygame.font.init()

GRID_SIZE = 10

dictionary = {b"A":b"1", b"B":b"2", b"C":b"3", b"D":b"4", b"E":b"5", b"F":b"6", b"G":b"7", b"H":b"8", b"I":b"9", b"J":b"10"}
dictionary_opponent = {b"a":b"1", b"b":b"2", b"c":b"3", b"d":b"4", b"e":b"5", b"f":b"6", b"g":b"7", b"h":b"8", b"i":b"9", b"j":b"10"}
axes = [key for key in dictionary]
block_size=40


def return_x_val(x):
    """ The function returns the x-coordinates necessary to position a ship on the Pygame display given
    an input as the uppercase string character standing for the column label.

    Parameters
    ----------
    x: str
        an uppercase/lowercase letter depending on whether it is the Player or the Opponent, identifying the column
        of the board

    Returns
    -------
    x_val: int
        the magnitude of the x-coordinates on the Pygame display
    """
    if x.isupper():
        x_val = (int(dictionary[x]) + 2)*block_size
        return x_val
    else:
        x_val = (int(dictionary_opponent[x]) + 14)*block_size
        return x_val

def return_y_val(x):
    """ The function returns the y-coordinates necessary to position a ship on the Pygame display given
    an integer input.

    Parameters
    ----------
    x: int
        the integer value standing as the row label

    Returns
    -------
    y_val: int
        the magnitude of the y-coordinates on the Pygame display
    """
    y_val = (int(x) + 2)*block_size
    return y_val

def get_num_coord(coord, vert, length):
    """ This function is used for translating the placement of the Ship on the board into a numpy array representation
    which is needed for the logical flow of the game.

    Parameters
    ----------
    coord: list
        list of the coordinates of the Ship.
        it retrieves the information from the Ship.set_gridpos method to capture the first cell in which the Ship is placed
    vert: bool
        boolean value representing whether the Ship is vertical or not
    length: int
        attribute storing the length of the Ship

    Returns
    -------
    a: list
        list of coordinates of the placed Ship converted into value positional argument to identify the entry
        of a numpy matrix
    """
    key = [key for key in dictionary.keys()]
    value = [value for value in dictionary.values()]
    a = [[]]
    for v in value:
        if int(v) == coord[1]:
            a[0].append(value.index(v))
    for k in key:
        if k == bytes(coord[0], encoding='utf-8'):
            a[0].append(key.index(k))
    if length == 1:
        return a
    else:
        if vert == True:
            for i in range(1, length):
                b = a[0][0] + i
                v = [b, a[0][1]]
                a.append(v)
            return a
        else:
            for i in range(1, length):
                b = a[0][1] + i
                v = [a[0][0], b]
                a.append(v)
            return a

def get_num_coord_opp(coord):
    """ This function is the equivalent to get_num_coord but is used for the shoot-get_shot phase (and not
    for the insertion one). In addition, we are sure we are dealing with a single square of the table and not
    multiple ones (as in the case of the ship insertion) and this leads to changes in the function.
    It is used for translating the placement of a shot onto the opponent's board
    into a row-column index pair to be used to query the numpy matrix board.

    Parameters
    ----------
    coord: list
        list of the matrix coordinates of the shot (coordinates on the Pygame surface).
        it retrieves the information from the Board.get_coord method to capture the first cell in which the shot is placed

    Returns
    -------
    a: list
        list of coordinates of the placed shot converted into value positional argument to identify the entry
        of a numpy matrix
    """
    key = [key.lower() for key in dictionary.keys()]
    value = [int(value) for value in dictionary.values()]
    a = []
    for v in value:
        if v == coord[1]:
            a.append(value.index(v))
    for k in key: 
        if k == coord[0]:
            a.append(key.index(k))            
    return a


def draw_text(surf, color, text, size, x, y):
    """ This method is an help function for the insertion of text string on the Pygame surface.
    It returns the graphical representation of the text across the iterations of the main
    loop

    Parameters
    ----------
    surf: Pygame surface
        the main Pygame display is passed as an argument to blit the text
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
    ## selecting a cross platform font to display the score
    font = pygame.font.Font('freesansbold.ttf', size)
    text_surface = font.render(text, True, color)       ## True denotes the font to be anti-aliased
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def pairwise_elements(l):
    """ The function takes as input a list consisting of pygame.events MOUSEBUTTONDOWN and MOUSEBUTTONUP (once
    validated only if taking place inside the actual space devoted to the board) and returns a list of lists
    which successfully pairs all the elements. This function is necessary as a pair in fact stands for a Ship
    to be drawn on the screen.

    Parameters
    ----------
    l: list
        a list consisting of the coordinates of all pygame.events MOUSEBUTTONDOWN and MOUSEBUTTONUP gathered
        at that point in the loop

    Returns
    -------
    couples: list
        list of lists whose i entry consists of a list consisting of two members (i.e. a pair formed)
    """
    couples = []
    if len(l)%2 != 0:
        return couples
    for i in range(0, len(l), 2):
        a = [l[i], l[i+1]]
        couples.append(a)
    return couples



