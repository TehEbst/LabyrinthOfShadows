"""
This file contains the maze generation function
"""

import random
import numpy

NORTH, EAST, SOUTH, WEST = 1, 2, 3, 4


class GenerateMaze:
    """
    This class uses the Hunt and Kill algorithm to generate a
    randomized maze. The maze is 2D but the numpy matrix it is stored
    in is 3D to hold cell information such as connections and presence
    of a neighbor. Each cell gives information about its four
    neighbors. A 0 means there is no neighbor, a 1 means that a
    neighbor exists in that direction, and a 2 means that the cell has
    a connection with the neighbor to that direction. The first index
    is to reserve whether the cell has been visited or not for maze
    building purposes.
    """

    def __init__(self, rows: int, cols: int):
        self.num_rows = rows
        self.num_cols = cols
        self.maze = np.zeros([self.num_rows, self.num_cols, 5], int)

    def hunt_and_kill(self, start=False):
        """
        This function implements the hunt and kill algorithm to
        generate a maze. It starts by calling the inebriated_stroll
        function once. Then it scans starting from the first cell until
        we reach a cell with a neighbor that has been visited. We
        connect those two cells and then initiate another inebriated
        stroll. We repeat this process until every cell has
        been visited
        """