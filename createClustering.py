import json
import sys

import numpy as np
np.set_printoptions(threshold=sys.maxsize)

from Code_Kees.AffinityClustering import affinity_clustering

# Load meta data
followingGraphMetadata = None
with open("Data/Output/followingGraphMetadata.json", "r") as graphFileMeta:
    followingGraphMetadata = json.load(graphFileMeta)
peopleCount = len(followingGraphMetadata)

# Load graph
weightedGraph = None
with open("Data/Output/weightedGraph.json", "r") as graphFile:
    weightedGraph = np.fromfile(graphFile).reshape(peopleCount, peopleCount)

# Make adjacency matrix into adjacency list
adjacencyList = []
for i in range(peopleCount):
    adjacencyListPersonI = []

    for j in range(peopleCount):
        if i == j:
            continue

        if weightedGraph[i][j] > 0:
            adjacencyListPersonI.append((j, weightedGraph[i][j]))

    adjacencyList.append((i, adjacencyListPersonI))

# Perform clustering
# Compute number of clusters (= different parties)
parties = set()
for i in range(peopleCount):
    parties.add(followingGraphMetadata[i]["partij"])

i, graph, yhats, contracted_leader, mst = affinity_clustering(adjacencyList, 1)


# Tree construction
childrenPerRun = []
for yhat in yhats:
    children = []
    for i in range(len(yhat)):
        childList = []
        for j in range(len(yhat)):
            if yhat[i] == yhat[j] and i != j:
                childList.append(j)
        children.append(childList)
    childrenPerRun.append(children)


print(mst)
