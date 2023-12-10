import pygame
import sys
import random
import game

# Current game state
thisGame = None

# Initializing game
pygame.init()

# Constants for te GUI
WIDTH, HEIGHT = 900, 900  # 1004, 1004  # Square window size
GRID_ROWS, GRID_COLS, GRID_LAYERS = 4, 4, 4  # 4x4 grid on 4 layers
GRID_SIZE = 50  # Size of each grid cell
PERSPECTIVE_OFFSET_X = 25  # Horizontal offset for 3D effect
PERSPECTIVE_OFFSET_Y = GRID_SIZE // 2  # Vertical offset for 3D effect
CIRCLE_RADIUS = int(GRID_SIZE // 5)
CROSS_SIZE = CIRCLE_RADIUS  # Size of the 'X' is the same as the circle

#### Start of Constants for Level Selector Button and End game Button ####

# Difficulty levels and their corresponding depths
DIFFICULTY_LEVELS = {"easy": 2, "difficult": 4, "insane": 6}

# RGB Colors for the application
BG_COLOR = (0, 0, 0)  # Black background
LINE_COLOR = (0, 255, 0)  # Green grid
CIRCLE_COLOR = (255, 0, 0)  # Red circles for human player
CROSS_COLOR = (0, 0, 255)  # Blue 'X' for the AI player

# Colors for buttons
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)
TEXT_COLOR = (255, 255, 255)

# Font for button text
pygame.font.init()
FONT = pygame.font.SysFont("Arial", 24)
#### End of Constants for Level Selector Button and End game buttons####


# Setup the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Tic Tac Toe")


# Function to draw difficulty buttons
def draw_buttons():
    buttons = {}  # Dictionary to hold button
    # Iterate over difficulty levels
    for index, (level, depth) in enumerate(DIFFICULTY_LEVELS.items()):
        # Set the x, y, width, and height for the button
        button_x = WIDTH // 4  # Position the button horizontally centered
        button_y = HEIGHT // 3 + (
            index * 50
        )  # Position the button vertically based on its index
        button_w = WIDTH // 2  # Width of the button
        button_h = 40  # Height of the button

        # Create a rectangle for the button
        button_rect = pygame.Rect(button_x, button_y, button_w, button_h)
        # Draw the rectangle on the screen with the default button color
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
        # Get poistion
        mouse_pos = pygame.mouse.get_pos()
        # Change the button color if the mouse hovering over it
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)

        # Render the text for the button with the difficulty level and depth
        text_surface = FONT.render(
            f"{level.capitalize()} (Depth {depth})", True, TEXT_COLOR
        )
        # draw the text on the button
        screen.blit(text_surface, (button_x + 10, button_y + 5))

        # Store the button's rectangle in the buttons dictionary for click detection
        buttons[level] = button_rect

    return buttons


