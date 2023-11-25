import numpy as np
import model
from enum import Enum

class Turn(Enum):
    PLAYER = 1
    AI = 2
    
class Token(Enum):
    PLAYER = -1
    AI = 1

# This class stores the internal state of the game being played.
class State:

    gameRepresentation = None
    
    # __init__(self)
    #    Input: self (the object being instantiated)
    #
    #    Output: None (Side effect of instantiation)
    #
    #    Initializes the State object with an array of values, initially 0,
    #    0 meaning an empty board.
    def __init__(self):
        self.gameRepresentation = np.zeros(shape=(4,4,4), dtype=int)
    # end __init__
    
    # h(self)
    #    Input: self (the object)
    #
    #    Output: integer (heuristic value of the state)
    #
    #    The heuristic function. This function will determine a value that
    #    represents the "goodness" of a particular state to a particular player.
    #    Negative values mean the minimizing player is in a better position,
    #    positive values mean the maximizing player is in a better position.
    def h(self):
        win, winner = self.isWin()
        # Check if max wins, if min wins, or if tie.
        if win and winner == 1:
            return 100
        elif win and winner == -1:
            return -100
        elif win and winner == 0:
            #Heuristic is negative since the AI is maximizing.
            return -20
        #end if/elif
        
        # Create extension directions.
        extensions = []
        for x in range(2):
            for y in range(2):
                for z in range(2):
                    # Extension [0,0,0] is invalid.
                    if x != 0 or y != 0 or z != 0:
                        extensions.append(np.array([x,y,z]))
                    #end if
                #end for
            #end for
        #end for
        
        # Produces all edge points. 
        points = []
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    if x == 0 or y == 0 or z == 0:
                        points.append(np.array[x,y,z])
                    #end if
                #end for
            #end for
        #end for
        
        # Extend each point in each direction.
        score = 0
        
        for point in points:
            for direction in extensions:
                prevVal = 0
                count = 0
                for num in range(4):
                    value = self.gameRepresentation[point[0], point[1], point[2]]
                    # No point 
                    if value != 0:
                        if prevVal == 0:
                            prevVal = value
                        #end if
                        
                        if prevVal == value:
                            # We found another one in the line.
                            # Pos for max, neg for min.
                            # The more that are in a particular direction, the better.
                            count += value * (count + 1)
                        else:
                            # Line is blocked. Should not encourage moves like this.
                            count = 0
                        #end if/else
                    #end if
                    
                    # We want to encourage points even if they are not directly
                    # in a line. No case for value is 0 is necessary.
                    
                    point[0] += direction[0]
                    point[1] += direction[1]
                    point[2] += direction[2]
                #end for
            #end for
        #end for
    # end h
    
    # play(self, x, y, z, player
    #    Input: self (the object)
    #    x (the x value in the array, 0 to 3)
    #    y (the y value in the array, 0 to 3)
    #    z (the z value in the array, 0 to 3)
    #    player (a string, 'MAX' for maximizing player turn,
    #    'MIN' for minimizing player)
    #
    #    Output: Boolean (Is move legal)
    #    (side effect of changing the game state)
    #    
    #    Does the turn of the player mentioned. Places a number to act
    #    as a token for the player in the game's representation array.
    def play(self, x, y, z, player):
        if self.gameRepresentation[x,y,z] == 0:
            self.gameRepresentation[x, y, z] = 1 if player.upper() == 'MAX' else -1
            return True
        #end if
        
        return False
    #end play
    
    # isValid(self, x, y, z)
    #    Input: self (the object)
    #    x (the x value of the move)
    #    y (the y value of the move)
    #    z (the z value of the move)
    #    
    #    Output: Boolean (If move is valid)
    #
    #    Returns if a given move would cause an error without playing the move.
    def isValid(self, x, y, z):
        return self.gameRepresentation[x,y,z] == 0
    
    # getState(self)
    #    Input: self (the object)
    #
    #    Output: numpy ndarray, 4x4x4 (the game's internal representation)
    #
    #    Returns the array that represents the current game's state.
    def getState(self):
        return self.gameRepresentation
    # end getState
    
    # setState(self, array)
    #    Input: self (the object)
    #    array (numpy ndarray, 4x4x4)
    #
    #    Output: None (side effect of changing the game state to array)
    #
    #    Sets the value of the game's representation array to the array provided.
    def setState(self, array):
        if np.shape(array) == (4,4,4):
            del self.gameRepresentation
            self.gameRepresentation = array
        else:
            raise TypeError('Argument "array" is not 4x4x4 as expected')
        #end if/else
    #end setState
    
    # copy(self)
    #    Input: self (the object)
    #
    #    Output: State (a state in the same state as self)
    #
    #    Provides a copy of the State object.
    def copy(self):
        copy_state = State()
        copy_state.setState(np.copy(self.getState()))
        return copy_state
    #end copy
    
    # _potWins(self)
    #    Input: self (the object)
    #
    #    Output: List (list of all points that could include wins)
    #
    #    Returns all points with a 0 in some direction (all winning lines have a 0
    #    in some direction, because they cross the board.
    def _potWins(self):
        # Main idea, to get a win, you need a 0 in some dimension.
        # Loop over pairs of dimensions, 3(4^2) < 4^3
        # Store all potential wins, see if they work by expanding in each direction.
        
        potWins = []
        for y in range(3):
            for z in range(3):
                token = self.gameRepresentation[0, y, z]
                array = np.array([0,y,z])
                if token != 0 and array not in potWins:
                    potWins.append((array,token))
                #end if
            #end for
        #end for
        
        for x in range(3):
            for z in range(3):
                token = self.gameRepresentation[x, 0, z]
                array = np.array([x,0,z])
                if token != 0 and array not in potWins:
                    potWins.append((array,token))
                #end if
            #end for
        #end for
        
        for x in range(3):
            for y in range(3):
                token = self.gameRepresentation[x, y, 0]
                array = np.array([x,y,0])
                if token != 0 and array not in potWins:
                    potWins.append((array,token))
                #end if
            #end for
        #end for
        
        return potWins
    #end _potWins
    
    # isWin(self)
    #    Input: self (the object)
    #
    #    Output: Boolean (if state is won)
    #    winner (1 if max player, -1 if min player, 0 if not won)
    #
    #    Tests if a state is won, and returns the player that won.
    def isWin(self):
        potWins = self._potWins()
        
        # Create extension directions.
        extensions = []
        for x in range(2):
            for y in range(2):
                for z in range(2):
                    # Extension [0,0,0] is invalid.
                    if x != 0 or y != 0 or z != 0:
                        extensions.append(np.array([x,y,z]))
                    #end if
                #end for
            #end for
        #end for
        
        # Extend each potential win in every plausible direction.
        for potWin in potWins:
            for direction in extensions:
                point = potWin[0]
                # Determines plausibility of a direction.
                xUnfeas = point[0] > 0 and direction[0] > 0 
                yUnfeas = point[1] > 0 and direction[1] > 0
                zUnfeas = point[2] > 0 and direction[2] > 0
                if not(xUnfeas or yUnfeas or zUnfeas):
                    val = potWin[1]
                    
                    winFound = False
                    for numFound in range(1,4):
                        point = point + direction
                        
                        x = point[0]
                        y = point[1]
                        z = point[2]
                        token = self.gameRepresentation[x,y,z]
                        if token != val:
                            break
                        #end if
                        
                        if numFound == 3:
                            winFound = True
                        #end if
                    #end for
                    
                    if winFound:
                        # Return win + player who won
                        return (True, val)
                    #end if
                #end if
            #end for
        #end for
        
        # Check for tie.
        for matrix in self.gameRepresentation:
            for row in matrix:
                for value in row:
                    if value == 0:
                        # Return no win.
                        return (False, 0)
                    #end if
                #end for
            #end for
        #end for
        
        # Return tie.
        return (True, 0)
    #end isWin
    
