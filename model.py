import numpy as np
import game

class Model:
    
    maxLayers = 0
    
    # __init__(self)
    #    Input: self (the object being instantiated)
    #    maxLayers (maximum depth of the tree)
    #
    #    Output: None (Side effect of instantiation)
    #
    #    Initializes the Model object, with a maximum depth of alpha-beta pruning.
    def __init__(self, maxLayers):
        self.maxLayers = maxLayers
    #end __init__
    
    # _heuristicSort(self, played, actions, zeroIndex)
    #    Input: self (the object)
    #    played (Latest move played)
    #    actions (List of actions)
    #    zeroIndex (Index of the first element that doesn't have a positive heuristic)
    #
    #    Output: List of actions (3-long numpy arrays) sorted in heuristic order
    #    Integer of the new zeroIndex of the sorted list.
    #
    #    Returns a list of sorted actions based upon if they match a direction of the
    #    dimension of a played move or not. Theoretically this puts moves in a line
    #    going before those that aren't, making alpha-beta pruning more efficient.
    #    It does miss some cases of 3D diagonals, but it needs to be fast to speed
    #    up the algorithm.
    def _heuristicSort(self, played, actions, zeroIndex):
        sortedList = actions[:zeroIndex]
        newIndex = len(sortedList)
        for i in range(zeroIndex, len(actions)):
            if np.any(np.isin(actions[i], played)):
                sortedList.insert(0,actions[i])
                newIndex += 1
            else:
                sortedList.append(actions[i])
            #end if/else
        #end for
        
        return sortedList, newIndex
    #end _heuristicSort
    
    # maxSearch(self, state, alpha, beta, depth, zeroIndex, possibleActions)
    #    Input: self (the object)
    #    state (the current game state)
    #    alpha (the highest value seen in this path)
    #    beta (the lowest value seen in this path)
    #    depth (the current depth of the recursion)
    #    zeroIndex (Index of the first element that doesn't have a positive heuristic)
    #    possibleActions (list of all possible actions)
    #
    #    Output: Float (the perceived value of this state)
    #    List (the list of actions to take after this state to get the best value)
    #
    #    Implements the search of the maximizing player in alpha-beta pruning.
    def maxSearch(self, state, alpha, beta, depth, zeroIndex, possibleActions = []):
        self.count += 1
        if self.maxLayers == depth or state.isWin()[0]:
            return (state.h(), [])
        #end if
        
        possibleActions, zeroIndex = self._heuristicSort(state.getLastPlayed(), possibleActions, zeroIndex)
        utility = -float('inf')
        maxAction = [0,0,0]
        initialActions = possibleActions.copy()
        for i, action in enumerate(initialActions):#game.actions(state):
            newState = game.result(state, action, 'max')
            possibleActions.pop(i)
            response = self.minSearch(newState, alpha, beta, depth+1, zeroIndex, possibleActions)[0]
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
    
    # minSearch(self, state, alpha, beta, depth, zeroIndex, possibleActions)
    #    Input: self (the object)
    #    state (the current game state)
    #    alpha (the highest value seen in this path)
    #    beta (the lowest value seen in this path)
    #    depth (the current depth of the recursion)
    #    possibleActions (list of all possible actions)
    #    zeroIndex (Index of the first element that doesn't have a positive heuristic)
    #
    #    Output: Float (the perceived value of this state)
    #    List (the list of actions to take after this state to get the best value)
    #
    #    Implements the search of the minimizing player in alpha-beta pruning.
    def minSearch(self, state, alpha, beta, depth, zeroIndex, possibleActions = []):
        self.count += 1
        if self.maxLayers == depth or state.isWin()[0]:
            return (state.h(), [])
        #end if
        
        possibleActions, zeroIndex = self._heuristicSort(state.getLastPlayed(), possibleActions, zeroIndex)
        utility = float('inf')
        minAction = [0,0,0]
        initialActions = possibleActions.copy()
        for i, action in enumerate(initialActions): #game.actions(state)
            newState = game.result(state, action, 'min')
            possibleActions.pop(i)
            response = self.maxSearch(newState, alpha, beta, depth+1, zeroIndex, possibleActions)[0]
            
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
        response = self.maxSearch(state, -float('inf'), float('inf'), 0, 0, actions)
        
        return response[1]
    #end alphaBetaSearch
    
#end Model