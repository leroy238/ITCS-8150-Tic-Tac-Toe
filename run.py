import traceback
import numpy as np
import game
import model

mode = 'debug' #other mode is 'run'

# stateTest()
#    Input: None
#
#    Output: None (Exceptions on failure)
#
#    Throughly tests the functions of State.
def stateTest():
            #Unit tests for State
        test_array = np.zeros(shape=(4,4,4), dtype=int)
        
        test_state = game.State()
        
        #Heuristic tests omitted since they do not yet exist.
        
        assert(test_state.play(1,1,1,'max'))
        assert(test_state.play(1,0,1,'min'))
        assert(not test_state.play(1,1,1, 'max'))
        
        test_array[1,1,1] = 1
        test_array[1,0,1] = -1
        
        assert(np.all(np.equal(test_state.getState(), test_array)))
        
        test_array[2,2,2] = 1
        
        test_state.setState(test_array)
        assert(np.all(np.equal(test_state.getState(), test_array)))
        
        try:
            test_state.setState(np.ndarray(shape=(3,3,3), dtype=int))
            assert(False)
        except TypeError:
            #Exception here was expected.
            assert(True)
        #end try/except
        
        copy_state = test_state.copy()
        assert(np.all(np.equal(copy_state.getState(), test_state.getState())))
        
        assert(copy_state.play(2,1,3,'min'))
        assert(not np.all(np.equal(copy_state.getState(), test_state.getState())))
        
        del copy_state
        del test_state
        del test_array
        
        test_state = game.State()
        assert(test_state.play(0,0,0,'max'))
        assert(test_state.play(1,1,1,'max'))
        assert(test_state.play(2,2,2,'max'))
        assert(test_state.play(3,3,3,'max'))
        
        assert(test_state.isWin()[0] and test_state.isWin()[1] == 1)
        
        del test_state
        
        test_state = game.State()
        assert(test_state.play(0,1,0,'max'))
        assert(test_state.play(0,1,1,'max'))
        assert(test_state.play(0,1,2,'max'))
        assert(test_state.play(0,1,3,'max'))
        
        assert(test_state.isWin()[0] and test_state.isWin()[1] == 1)
        
        del test_state
        
        test_state = game.State()
        assert(test_state.play(1,0,0,'max'))
        assert(test_state.play(1,1,0,'max'))
        assert(test_state.play(1,2,0,'max'))
        assert(test_state.play(1,3,0,'max'))
        
        assert(test_state.isWin()[0] and test_state.isWin()[1] == 1)
        
        del test_state
        
        test_state = game.State()
        assert(test_state.play(0,1,0,'min'))
        assert(test_state.play(1,1,0,'min'))
        assert(test_state.play(2,1,0,'min'))
        assert(test_state.play(3,1,0,'min'))
        
        assert(test_state.isWin()[0] and test_state.isWin()[1] == -1)
        
        del test_state
        
        test_state = game.State()
        assert(test_state.play(0,1,0,'min'))
        assert(test_state.play(1,1,0,'max'))
        assert(test_state.play(2,1,0,'min'))
        assert(test_state.play(3,1,0,'max'))
        
        assert(not(test_state.isWin()[0]) and test_state.isWin()[1] == 0)
        
        del test_state


def debug():
    try:
        #Tests all aspects of State
        stateTest()
    except Exception:
        traceback.print_exc()
        return -1
    #end try/except

    return 0
#end debug

def main():
    return 0
#end main

def printStatus(status):
    if status == 0:
        print('No errors on execution')
    else:
        print('Error upon execution, terminating.')

if __name__ == '__main__':
    status = -1
    if mode == 'debug':
        status = debug()
    else:
        status = main()
    #end if/else
    
    printStatus(status)
#end if