# AI Model

## Justin

Implemented alpha-beta pruning, completely independently of the underlying implementation. As long as the state itself is an object and there exists a function actions() and results() which when the game state is input, produce the actions possible, and a results function, that when a state and action are input produce an output, this fill function. It also needs to be able to take actions on a copy of the board.

State refers to the current game information.

Is considered the maximizing player, means it plays on the board as 1.

# Game Loop

## Justin

Implemented a basic game loop. Takes the user's text input to place a token on the board (-1). Then takes the output of the model as to its next action, and plays that move. The game ends when it is won (need to add ending on a tie, but that's simple).

## Sampada

Haven't implemented a game loop, but have created functions to accept the player's (AI or User) input. The input is used to update the board and calculate the current state of the game (Win / Draw / Lose). 
The game is won if any player has 4 in a row vertically or horizontally in each layer, or diagonally (top left --> bottom right or top right --> bottom left) and straight down across all 3 layers. I just realized I don't have logic to check for 4 in a row digonally in each layer, but that can be easily added. 
The game is tied if all moves have been made and no player has won, i.e. board has no empty spaces left and game is still in progress.
No player can make a move in a position that is not empty, this results in an error.

## Bianca

Implemented function for user input, along with the AI's response (in my case a random int function). The users move is based on the number of the desired spot on the board according to 1-16 (n-1). if the user or AI have placed their mark on a spot then the program will return an error "player has already placed mark here." I have logic for wins horizontally, vertically and diagonally.

# Game Information (Board)

## Justin

Implemented a game state, which can be copied, has a placeholder heuristic function, and the ability to track a win (ties would be simple to add with a linear search for a 0 (no token). Some quick work should make the win function not have as many duplicates, which do currently show up. The method would also make the function more legible, brief, and efficient, I just didn't think about it while implementing. I'll try to have this done before merge in case we go with this option.

## Sampada

The game board is implemented as a `3 x 4 x 4` 3D array. Its values represent all turns taken by players up to any point in time. 
The game state is In Progress until either a Win or Draw situation occurs.

## Bianca

Game borad is 4x4, I have not implemented the '3D aspect to the board for player use. It seems like I can add the logic seperately but I am afraid of have redundant and repetitive code to the board implementation.
