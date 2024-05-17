import pygame
from maze_generation import GenerateMaze

NORTH, EAST, SOUTH, WEST = 1, 2, 3, 4
DIRECTIONS = [NORTH, EAST, SOUTH, WEST]
clrs = {"Elephant": (92, 75, 81),
          "Blue": (140, 190, 178),
          "Cream": (242, 235, 191),
          "Orange": (243, 181, 98),
          "Red": (240, 96, 96),
          "White": (250, 250, 250),
          "Black": (0, 0, 0)}

# Initialize the pygame library
pygame.init()

# Set up the opening screen
SCREEN = pygame.display.set_mode([500, 500])
pygame.display.set_caption("Menu")

def main_menu():
    running = True
    while running:
        # Put the background
        SCREEN.fill(clrs["Black"])
        pygame.display.update()

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the display
        pygame.display.update()


main_menu()
