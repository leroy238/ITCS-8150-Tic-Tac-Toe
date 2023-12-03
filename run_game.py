import pygame
import sys
import random
import game

# InitializINg game
pygame.init()

# Constants for te GUI
WIDTH, HEIGHT = 1004, 1004  # Square window size
GRID_ROWS, GRID_COLS, GRID_LAYERS = 4, 4, 4  # 4x4 grid on 4 layers
GRID_SIZE = 50  # Size of each grid cell
PERSPECTIVE_OFFSET_X = 25  # Horizontal offset for 3D effect
PERSPECTIVE_OFFSET_Y = GRID_SIZE // 2  # Vertical offset for 3D effect
CIRCLE_RADIUS = int(GRID_SIZE // 5)
CROSS_SIZE = CIRCLE_RADIUS  # Size of the 'X' is the same as the circle

# RGB Colors for the application
BG_COLOR = (0, 0, 0)  # Black background
LINE_COLOR = (0, 255, 0)  # Green grid
CIRCLE_COLOR = (255, 0, 0)  # Red circles for human player
CROSS_COLOR = (0, 0, 255)  # Blue 'X' for the AI player

# Setup the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Tic Tac Toe")

# Initialize the board state with 0 (empty), 1 (human player's circle), 2 (AI's 'X')
board_state = [
    [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    for _ in range(GRID_LAYERS)
]


# Function to draw all four layers
def draw_layers():
    # Iterate over each layer to draw it
    for layer in range(GRID_LAYERS):
        # Calculate the top-left origin of each layer, shifted for 3D effect
        origin_x = WIDTH // 2 - GRID_SIZE * 2 - layer * PERSPECTIVE_OFFSET_X
        origin_y = layer * (GRID_SIZE * GRID_ROWS + PERSPECTIVE_OFFSET_Y)

        # Draw horizontal grid lines for the current layer
        for row in range(GRID_ROWS + 1):
            # Calculate starting point of the horizontal line based on row number
            start_pos = (
                origin_x
                + PERSPECTIVE_OFFSET_X * row,  # Shift to the right for perspective
                origin_y + GRID_SIZE * row,  # Shift down based on row number
            )
            # Calculate ending point of the horizontal line
            end_pos = (
                origin_x
                + GRID_SIZE * GRID_COLS
                + PERSPECTIVE_OFFSET_X * row,  # Shift to the right, end of row
                origin_y + GRID_SIZE * row,  # Stay on the same horizontal level
            )
            # Draw a green line between the start and end points
            pygame.draw.line(screen, LINE_COLOR, start_pos, end_pos)

        # Draw vertical grid lines for the current layer
        for col in range(GRID_COLS + 1):
            # Calculate starting point of the vertical line based on column number
            start_pos = (
                origin_x + GRID_SIZE * col,  # Shift to the right based on column number
                origin_y,  # Start at the top of the current layer
            )
            # Calculate ending point of the vertical line
            end_pos = (
                origin_x
                + GRID_SIZE * col
                + PERSPECTIVE_OFFSET_X
                * GRID_ROWS,  # Shift to the right for perspective
                origin_y + GRID_SIZE * GRID_ROWS,  # Shift down, end of column
            )
            # Draw a green line between the start and end points
            pygame.draw.line(screen, LINE_COLOR, start_pos, end_pos)


# Function to draw circles and 'X's based on the board state
def draw_marks():
    # Iterate over each layer, row, and column to draw marks
    for layer in range(GRID_LAYERS):
        # Calculate the origin for the marks on the current layer
        origin_x = WIDTH // 2 - GRID_SIZE * 2 - layer * PERSPECTIVE_OFFSET_X
        origin_y = layer * (GRID_SIZE * GRID_ROWS + PERSPECTIVE_OFFSET_Y)

        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                # Calculate the center position for the mark
                center_x = (
                    origin_x
                    + col * GRID_SIZE
                    + GRID_SIZE // 2
                    + PERSPECTIVE_OFFSET_X * row
                )
                center_y = origin_y + row * GRID_SIZE + GRID_SIZE // 2
                # If the slot contains the human player's mark, draw a red circle
                if board_state[layer][row][col] == 1:
                    pygame.draw.circle(
                        screen, CIRCLE_COLOR, (center_x, center_y), CIRCLE_RADIUS
                    )
                # If the slot contains the AI's mark, draw a blue 'X'
                elif board_state[layer][row][col] == 2:
                    # Draw one diagonal line of the 'X'
                    pygame.draw.line(
                        screen,
                        CROSS_COLOR,
                        (center_x - CROSS_SIZE, center_y - CROSS_SIZE),
                        (center_x + CROSS_SIZE, center_y + CROSS_SIZE),
                        2,
                    )
                    # Draw the other diagonal line of the 'X'
                    pygame.draw.line(
                        screen,
                        CROSS_COLOR,
                        (center_x + CROSS_SIZE, center_y - CROSS_SIZE),
                        (center_x - CROSS_SIZE, center_y + CROSS_SIZE),
                        2,
                    )


# Function to handle mouse clicks when  the human player click or scooll mouse3
def handle_mouse_click(pos):
    # Iterate over all slots to check for the clicked position
    for layer in range(GRID_LAYERS):
        origin_x = WIDTH // 2 - GRID_SIZE * 2 - layer * PERSPECTIVE_OFFSET_X
        origin_y = layer * (GRID_SIZE * GRID_ROWS + PERSPECTIVE_OFFSET_Y)
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                # Define the rectangle for the current slot
                rect_x = origin_x + col * GRID_SIZE + PERSPECTIVE_OFFSET_X * row
                rect_y = origin_y + row * GRID_SIZE
                slot_rect = pygame.Rect(rect_x, rect_y, GRID_SIZE, GRID_SIZE)
                # If the click is within the slot and it's empty, mark it with a circle
                if slot_rect.collidepoint(pos) and board_state[layer][row][col] == 0:
                    
                    board_state[layer][row][col] = 1
                    thisGame.gameState.play(layer, row, col, game.Token.PLAYER)
                    return True  # A circle placed
    return False  # No circle placed


# Function for the AI to make a move
def ai_make_move():
    # createtr a list of all empty slots l-layer r- row  c- column
    empty_slots = [
        (l, r, c)
        for l in range(GRID_LAYERS)
        for r in range(GRID_ROWS)
        for c in range(GRID_COLS)
        if board_state[l][r][c] == 0
    ]
    # If there are empty slots, choose one at random and mark it with an 'X'
    if empty_slots:
        currState = thisGame.gameState
        layer, row, col = thisGame.aiPlayer.alphaBetaSearch(currState)#random.choice(empty_slots)
        thisGame.gameState.play(layer, row, col, game.Token.AI)
        board_state[layer][row][col] = 2  # Mark the slot with an 'X'


# Main game loop
running = True
thisGame = game.Game(2) #TODO: Put maxDepth here
# thisGame.run()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the player clicks and a circle is placed
            player_moved = handle_mouse_click(event.pos)
            if player_moved:
                ai_make_move()  # AI makes THE move after the player
                # Redraw the screen with the new marks
                screen.fill(BG_COLOR)
                draw_layers()
                draw_marks()
                pygame.display.flip()
                
                winTuple = thisGame.gameState.isWin()
                winner = ''
                if winTuple[1] == 1:
                    winner = 'Player'
                else:
                    winner = 'AI'
                if winner != '':
                    print(winner + 'has won!')
                    running = False

    # Draw the initial game state if the game is still running
    if running:
        screen.fill(BG_COLOR)
        draw_layers()
        draw_marks()
        pygame.display.flip()

# Quit the game when the main loop ends
pygame.quit()
sys.exit()
