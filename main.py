# Importing the required modules
import pygame
import sys
import numpy as np

# Initializes pygame
pygame.init()

# Constants defining the window size, the number of rows and columns on the board, and the size of each square
WIDTH, HEIGHT = 600, 600
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS

# Colors (changed for a different color scheme)
BG_COLOR = (255, 0, 0)  # Dark background color
LINE_COLOR = (15, 15, 15)  # Color for the grid lines
CIRCLE_COLOR = (239, 231, 200)  # Light color for the circle
CROSS_COLOR = (66, 66, 66)  # Dark color for the cross

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE')
screen.fill(BG_COLOR)

# Board setup (3x3 grid initialized to zeros)
board = np.zeros((BOARD_ROWS, BOARD_COLS))

# Function to draw the grid lines on the board


def draw_lines():
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row *
                         SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), 2)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE,
                         0), (col * SQUARE_SIZE, HEIGHT), 2)


# Function to draw circles and crosses on the board


def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            # Check if the current cell is marked with a 1 (player 1)
            if board[row][col] == 1:  # Draw circles for player 1
                # - Draw the circle using the calculated center, a predefined radius, and line thickness
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(
                    # int part refert to x,y cord for the circle, 100->Radius , 15-> Thickness
                    col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), 100, 15)
            elif board[row][col] == 2:  # Draw crosses for player 2
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + 50, row * SQUARE_SIZE + 50),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - 50, row * SQUARE_SIZE + SQUARE_SIZE - 50), 25)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + 50, row * SQUARE_SIZE +
                                 SQUARE_SIZE - 50), (col * SQUARE_SIZE + SQUARE_SIZE - 50, row * SQUARE_SIZE + 50), 25)


# Main game loop
game_over = False
player = 1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Allows exiting the game
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:  # Handle mouse clicks
            mouseX = event.pos[0]  # X position of the mouse click
            mouseY = event.pos[1]  # Y position of the mouse click

            clicked_row = mouseY // SQUARE_SIZE  # Translate click to grid row
            clicked_col = mouseX // SQUARE_SIZE  # Translate click to grid column

            # Check if the clicked square is empty
            if board[clicked_row][clicked_col] == 0:
                # Mark the square for the current player
                board[clicked_row][clicked_col] = player
                player = player % 2 + 1  # Switch turns between player 1 and 2

            # Clear the screen and redraw the grid and figures every frame
            # Clear the screen by filling it with the background color
            screen.fill(BG_COLOR)
            draw_lines()  # Draw the grid lines on the board, including the border lines
            draw_figures()  # Draw the figures on the board

    # Refresh the game display
    pygame.display.update()
