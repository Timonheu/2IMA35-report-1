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

# Perform clustering
# Compute number of clusters (= different parties)
parties = set()
for i in range(peopleCount):
    parties.add(followingGraphMetadata[i]["partij"])

i, graph, yhats, contracted_leader, mst = affinity_clustering(weightedGraph, len(parties))

print(mst)