import numpy
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
    
    # maxSearch(self, state, alpha, beta, depth)
    #    Input: self (the object)
    #    state (the current game state)
    #    alpha (the highest value seen in this path)
    #    beta (the lowest value seen in this path)
    #    depth (the current depth of the recursion)
    #
    #    Output: Float (the perceived value of this state)
    #    List (the list of actions to take after this state to get the best value)
    #
    #    Implements the search of the maximizing player in alpha-beta pruning.
    def maxSearch(self, state, alpha, beta, depth):
        if self.maxLayers == depth or state.isWin():
            return (state.h(), [])
        #end if
        
        utility = -float('inf')
        maxAction = [0,0,0]
        
        for action in actions(state):
            newState = result(state, action, 'max')
            response = minSearch(newState, alpha, beta, depth+1)[0]
            del newState
            
            if response > utility:
                maxAction = action
                utility = response
            #end if
            
            if utility >= beta:
                return (utility, maxAction)
            #end if
            
            alpha = max(alpha, utility)
        #end for
        
        return (utility, maxAction)
    #end maxSearch
    
    # minSearch(self, state, alpha, beta, depth)
    #    Input: self (the object)
    #    state (the current game state)
    #    alpha (the highest value seen in this path)
    #    beta (the lowest value seen in this path)
    #    depth (the current depth of the recursion)
    #
    #    Output: Float (the perceived value of this state)
    #    List (the list of actions to take after this state to get the best value)
    #
    #    Implements the search of the minimizing player in alpha-beta pruning.
    def minSearch(self, state, alpha, beta, depth):
        if self.maxLayers == depth or state.isWin():
            return (state.h(), [])
        #end if
        
        utility = -float('inf')
        minAction = [0,0,0]
        
        for action in actions(state):
            newState = result(state, action, 'min')
            response = maxSearch(newState, alpha, beta, depth+1)[0]
            
            if response < utility:
                minAction = action
                utility = response
            #end if
            
            if utility <= alpha:
                return (utility, minAction)
            #end if
            
            beta = min(beta, utility)
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
        response = maxSearch(state, -float('inf'), float('inf'), 0)
        
        return response[1]
    #end alphaBetaSearch
    
#end Model