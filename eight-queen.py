import random
import time
"""
OVERVIEW: 
Uses random-start hill algorithm to solve the 8 queen problem. 
Two successor selection methods are used: first-choice random selection and selection 
from all possible successors. Queens cannot occupy the same row in initial state.

NOTES: 
Random Restart Hill Algorithm:
    Perform local search to find best successor.
    Choose best successor state based on evaluation function and move to that state.
    Repeat max-restart amount of times to escape local maxima and plateue. 
With First Choice Successor:
    Return first randomized successor that is better than current state.
"""

def isDiagonal(p1, p2):
    """
    Checks if two numbers are located diagonally to each other.

    Args: 
        p1 (list[int,int]): list of size 2 containing first point's row and column 
        p2 (list[int,int]): list of size 2 containing second point's row and column 
    
    Returns: 
        bool: true if diagonal
    """
    [x1, y1] = p1
    [x2, y2] = p2
    h_dist = abs(x1 - x2)
    v_dist = abs(y1 - y2)
    return h_dist == v_dist

def calcAttacks(board):
    """
    Returns number of unique attack pairs.
    """
    attackPairs = set()
    for i, q in enumerate(board):
        for j, otherQ in enumerate(board):
            pair = ((q, i), (otherQ, j))
            if (i != j and # ensures that its not the same queen
                (q == otherQ or isDiagonal(*pair)) and # if in attack path
                ((otherQ, j), (q, i)) not in attackPairs): # avoid counting duplicates

                attackPairs.add(pair)    
    return len(attackPairs)

def randomEightQueensBoard():
    """
    Returns a randomly generated 8 queens board with 1 queen in each row.
    """
    # create one queen in each row
    board = [-1] * 8
    for i in range(8):
        row = random.randint(0, 7)
        # randomize row position if another queen is already in that row
        while (row in board):
            row = random.randint(0, 7)
        board[i] = row
    return board

def printBoard(board):
    """
    Prints board in a chess grid format.
    """
    for r in range(len(board)):
        for c in range(len(board)):
            if r != board[c]:
                print('_', end=' ')
            else:
                print(board[c], end=' ')
        print()
        

def hillClimbing(getSuccessorFunc):
    maxRestart = 500
    bestState = None
    bestAttacks = 999

    startTime = time.time()

    for _ in range(maxRestart):
        # create random initial state
        current = randomEightQueensBoard()
        currentAttacks = calcAttacks(current)

        # local search to find best successor
        while (currentAttacks > 0):

            # search for best successor state
            successorState, successorAttacks = getSuccessorFunc(current)

            # if successor is better, save it
            if (successorAttacks < currentAttacks):
                current = successorState
                currentAttacks = successorAttacks
                # if the solution is found early, terminate local search
                if currentAttacks == 0:
                    break
            # if local maxima or plateue is reached, restart search
            else:
                break

        # if results from local search are better than initial state, save the best state
        if (currentAttacks < bestAttacks or currentAttacks == 0):
            bestAttacks = currentAttacks
            bestState = current
            # if the best state is the solution, terminate hill climbing 
            if currentAttacks == 0:
                break

    return bestState, bestAttacks, time.time() - startTime




def getBestSuccessor(current_state):
    """
    Generates all possible successors from current state and returns one with the best performance.
    """
    bestState = None
    bestAttacks = 999
    # for each queen
    for col in range(len(current_state)):
        # move the queen to different rows within the same column
        for row in range(len(current_state)):
            # skip if new row is the same as old row
            if row != current_state[col]:
                successor = current_state[:col] + [row] + current_state[col+1:]
                successorAttacks = calcAttacks(successor)
                if (bestAttacks > successorAttacks):
                    bestState = successor
                    bestAttacks = successorAttacks 
    
    return bestState, bestAttacks


def getFirstChoiceSuccessor(current_state):
    """
    Returns the first random successor if it's better than current state.
    """
    currentAttacks = calcAttacks(current_state)
    maxGeneration = 100
    for i in range(maxGeneration):
        successor = [-1] * 8 
        for j in range(len(current_state)):
            new = random.randint(0, 7)
            successor[j] = new
    
        successorAttacks = calcAttacks(successor)
        # if successor is better, return
        if successorAttacks < currentAttacks or successorAttacks == 0:
            return successor, successorAttacks
    # if no successor is better, return current state 
    return current_state, currentAttacks

# tests program 10 times
print("RANDOM-RESTART HILL CLIMBING")
for i in range(10):
    bestState, attacks, duration = hillClimbing(getBestSuccessor)
    printBoard(bestState)
    print("Attacks: " + str(attacks) + " Duration: " + str(duration))

print("FIRST CHOICE RANDOM-RESTART HILL CLIMBING")
for i in range(10):
    bestState, attacks, duration = hillClimbing(getFirstChoiceSuccessor)
    printBoard(bestState)
    print("Attacks: " + str(attacks) + " Duration: " + str(duration))
