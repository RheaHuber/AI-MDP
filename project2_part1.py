# MDP Policy Evaluator
# Receives default reward and input file from command line
# Input file is a .csv file containing an MDP policy as a 3x4 matrix of integers
# Returns the expected utility of the provided policy

# Import sys to access command line arguments
import sys

# Receive variable value and input file name from command line
# Reward for non-terminal states
REWARD = float(sys.argv[1])
policy = open(str(sys.argv[2]), "rt")

# Constant values
# Maximum iterations allowed
MAXITERATIONS = 20
# Gamma (discount factor)
DISCOUNT = 0.95
# Transition probability of success
TRANSSUCCESS = 0.8
# Transition probability of each result of a failure
TRANSFAIL = (1 - TRANSSUCCESS) / 2
# If change in all V(s) from an iteration falls below this value, stop iteration
TOLERANCE = 0.00001

# Fill 2D array with reward values
rewards = [[REWARD, REWARD, REWARD, 1],
           [REWARD, REWARD, REWARD, -1],
           [REWARD, REWARD, REWARD, REWARD]]

# Fill 3D array with actions
actions = [[[2, -1], [2, -2], [2, -1, -2], []],
           [[1, -1], [], [1, 2, -1], []],
           [[1, 2], [2, -2], [1, 2, -2], [1, -2]]]

# Fill 2 2D arrays with values V(s)
values1 = [[0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0]]

values2 = [[0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0]]

# Read inputs into 2D array
positions = [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0]]

currentRow = 0
currentCol = 0
neg = 0
for line in policy:
    for x in line:
        if x == ',':
            currentCol += 1
        elif x == '-':
            neg = 1
        elif neg == 1:
            if x == '1':
                positions[currentRow][currentCol] = -1
            elif x == '2':
                positions[currentRow][currentCol] = -2
            neg = 0
        elif x == '1':
            positions[currentRow][currentCol] = 1
        elif x == '2':
            positions[currentRow][currentCol] = 2
    currentRow += 1
    currentCol = 0
    if currentRow == 3:
        break


# Function to calculate new values of all states
def findValues(valuesIn, valuesOut):
    for row in range(3):
        for col in range(4):
            # If this is a terminal state
            if len(actions[row][col]) == 0:
                continue
            # Values of each possible move
            valStay = rewards[row][col] + (DISCOUNT * valuesIn[row][col])
            # If moving North is possible
            if actions[row][col].count(1) != 0:
                valNorth = rewards[(row - 1)][col] + (DISCOUNT * valuesIn[(row - 1)][col])
            else:
                # Or run in place
                valNorth = valStay
            # If moving East is possible
            if actions[row][col].count(2) != 0:
                valEast = rewards[row][(col + 1)] + (DISCOUNT * valuesIn[row][(col + 1)])
            else:
                # Or run in place
                valEast = valStay
            # If moving South is possible
            if actions[row][col].count(-1) != 0:
                valSouth = rewards[(row + 1)][col] + (DISCOUNT * valuesIn[(row + 1)][col])
            else:
                # Or run in place
                valSouth = valStay
            # If moving West is possible
            if actions[row][col].count(-2) != 0:
                valWest = rewards[row][(col - 1)] + (DISCOUNT * valuesIn[row][(col - 1)])
            else:
                # Or run in place
                valWest = valStay
            # Calculate final value based on actual move intended
            action = positions[row][col]
            if action == 1:
                valuesOut[row][col] = (TRANSSUCCESS * valNorth) + (TRANSFAIL * valWest) + (TRANSFAIL * valEast)
            elif action == 2:
                valuesOut[row][col] = (TRANSSUCCESS * valEast) + (TRANSFAIL * valNorth) + (TRANSFAIL * valSouth)
            elif action == -1:
                valuesOut[row][col] = (TRANSSUCCESS * valSouth) + (TRANSFAIL * valEast) + (TRANSFAIL * valWest)
            else:
                valuesOut[row][col] = (TRANSSUCCESS * valWest) + (TRANSFAIL * valSouth) + (TRANSFAIL * valNorth)


# Main iterative loop
iteration = 0
while iteration < MAXITERATIONS:
    # Alternate between writing to/from each array
    if iteration % 2 == 0:
        findValues(values2, values1)
    else:
        findValues(values1, values2)
    # Check how much the values have changed in last iteration
    maxDiff = 0
    for rowNum in range(3):
        for colNum in range(4):
            diff = values1[rowNum][colNum] - values2[rowNum][colNum]
            if diff < 0:
                diff *= -1
            if diff > maxDiff:
                maxDiff = diff
    iteration += 1
    if maxDiff < TOLERANCE:
        break

# Output the value of the starting position, according to the given policy and parameters
# "iteration" was incremented one extra time before the while loop ended
print("\nIteration: " + str(iteration - 1))
if iteration % 2 == 0:
    print("V(start): " + str(round(values2[2][0], 5)))
else:
    print("V(start): " + str(round(values1[2][0], 5)))
