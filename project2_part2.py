# MDP Policy Optimizer
# Receives transition success probability and default reward
# Finds the optimal policy for the given parameters
# Returns the expected utility of the optimal policy and the policy itself

# Import sys to access command line arguments
import sys

# Receive variable value and input file name from command line
# Transition probability of success
TRANSSUCCESS = float(sys.argv[1])
# Reward for non-terminal states
REWARD = float(sys.argv[2])

# Constant values
# Maximum iterations allowed
MAXITERATIONS = 20
# Gamma (discount factor)
DISCOUNT = 0.95
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

# Fill a 2D array for the policy with dummy values
policy = [[0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]]


# Function to calculate new values of all states
def findValues(valuesIn, valuesOut):
    for row in range(3):
        for col in range(4):
            # If this is a terminal state
            if len(actions[row][col]) == 0:
                continue
            # Values V(s) of each possible move
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
            # Values Q(s, a)
            chooseNorth = (TRANSSUCCESS * valNorth) + (TRANSFAIL * valWest) + (TRANSFAIL * valEast)
            chooseEast = (TRANSSUCCESS * valEast) + (TRANSFAIL * valNorth) + (TRANSFAIL * valSouth)
            chooseSouth = (TRANSSUCCESS * valSouth) + (TRANSFAIL * valEast) + (TRANSFAIL * valWest)
            chooseWest = (TRANSSUCCESS * valWest) + (TRANSFAIL * valSouth) + (TRANSFAIL * valNorth)
            # Find highest Q(s, a) and update policy and V(s)
            if chooseNorth >= chooseEast and chooseNorth >= chooseSouth and chooseNorth >= chooseWest:
                policy[row][col] = 1
                valuesOut[row][col] = chooseNorth
            elif chooseEast >= chooseSouth and chooseEast >= chooseWest:
                policy[row][col] = 2
                valuesOut[row][col] = chooseEast
            elif chooseSouth >= chooseWest:
                policy[row][col] = -1
                valuesOut[row][col] = chooseSouth
            else:
                policy[row][col] = -2
                valuesOut[row][col] = chooseWest


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

# Output the Vopt(start) and optimized policy
# "iteration" was incremented one extra time before the while loop ended
print("\nIteration: " + str(iteration - 1))
if iteration % 2 == 0:
    print("Vopt: " + str(round(values2[2][0], 5)))
else:
    print("Vopt: " + str(round(values1[2][0], 5)))

print("\nOptimal policy:")
for currentRow in range(3):
    print(policy[currentRow])

# Write solution to file
outputData = open("expectimax.csv", "w")
for currentRow in range(3):
    outputData.write(str(policy[currentRow]))
    outputData.write("\n")

# Close the output file
outputData.close()
