"""
This file contains the maze generation class
"""

import random
import numpy as np


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
        # To reduce number of loops, create a list that stores rows with
        # unvisited cells and delete the row once all cells are visited
        self.unvisited_rows = [x for x in range(0, self.num_rows)]
        self.unvisited_cols = [y for y in range(0, self.num_cols)]
        self.iterations = 0

    def mark_cell_visited(self, row: int, col: int):
        # 0 indicates no visit, and 1 means it has been visited
        self.maze[row, col, 0] = 1

    def update_relation_state(self, row: int, col: int,
                              direction: int, state: int):
        """This will update status between current cell and neighbor in
        specified direction"""

        def update_neighbor_relation(row: int, col: int, direction: int, state: int):
            # One way, update state in direction
            self.maze[row, col, direction] = state

        # Check for impossible assignments
        if (row == 0 and direction == NORTH) or \
           (col == self.num_cols - 1 and direction == EAST) or \
           (row == self.num_rows - 1 and direction == SOUTH) or \
           (col == 0 and direction == WEST):
            return

        # Update the relation in the current cell
        update_neighbor_relation(row, col, direction, state)
        # Update the relation in the neighbor cell
        update_neighbor_relation(
            *self.get_neighbor_coordinates(row, col,
                                           direction, True), 2)
        return

    def get_neighbor_coordinates(self, row: int, col: int, neighbor_direction: int,
                                 include_calling_cell_direction=False):
        """
        This function returns neighbor coordinates in a tuple of
        row, col. Tuple can include direction of calling cell if True
        """

        # Ensure neighbor exists in that direction
        if (row == 0 and neighbor_direction == NORTH) or \
                (row == self.num_rows - 1 and neighbor_direction == SOUTH) or \
                (col == 0 and neighbor_direction == WEST) or \
                (col == self.num_cols - 1 and neighbor_direction == EAST):
            return None

        # Find coordinates of neighbor in that direction
        if neighbor_direction == NORTH:
            if include_calling_cell_direction:
                calling_cell_direction = NORTH + 2
                return row - 1, col, calling_cell_direction
            return row - 1, col
        elif neighbor_direction == EAST:
            if include_calling_cell_direction:
                calling_cell_direction = EAST + 2
                return row, col + 1, calling_cell_direction
            return row, col + 1
        elif neighbor_direction == SOUTH:
            if include_calling_cell_direction:
                calling_cell_direction = SOUTH - 2
                return row + 1, col, calling_cell_direction
            return row + 1, col
        elif neighbor_direction == WEST:
            if include_calling_cell_direction:
                calling_cell_direction = WEST - 2
                return row, col - 1, calling_cell_direction
            return row, col - 1

    def get_unvisited_neighbor_direction(self, row: int, col: int):
        # Returns directions of unvisited neighbors in a list
        unvisited_list = []

        # Create a list of all neighbors
        for i in range(1, 5):
            if self.maze[row, col, i] == 1:
                neighbor_coordinates = self.get_neighbor_coordinates(row, col, i)
                if self.maze[(*neighbor_coordinates, 0)] == 0:
                    unvisited_list.append(i)

        if not unvisited_list:
            return None
        else:
            return random.choice(unvisited_list)

    """def get_num_connections(self, row: int, col: int):
        num_connections = 0
        for i in range(1, 5):
            if self.maze[(row, col, i)] == 2:
                num_connections += 1
        return num_connections"""

    def check_if_unvisited_cell_with_visited_neighbor(self, row: int, col: int):
        """
        This function first checks if current cell has been visited then checks if
        a neighbor that has been visited exists
        """
        if self.maze[row, col, 0] != 0:
            return False
        for direction in range(1, 5):
            n_coords = self.get_neighbor_coordinates(row, col, direction)
            if n_coords is None:
                continue
            if self.maze[(*n_coords, 0)] == 1:
                return direction
        return False

    def update_unvisited_axis(self):
        row_removal = []
        col_removal = []
        for row in self.unvisited_rows:
            if np.all(self.maze[row, :, 0] == 1):
                row_removal.append(row)
        for col in self.unvisited_cols:
            if np.all(self.maze[:, col, 0] == 1):
                col_removal.append(col)
        for row in row_removal:
            self.unvisited_rows.remove(row)
        for col in col_removal:
            self.unvisited_cols.remove(col)

    def generate_blank_maze(self):
        # Generates a grid represented by a 3D matrix
        for row in range(0, self.num_rows):
            for column in range(0, self.num_cols):
                if row < self.num_rows - 1:
                    self.maze[row, column, SOUTH] = 1
                if column < self.num_cols - 1:
                    self.maze[row, column, EAST] = 1
                if row > 0:
                    self.maze[row, column, NORTH] = 1
                if column > 0:
                    self.maze[row, column, WEST] = 1

    def inebriated_stroll(self, row, col):
        """
        This function starts at inputted cell, checks for unvisited neighbors,
        connects the two, and marks them both as visited. Program terminates
        when no unvisited cells are reachable
        """

        # Mark the current cell as visited
        self.mark_cell_visited(row, col)

        # Choose a random unvisited neighbor direction
        unv_neighbor = self.get_unvisited_neighbor_direction(row, col)

        # If no unvisited neighbors exist, return
        if not unv_neighbor:
            return

        # Connect the two cells together
        self.update_relation_state(row, col, unv_neighbor, 2)

        # Get coordinates of new connection and call function again
        unv_neighbor_coords = self.get_neighbor_coordinates(row, col, unv_neighbor)
        self.inebriated_stroll(*unv_neighbor_coords)

    def maze_iteration(self):
        if bool(random.getrandbits(1)):
            for row in self.unvisited_rows:
                if np.any(self.maze[row, :, 0] == 1):
                    for col in self.unvisited_cols:
                        hit = self.check_if_unvisited_cell_with_visited_neighbor(row, col)
                        if hit is False:
                            continue
                        self.update_relation_state(row, col, hit, 2)
                        self.inebriated_stroll(row, col)
                        return
        else:
            for col in self.unvisited_cols:
                if np.any(self.maze[:, col, 0] == 1):
                    for row in self.unvisited_rows:
                        hit = self.check_if_unvisited_cell_with_visited_neighbor(row, col)
                        if hit is False:
                            continue
                        self.update_relation_state(row, col, hit, 2)
                        self.inebriated_stroll(row, col)
                        return

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

        def get_random_cell():
            # Returns coordinates of a random cell
            rand_row = random.randint(0, self.num_rows - 1)
            rand_col = random.randint(0, self.num_cols - 1)
            return rand_row, rand_col

        # Start from a random cell
        if start:
            self.generate_blank_maze()
            self.inebriated_stroll(*get_random_cell())
            self.iterations += 1

        while True:
            self.update_unvisited_axis()
            if not self.unvisited_rows and not self.unvisited_cols:
                return
            self.iterations += 1
            self.maze_iteration()
