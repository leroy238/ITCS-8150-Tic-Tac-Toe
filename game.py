import numpy as np
import model

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
        return 1
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
    
    # isWin(self)
    #    Input: self (the object)
    #
    #    Output: Boolean (if state is won)
    #    winner (1 if max player, -1 if min player, 0 if not won)
    #
    #    Tests if a state is won, and returns the player that won.
    def isWin(self):
        # Main idea, to get a win, you need a 0 in some dimension.
        # Loop over pairs of dimensions, saves on redundancy.
        # Store all potential wins, see if they work by expanding in each direction.
        
        potWins = []
        for y in range(3):
            for z in range(3):
                token = self.gameRepresentation[0, y, z]
                if token != 0:
                    potWins.append((np.array([0,y,z]),token))
                #end if
            #end for
        #end for
        
        for x in range(3):
            for z in range(3):
                token = self.gameRepresentation[x, 0, z]
                if token != 0:
                    potWins.append((np.array([x,0,z]),token))
                #end if
            #end for
        #end for
        
        for x in range(3):
            for y in range(3):
                token = self.gameRepresentation[x, y, 0]
                if token != 0:
                    potWins.append((np.array([x,y,0]),token))
                #end if
            #end for
        #end for
        
        # Create extension directions.
        extensions = []
        for x in range(2):
            for y in range(2):
                for z in range(2):
                    #Extension [0,0,0] is invalid.
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
                        return (True, val)
                    #end if
                #end if
            #end for
        #end for
        
        return (False, 0)
    #end isWin
    
#end State

# This class holds all the information about the current Game being played.
class Game:
    
    aiPlayer = None
    gameState = None
    
#end Game