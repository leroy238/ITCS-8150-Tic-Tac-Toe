import numpy as np
import game

class Model:
    
    maxLayers = 0
    transpositionTable = None
    
    # __init__(self)
    #    Input: self (the object being instantiated)
    #    maxLayers (maximum depth of the tree)
    #
    #    Output: None (Side effect of instantiation)
    #
    #    Initializes the Model object, with a maximum depth of alpha-beta pruning.
    def __init__(self, maxLayers):
        self.maxLayers = maxLayers
        self.transpositionTable = dict()
    #end __init__
    
    # _dist(self, point, playerPoint, aiPoint
    #    Input: self (the object)
    #    point (Numpy array of coordinates on grid)
    #    playerPoint (Numpy array of coordinates of last player move)
    #    aiPoint (Numpy array of coordinates of last AI move)
    #
    #    Output: Integer
    #
    #    Produces the sum of the distances between point and both previous move points.
    def _dist(self, point, playerPoint, aiPoint):
        playerSum = np.sum(np.absolute((point - playerPoint)))
        # It is entirely possible for the AI to have not yet made a move.
        if np.any(aiPoint == None):
            return (playerSum, 0)
        #end if
        aiSum = np.sum(np.absolute((point - aiPoint)))
        return (playerSum, aiSum)
    #end _dist
    
    # _merge(self, left, right)
    #    Input: self (the object)
    #    left (list of 3-long numpy arrays)
    #    right (list of 3-long numpy arrays)
    #
    #    Output: List of 3-long numpy arrays
    #
    #    Merges the two input lists together in heuristic order, based on _dist.
    def _merge(self, state, left, right, player):
        array = []
    
        i,j = (0,0)
        while i < len(left) and j < len(right):
            leftResult = game.result(state, left[i], player)
            rightResult = game.result(state, right[j], player)
            hTable = self.transpositionTable
            maxMinFix = 1 if player == 'max' else -1
            if maxMinFix * leftResult.h(hTable) >= maxMinFix * rightResult.h(hTable):
                array.append(left[i])
                i += 1
            else:
                array.append(right[j])
                j += 1
            #end if/else
        #end while
        
        while i < len(left):
            array.append(left[i])
            i += 1
        #end while
        
        while j < len(right):
            array.append(right[j])
            j += 1
        #end while
        
        return array
    #end _merge
    
    # _mergeSort(self, array)
    #    Input: self (the object)
    #    array (list of 3-long numpy arrays)
    #
    #    Output: List of 3-long numpy arrays
    #
    #    Heuristically sorts the input array.
    def _mergeSort(self, state, array, player):
        if len(array) > 1:
            mid = len(array) // 2
            left = array[:mid]
            right = array[mid:]
            
            left = self._mergeSort(state, left, player)
            right = self._mergeSort(state, right, player)
            
            array = self._merge(state, left, right, player)
            
            return array
        else:
            return array
        #end if/else
    #end _mergeSort
    
    # maxSearch(self, state, alpha, beta, depth, possibleActions)
    #    Input: self (the object)
    #    state (the current game state)
    #    alpha (the highest value seen in this path)
    #    beta (the lowest value seen in this path)
    #    depth (the current depth of the recursion)
    #    possibleActions (list of all possible actions)
    #
    #    Output: Float (the perceived value of this state)
    #    List (the list of actions to take after this state to get the best value)
    #
    #    Implements the search of the maximizing player in alpha-beta pruning.
    def maxSearch(self, state, alpha, beta, depth, possibleActions = []):
        turnsTaken = np.sum(np.absolute(state.getState()))/2
        if self.maxLayers == depth or (turnsTaken >= 4 and state.isWin(self.transpositionTable)[0]):
            return (state.h(self.transpositionTable), [])
        #end if
        
        noCull = []
        for action in possibleActions:
            playerMove = state.getLastPlayed('player')
            aiMove = state.getLastPlayed('ai')
            distance = self._dist(action, playerMove, aiMove)
            if distance[0] > 3 or distance[1] > 3:
                noCull.append(action)
            #end if
        #end for
        possibleActions = noCull.copy()
        del noCull
        
        if self.maxLayers - depth > 1:
            possibleActions = self._mergeSort(state, possibleActions, 'max')
        #end if
        utility = -float('inf')
        maxAction = [0,0,0]
        initialActions = possibleActions.copy()
        maxIndex = max(10, len(initialActions))
        for i, action in enumerate(initialActions[:maxIndex]):
            newState = game.result(state, action, 'max')
            possibleActions.pop(i)
            response = self.minSearch(newState, alpha, beta, depth+1, possibleActions)[0]
            del newState
            
            if response > utility:
                maxAction = action
                utility = response
            #end if
            
            if utility >= beta:
                return (utility, maxAction)
            #end if
            
            alpha = max(alpha, utility)
            possibleActions = initialActions.copy()
        #end for
        
        return (utility, maxAction)
    #end maxSearch
    
    # minSearch(self, state, alpha, beta, depth, possibleActions)
    #    Input: self (the object)
    #    state (the current game state)
    #    alpha (the highest value seen in this path)
    #    beta (the lowest value seen in this path)
    #    depth (the current depth of the recursion)
    #    possibleActions (list of all possible actions)
    #
    #    Output: Float (the perceived value of this state)
    #    List (the list of actions to take after this state to get the best value)
    #
    #    Implements the search of the minimizing player in alpha-beta pruning.
    def minSearch(self, state, alpha, beta, depth, possibleActions = []):
        turnsTaken = np.sum(np.absolute(state.getState()))/2
        if self.maxLayers == depth or (turnsTaken >= 4 and state.isWin(self.transpositionTable)[0]):
            return (state.h(self.transpositionTable), [])
        #end if
        
        noCull = []
        for action in possibleActions:
            playerMove = state.getLastPlayed('player')
            aiMove = state.getLastPlayed('ai')
            distance = self._dist(action, playerMove, aiMove)
            if distance[0] > 3 or distance[1] > 3:
                noCull.append(action)
            #end if
        #end for
        possibleActions = noCull.copy()
        del noCull
        
        # Wasting time to do this at the node before the leaves.
        if self.maxLayers - depth > 1:
            possibleActions = self._mergeSort(state, possibleActions, 'min')
        #end if
        utility = float('inf')
        minAction = [0,0,0]
        initialActions = possibleActions.copy()
        maxIndex = max(10, len(initialActions))
        for i, action in enumerate(initialActions[:maxIndex]):
            newState = game.result(state, action, 'min')
            possibleActions.pop(i)
            response = self.maxSearch(newState, alpha, beta, depth+1, possibleActions)[0]
            
            if response < utility:
                minAction = action
                utility = response
            #end if
            
            if utility <= alpha:
                return (utility, minAction)
            #end if
            
            beta = min(beta, utility)
            possibleActions = initialActions.copy()
        #end for
        
        return (utility, minAction)
    #end minSearch
    
    # alphaBetaSearch(self, state)
    #    Input: self (the object)
    #    state (the current game state)
    #
    #    Output: Numpy Array (Best move to make)
    #
    #    Calls the initial alpha-beta search and returns the optimal action.
    #    The optimal action is the one that puts the model in the best position,
    #    given its heuristic evaluation of the state.
    def alphaBetaSearch(self, state):
        actions = game.actions(state)
        response = self.maxSearch(state, -float('inf'), float('inf'), 0, actions)
        
        return response[1]
    #end alphaBetaSearch
    
#end Model