#end State

# This class holds all the information about the current Game being played.
class Game:
    
    aiPlayer = None
    gameState = None
    turn = None
    
    # __init__(self, maxDepth)
    #    Input: self (the object being instantiated)
    #    maxDepth (the maximum depth that the AI is allowed to search through)
    #
    #    Output: None (Side effect of instantiation)
    #
    #    Instantiates the Game object, which includes a State and Model object.
    def __init__(self, maxDepth):
        self.gameState = State()
        self.aiPlayer = Model(maxDepth)
        
        self.turn = Turn.PLAYER
    #end __init__
    
    # run(self)
    #    Input: self (the object)
    #
    #    Output: None (Side effect of printing out who won)
    #
    #    Starts the game, ending when the game is finished and printing out who won.
    def run(self):
        winTuple = self.gameState.isWin()
    
        while(not winTuple[0]):
            if self.turn == Turn.PLAYER:
                # Temporary system of taking in a player's turn.
                playerTurn = input("Input your turn. Do this in the format 'x, y, z'")
                
                turnVal = np.array([0,0,0])
                count = 0
                
                for val in playerTurn.split(', '):
                    turnVal[count] = int(val)
                    count += 1
                #end for
                
                self.gameState.play(turnVal[0], turnVal[1], turnVal[2], Token.PLAYER)
            else:
                currState = self.gameState.getState()
                turnVal = self.aiPlayer.alphaBetaSearch(currState)
                
                self.gameState.play(turnVal[0], turnVal[1], turnVal[2], Token.AI)
            #end if/else
            
            # Temporary method of making the game state visible to the player.
            print(self.gameState.getState())
            
            winTuple = self.gameState.isWin()
        #end while
        
        winner = ''
        if winTuple[1] == 1:
            winner = 'Player'
        else:
            winner = 'AI'
        #end if/else
        
        print(winner + 'has won!')
    #end run

#end Game

# actions(state)
#    Input: state (Current game state)
#
#    Output: List (List of actions possible in this state)
#
#    Outputs all possible playable moves in a given state.
def actions(state):
    actions = []
    
    for x in range(4):
        for y in range(4):
            for z in range(4):
                if state.isValid(x,y,z):
                    actions.append(np.array([x,y,z]))
                #end if
            #end for
        #end for
    #end for
    
    return actions
#end actions

def result(state, action, player):
    newState = state.copy()
    
    val = 0
    if player.upper() == 'MAX':
        val = 1
    else:
        val = -1
    #end if/else
    
    newState.play(action[0], action[1], action[2], val)
    
    return newState
#end result