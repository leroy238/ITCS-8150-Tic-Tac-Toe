# AI Model

## Justin

Implemented alpha-beta pruning, completely independently of the underlying implementation. As long as the state itself is an object and there exists a function actions() and results() which when the game state is input, produce the actions possible, and a results function, that when a state and action are input produce an output, this fill function. It also needs to be able to take actions on a copy of the board.

State refers to the current game information.

Is considered the maximizing player, means it plays on the board as 1.

# Game Loop

## Justin

Implemented a basic game loop. Takes the user's text input to place a token on the board (-1). Then takes the output of the model as to its next action, and plays that move. The game ends when it is won (need to add ending on a tie, but that's simple).

# Game Information (Board)

## Justin

Implemented a game state, which can be copied, has a placeholder heuristic function, and the ability to track a win (ties would be simple to add with a linear search for a 0 (no token). Some quick work should make the win function not have as many duplicates, which do currently show up. The method would also make the function more legible, brief, and efficient, I just didn't think about it while implementing. I'll try to have this done before merge in case we go with this option.