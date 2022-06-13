import pygame
import numpy as np

from shps.ships import *
from brd.board  import *

GRID_SIZE = 10

pygame.init()
pygame.font.init()

dictionary={b"A":b"1", b"B":b"2", b"C":b"3", b"D":b"4", b"E":b"5", b"F":b"6", b"G":b"7", b"H":b"8", b"I":b"9", b"J":b"10"}

class Player(object):
    """
     The Player class is one of the two players of a classic battleship game on one own.
    It stores all the necessary identifier of the player which are constantly updated during the game, together
    with the main functions for placing and calling the shots to be alternated with the one of the subclass Random(Player).
    Each player is endowed with 10 ships of varying dimensions and a 10x10 board matrix.

    Attributes
    -------
    boats_list: list
        list of the available Ships
    boats: Pygame Group
        attribute containing all the Ships (as Pygame objects)
    own_board: object
        personal instantiation of Board object for Player
    hit_cells: list
        list containing the coordinates (row and column indexes) of the hit cells
    number_ships_sunk: int
        the variable responsible for ending the main loop of the game, whenever the number of ships sunk of a
        certain player is equivalent to the total number of ships available (10).
        it is based on the previous one, since number_ships_sunk increases by 1 every time the remaining lives of
        one of the ships stored in placed_ships go to 0.
    """

    def __init__(self):
        self.aircraft_carrier = AircraftCarrier()
        self.battle_ship1 = Battleship()
        self.destroyer1 = Destroyer(); self.destroyer2 = Destroyer()
        self.submarine1 = Submarine(); self.submarine2 = Submarine(); self.submarine3 = Submarine()
        self.patrol1 = PatrolBoat(); self.patrol2 = PatrolBoat(); self.patrol3 = PatrolBoat()
        self.boats_list = [self.aircraft_carrier, self.battle_ship1, self.destroyer1, self.destroyer2, self.submarine1,
                         self.submarine2, self.submarine3, self.patrol1, self.patrol2, self.patrol3]
        self.own_board = Board()
        self.boats = pygame.sprite.Group()
        self.boats.add(self.boats_list)
        self.hit_cells = []
        self.number_ships_sunk = 0

    def reset(self):
        self.own_board.clear()
        self.own_board.draw_screen_game()
        self.placed_ships = []
        self.boats.add(self.boats_list)
        self.hit_cells = []
        self.number_ships_sunk = 0

class Player_(object):
    """ 
    The Player class is one of the two players of a classic battleship game on one own.
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
    def __init__(self):  
        self.number_ships = 10
        self.board = np.zeros((10,10), dtype=int)
        self.available_ships = ["AircraftCarrier", "Battleship", "Destroyer", "Destroyer", "Submarine",
                                "Submarine", "Submarine", "PatrolBoat", "PatrolBoat", "PatrolBoat"]
        self.available_ships_sizes = [AircraftCarrier().size, Battleship().size, Destroyer().size, Destroyer().size,
                                      Submarine().size, Submarine().size, Submarine().size,
                                      PatrolBoat().size, PatrolBoat().size, PatrolBoat().size]
        self.occupied_positions = []
        self.placed_ships = []
        self.number_ships_sunk = 0  
    def reset(self):
        self.number_ships = 10
        self.own_board = np.zeros((10, 10))
        self.available_ships = ["AircraftCarrier", "Battleship", "Destroyer", "Destroyer", "Submarine",
                                "Submarine", "Submarine", "Patrol", "Patrol", "Patrol"]
        self.available_ships_sizes = [5, 4, 3,
                                      3, 2, 2,
                                      2, 1, 1, 1]
        self.occupied_positions = []
        self.placed_ships = []
        self.number_ships_sunk = 0