# Function to draw the 'Replay' and 'Quit' buttons and the outcome message
def draw_end_game_buttons_and_message(winner):
    message = f"{winner} has won!" if winner != "Tie" else "It's a tie!"

    # Display the outcome message
    message_surface = FONT.render(message, True, TEXT_COLOR)
    screen.blit(message_surface, (WIDTH // 2 - 100, HEIGHT // 3))

    # Buttons
    replay_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 100, 50)
    quit_button = pygame.Rect(WIDTH // 2 + 50, HEIGHT // 2, 100, 50)

    # Draw 'Replay' button
    pygame.draw.rect(screen, BUTTON_COLOR, replay_button)
    replay_text = FONT.render("Replay", True, TEXT_COLOR)
    screen.blit(replay_text, (replay_button.x + 20, replay_button.y + 15))

    # Draw 'Quit' button
    pygame.draw.rect(screen, BUTTON_COLOR, quit_button)
    quit_text = FONT.render("Quit", True, TEXT_COLOR)
    screen.blit(quit_text, (quit_button.x + 20, quit_button.y + 15))

    return replay_button, quit_button


# Function to check for button clicks
def check_button_clicks(pos, buttons):
    # Iterate over the buttons
    for level, rect in buttons.items():
        # Check if the provided position is within the button
        if rect.collidepoint(pos):
            return level  # Return the difficulty level
    return None


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


# Function to draw circles and X
def draw_marks():
    board_state = thisGame.gameState.getState()

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
                if board_state[layer][row][col] == game.Token.PLAYER.value:
                    pygame.draw.circle(
                        screen, CIRCLE_COLOR, (center_x, center_y), CIRCLE_RADIUS
                    )
                # If the slot contains the AI's mark, draw a blue 'X'
                elif board_state[layer][row][col] == game.Token.AI.value:
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
    board_state = thisGame.gameState.getState()

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
                    thisGame.gameState.play(layer, row, col, game.Token.PLAYER)
                    return True  # A circle placed
    return False  # No circle placed


# Function for the AI to make a move
def ai_make_move():
    currState = thisGame.gameState
    layer, row, col = thisGame.aiPlayer.alphaBetaSearch(currState)
    thisGame.gameState.play(layer, row, col, game.Token.AI)


# end ai_make_move


def winFound():
    winTuple = thisGame.gameState.isWin()
    winner = ""
    if winTuple[1] == -1:  # Player is min player
        winner = "Player"
    elif winTuple[1] == 1:  # AI is max player
        winner = "AI"
    elif winTuple[0]:  # Tie is a win with no winner.
        winner = "Tie"
    # end if/elif

    if winner != "":
        if winner != "Tie":
            print(winner + " has won!")
        else:
            print("It's a tie!")
        # end if/else
    # end if

    return winTuple[0]


# end winFound


# Main game loop
def gameLoop():
    global thisGame

    running = True
    waiting_for_difficulty = True
    buttons = None  # To store buttons for difficulty selection
    game_over = False
    winner = None  # To store the winner

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # This section of game_over check is  for handling the end-of-game scenario where it's necessary to determine the PLAYER interaction with the Replay and Quit buttons.
            if game_over:
                # Draw the end game buttons and message only if game is over
                replay_button, quit_button = draw_end_game_buttons_and_message(winner)
                # Handle end game scenario
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if replay_button.collidepoint(mouse_pos):
                        # Resetting the game state for replay
                        thisGame = game.Game(thisGame.aiPlayer.maxLayers)
                        game_over = False
                        waiting_for_difficulty = True
                        break  # Break out of the event loop to resTART the game
                    elif quit_button.collidepoint(mouse_pos):
                        running = False
                        break  # Exit BOTH event loop and the game loop

            elif event.type == pygame.MOUSEBUTTONDOWN and waiting_for_difficulty:
                # Check if a difficulty button was clicked
                level = check_button_clicks(event.pos, buttons)
                if level:
                    maxDepth = DIFFICULTY_LEVELS[level]
                    thisGame = game.Game(maxDepth)
                    waiting_for_difficulty = (
                        False  # Difficulty selected, start the game
                    )
                # end if

            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                # If the player clicks and a circle is placed
                player_moved = handle_mouse_click(event.pos)
                if player_moved:
                    # Check if the player's move resulted in a win
                    if winFound():
                        game_over = True
                        winner = "Player"
                        continue  # Skip to the end of game handling
                    # end if

                    ai_make_move()  # AI makes a move after the player

                    # Check if the AI's move resulted in a win
                    if winFound():
                        game_over = True
                        winner = "AI"
                        continue  # Skip to the end of game handling

            # Redraw the screen based on the current state of the Game
            screen.fill(BG_COLOR)
            if waiting_for_difficulty:
                # Draw buttons if waiting for difficulty selection
                buttons = draw_buttons()
            elif game_over:
                # Draw the end game buttons and message
                replay_button, quit_button = draw_end_game_buttons_and_message(winner)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if replay_button.collidepoint(mouse_pos):
                            # Reset the game state and restart
                            thisGame = game.Game(thisGame.aiPlayer.maxLayers)
                            game_over = False
                            waiting_for_difficulty = (
                                True  # Reset to difficulty selection
                            )
                        elif quit_button.collidepoint(mouse_pos):
                            # Quit the game
                            running = False
            else:
                # Draw the game layers and marks
                draw_layers()
                draw_marks()

            pygame.display.flip()


# end gameLoop

gameLoop()
sys.exit()