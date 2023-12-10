import numpy as np
import model
from enum import Enum
import itertools 

class Turn(Enum):
    PLAYER = 1
    AI = 2
    
class Token(Enum):
    PLAYER = -1
    AI = 1

# This class stores the internal state of the game being played.
class State:

    gameRepresentation = None
    playerPlayed = None
    aiPlayed = None
    layerKeys = None
    
    # __init__(self)
    #    Input: self (the object being instantiated)
    #
    #    Output: None (Side effect of instantiation)
    #
    #    Initializes the State object with an array of values, initially 0,
    #    0 meaning an empty board.
    def __init__(self, layerKeys = []):
        self.gameRepresentation = np.zeros(shape=(4,4,4), dtype=int)
        if len(layerKeys) == 0:
            self.layerKeys = self._produceAllLoop(np.zeros(shape=(4,4), dtype=int), 1)
        else:
            self.layerKeys = layerKeys
        #end if/else
    # end __init__
    
    def hash(self):
        num = 0
        for i in range(4):
            num += self.layerKeys.index(self.gameRepresentation[i,:,:]) << 12
        #end for
        
        return num
    #end __hash__
    
    def _produceAllLoop(self, state, val):
        #Produce all actions
        actions = []
        for x in range(4):
            for y in range(4):
                if state[x,y] == 0:
                    actions.append((x,y))
                #end if
            #end for
        #end for
        
        allStates = []
        for action in actions:
            state[action[0],action[1]] = val
            allStates.append(self._produceAllLoop(state, -val))
        #end for
        return allStates
    #end _produceAllLoop

    # isValidExtension(self, point, extension)
    # Input: self (the object), point (the position on the board), extension (the change to be applied to the position on the board)
    #
    # Output: boolean (whether or not the extension results in a position that is still on the board) 
    def isValidExtension(self, point: [int, int, int], extension: [int, int, int]):
        xExtend = point[0] + 3 * extension[0]
        yExtend = point[1] + 3 * extension[1]
        zExtend = point[2] + 3 * extension[2]
        return xExtend < 4 and xExtend > -1 and yExtend < 4 and yExtend > -1 and zExtend < 4 and zExtend > -1
    #end isValidExtension
    
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
        extensions = [np.array(list(pos)) for pos in itertools.product(range(-1, 2), range(-1,2), range(-1, 2)) if pos != (0, 0, 0)]
        # for x in range(-1, 2):
        #     for y in range(-1, 2):
        #         for z in range(-1, 2):
        #             # Extension [0,0,0] is invalid.
        #             if x != 0 or y != 0 or z != 0:
        #                 extensions.append(np.array([x,y,z]))
                    #end if
                #end for
            #end for
        #end for
        
        # Produces all edge points. 
        points = [np.array(list(pos)) for pos in itertools.product(range(4), range(4), range(4)) if self.gameRepresentation[pos[0], pos[1], pos[2]] != 0] # []
        # for x in range(4):
        #     for y in range(4):
        #         for z in range(4):
        #             if self.gameRepresentation[x,y,z] != 0:
        #                 points.append(np.array([x,y,z]))
                    #end if
                #end for
            #end for
        #end for
        
        startPoints = {(0,0,0)}
        for point in points:
            x = point[0]
            y = point[1]
            z = point[2]
            
            startPoints.add((0,y,z))
            startPoints.add((x,0,z))
            startPoints.add((x,y,0))
            startPoints.add((0,0,z))
            startPoints.add((0,y,0))
            startPoints.add((x,0,0))
        #end for
        # Now only contains valid starting positions
        points = [np.array([point[0], point[1], point[2]]) for point in startPoints]
        
        score = 0
        
        # Extend each point in each direction.
        for point in points:
            for direction in extensions:
                if not self.isValidExtension(point, direction):
                    continue
                #end if
                prevVal = 0
                count = 0
                tempScore = 0
                for num in range(3):
                    value = self.gameRepresentation[point[0], point[1], point[2]]
                    # Point has a value in it.
                    if value != 0:
                        if prevVal == 0:
                            prevVal = value
                        #end if
                        
                        if prevVal == value:
                            # We found another one in the line.
                            # Pos for max, neg for min.
                            # The more that are in a particular direction, the better.
                            count += 1
                            tempScore += value * (count + 1)
                        else:
                            # Line is blocked. Should not encourage moves like this.
                            count = 0
                            continue
                        #end if/else
                    #end if
                    
                    score += tempScore
                    
                    # We want to encourage points even if they are not directly
                    # in a line. No case for value is 0 is necessary.
                    
                    point[0] += direction[0]
                    point[1] += direction[1]
                    point[2] += direction[2]
                    
                #end for
            #end for
        #end for
        
        return score
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
            self.gameRepresentation[x, y, z] = player.value if isinstance(player, Token) else player
            
            # Store last played move.
            if (isinstance(player,Token) and player.value == -1) or player == -1:
                self.playerPlayed = np.array([x,y,z])
            else:
                self.aiPlayed = np.array([x,y,z])
            #end if
            
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
        copy_state = State(self.layerKeys)
        copy_state.setState(np.copy(self.getState()))
        copy_state.playerPlayed = self.playerPlayed
        copy_state.aiPlayed = self.aiPlayed
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
        for y in range(4):
            for z in range(4):
                token = self.gameRepresentation[0, y, z]
                array = [0,y,z]
                if token != 0 and ((array,token) not in potWins):
                    potWins.append((array,token))
                #end if
            #end for
        #end for
        
        for x in range(4):
            for z in range(4):
                token = self.gameRepresentation[x, 0, z]
                array = [x,0,z]
                if token != 0 and ((array, token) not in potWins):
                    potWins.append((array,token))
                #end if
            #end for
        #end for
        
        for x in range(4):
            for y in range(4):
                token = self.gameRepresentation[x, y, 0]
                array = [x,y,0]
                if token != 0 and ((array, token) not in potWins):
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
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
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
                xUnfeas = (point[0] > 0 and direction[0] > 0) or (point[0] < 3 and direction[0] < 0)
                yUnfeas = (point[1] > 0 and direction[1] > 0) or (point[1] < 3 and direction[1] < 0)
                zUnfeas = (point[2] > 0 and direction[2] > 0) or (point[2] < 3 and direction[2] < 0)
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
    
    # getLastPlayed(self)
    #    Input: self (the object)
    #    player (string describing the player whose move is wanted)
    #    
    #    Output: Numpy array of the last played move.
    #
    #    Retrieves the last played move from the state.
    def getLastPlayed(self, player):
        return self.playerPlayed if player.lower() == 'player' else self.aiPlayed
    #end getLastPlayed    
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
        self.aiPlayer = model.Model(maxDepth)
        
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
        
        print(winner + ' has won!')
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