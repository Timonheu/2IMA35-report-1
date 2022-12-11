import json
import math
import random
import sys

import numpy as np
np.set_printoptions(threshold=sys.maxsize)

# Function for performing a random from a single person
def doWalkForPerson(person, walkLength, adjacencyMatrix):
    # Initialise the starting point
    currentPerson = person
    remainingSteps = walkLength

    # Do walkLength steps on the random walk
    while remainingSteps > 0:
        # Check which nodes we can go to next
        currentPersonAdjacencies = adjacencyMatrix[i]

        # Get the indices of these nodes
        adjacentIndices = []
        for index in range(peopleCount):
            if currentPersonAdjacencies[index] != 0:
                adjacentIndices.append(index)

        # Check if we can actually leave this node, if not, the walk ends here
        if len(adjacentIndices) == 0:
            return currentPerson

        # Randomly select the next node that we go to (if possible)
        currentPerson = random.choice(adjacentIndices)
        remainingSteps -= 1

    # Walk has ended
    return currentPerson


# Read input files
followingGraphMetadata = None
with open("Data/Output/followingGraphMetadata.json", "r") as graphFileMeta:
    followingGraphMetadata = json.load(graphFileMeta)
peopleCount = len(followingGraphMetadata)

followingGraph = None
with open("Data/Output/followingGraph.json", "r") as graphFile:
    followingGraph = np.fromfile(graphFile).reshape(peopleCount, peopleCount)

# Perform random-walks
# Walk parameters
walkLength = int(math.sqrt(peopleCount))
walksPerPerson = 2 * 42 # Tsja, wat anders?

# Walk result
directedWeightedWalk = np.zeros((peopleCount, peopleCount)) # directedWeightedWalk[i][j] ==> #walks from i which ended at j

# Do the walks per person
for i in range(peopleCount):
    # Do walksPerPerson walks from person i
    for w in range (walksPerPerson):
        reachedPerson = doWalkForPerson(i, walkLength, followingGraph)
        directedWeightedWalk[i][reachedPerson] += 1

# Make the matrix undirected by adding the matrix and its transpose together
undirectedWeightedWalk = directedWeightedWalk + directedWeightedWalk.transpose()

# Get largest value in walk matrix to compute "relative" closeness between all politicians as
# (walks between i and j) / (maximum number of walks between any two politicians)
maxNumberWalks = np.amax(undirectedWeightedWalk)
relativeCloseness = np.divide(undirectedWeightedWalk, maxNumberWalks)

# Check if the graph is connected
for i in range(peopleCount):
    if np.count_nonzero(relativeCloseness[i]) == 0:
        print("Graph is not connected: " + graphFileMeta[i]["twitterHandle"] + " heeft geen enkele connectie")
        exit()

# Set distance between two people to  1 / relativeCloseness: less close = more distant ;)
# Loops needed to keep non-connected notes equal to 0
weightedGraph = np.zeros((peopleCount, peopleCount))
for i in range(peopleCount):
    for j in range(peopleCount):
        if relativeCloseness[i][j] != 0:
            weightedGraph[i][j] = 1 / relativeCloseness[i][j]

# Round distances to integers
weightedGraph = np.rint(weightedGraph)

# Store graph in file
with open("Data/Output/weightedGraph.json", "w") as weightedGraphFile:
    weightedGraph.tofile(weightedGraphFile)

print(weightedGraph)
