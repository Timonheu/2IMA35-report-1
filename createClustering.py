import json
import sys
import networkx as nx
import matplotlib.pyplot as plt

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

# Create colour map
colourMap = {
    "VVD": "#FF7609",
    "D66": "#ADD5B0",
    "PVV": "#002961",
    "CDA": "#28B445",
    "PVDA": "#E40006",
    "SP": "#EC1B23",
    "Groenlinks": "#39A935",
    "PvDD": "#00743C",
    "ChristenUnie": "#00a7eb",
    "FvD": "#B02520",
    "DENK": "#00B7B2",
    "Groep van Haga": "#FFC0CB",
    "JA21": "#242B57",
    "SGP": "#E95E10",
    "Volt": "#502379",
    "BBB": "#95C11F",
    "Bij1": "#FFFF00",
    "Fractie Den Haan": "#8B4513",
    "Gündoğan": "#DCDCDC",
    "Omtzigt": "#4169E1"
}

# Perform clustering
i, graph, yhats, contracted_leader, mst = affinity_clustering(adjacencyList, 1)

# Create a plot of the hierarchical clustering
clusteringGraph = nx.Graph(name="Tweede Kamer Clustering")
clusteringGraphNodeLabels = {}
clusteringGraphNodeColours = []
nodeCount = 0

# Add vertices for bottom layer
nodeRepresentationOnBaseLevel = {}  # Contains per original node the index of the node in clusteringGraph that represents that node
for i in range(peopleCount):
    clusteringGraph.add_node(nodeCount)
    nodeRepresentationOnBaseLevel[i] = nodeCount


    personI = followingGraphMetadata[i]
    identifier = personI["naam"] + " - " + personI["partij"]
    clusteringGraphNodeLabels[nodeCount] = identifier
    clusteringGraphNodeColours.append(colourMap[personI["partij"]])

    nodeCount += 1

# Add the layers of the clustering
nodeIndicesOnPreviousLevel = nodeRepresentationOnBaseLevel # Contains per original node the index of the node in clusteringGraph on the previous level which represents that node
level = 1
for yhat in yhats:
    newNodeIndices = dict()
    nodeIndicesOnThisLevel = {} # Contains per original node the index of the node in clusteringGraph on the current level which represents that node
    for j in range(peopleCount):
        originalNodeIndexRepresentingNodeJ = yhat[j]

        if originalNodeIndexRepresentingNodeJ not in newNodeIndices:
            clusteringGraph.add_node(nodeCount)
            newNodeIndices[originalNodeIndexRepresentingNodeJ] = nodeCount

            originalNodeRepresentingNodeJ = followingGraphMetadata[originalNodeIndexRepresentingNodeJ]
            identifier = originalNodeRepresentingNodeJ["naam"] + " - " + originalNodeRepresentingNodeJ["partij"] + " - level " + str(level)
            clusteringGraphNodeLabels[nodeCount] = identifier
            clusteringGraphNodeColours.append(colourMap[originalNodeRepresentingNodeJ["partij"]])

            nodeCount += 1

        nodeIndicesOnThisLevel[j] = newNodeIndices[originalNodeIndexRepresentingNodeJ]
        nodeJIndexThisLevel = nodeIndicesOnThisLevel[j]
        nodeJIndexPreviousLevel = nodeIndicesOnPreviousLevel[j]
        clusteringGraph.add_edge(nodeJIndexPreviousLevel, nodeJIndexThisLevel)

    level += 1
    nodeIndicesOnPreviousLevel = nodeIndicesOnThisLevel

#pos = nx.nx_agraph.graphviz_layout(clusteringGraph)
pos = nx.planar_layout(clusteringGraph)
f = plt.figure(figsize=(40, 40))
nx.draw_networkx(clusteringGraph, with_labels=False, ax=f.add_subplot(111), pos=pos, node_color=clusteringGraphNodeColours)
nx.draw_networkx_labels(clusteringGraph, pos, clusteringGraphNodeLabels)
plt.show()
f.savefig("Data/Output/ClusteringGraph.png")

