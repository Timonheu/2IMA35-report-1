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
with open("Data/Output/RandomWalk-length-0.5sqrt-people-amount-42/weightedGraph.json", "r") as graphFile:
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
    "VVD": "#e6194b",
    "D66": "#3cb44b",
    "PVV": "#ffe119",
    "CDA": "#4363d8",
    "PVDA": "#f58231",
    "SP": "#911eb4",
    "Groenlinks": "#46f0f0",
    "PvDD": "#f032e6",
    "ChristenUnie": "#bcf60c",
    "FvD": "#fabebe",
    "DENK": "#008080",
    "Groep van Haga": "#e6beff",
    "JA21": "#9a6324",
    "SGP": "#fffac8",
    "Volt": "#800000",
    "BBB": "#aaffc3",
    "Bij1": "#808000",
    "Fractie Den Haan": "#ffd8b1",
    "Gündoğan": "#000075",
    "Omtzigt": "#808080"
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


# Quantify the quality of the clustering
# Level with the best amount of clusters
bestLevel = 0
# difference between the amount of clusters and 20
bestClusterDifference = 9999
parties = len(colourMap)

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
            clusteringGraphNodeColours.append("#000")

            nodeCount += 1

        nodeIndicesOnThisLevel[j] = newNodeIndices[originalNodeIndexRepresentingNodeJ]
        nodeJIndexThisLevel = nodeIndicesOnThisLevel[j]
        nodeJIndexPreviousLevel = nodeIndicesOnPreviousLevel[j]
        clusteringGraph.add_edge(nodeJIndexPreviousLevel, nodeJIndexThisLevel)

        # find the amount of clusters in this level
        clusters = len(set(yhats[level-1]))
        difference = abs(clusters - parties)
        if difference < bestClusterDifference:
            bestLevel = level
            bestClusterDifference = difference

    level += 1
    nodeIndicesOnPreviousLevel = nodeIndicesOnThisLevel

    # if level == 3:
    #     break

# output amount of clusters
chosenLevel = yhats[bestLevel-1]
clusters = len(set(chosenLevel))
print("\nNumber of clusters: " + str(clusters) + " at level " + str(bestLevel))

# now that we have the best level, we can calculate the rest
partySet = set()
for person in followingGraphMetadata:
    partySet.add(person["partij"])

# calculate and output a
aCumulative = 0.0  # cumulative value for a, will need to be averaged
for party in partySet:
    clusterSet = set()
    for i in range(len(chosenLevel)):
        if followingGraphMetadata[i]["partij"] == party:
            clusterSet.add(chosenLevel[i])
    aCumulative += 1/len(clusterSet)

a = aCumulative/len(partySet)
print("a equals: " + str(a))

# calculate and output b
clusterSet = set()  # set of all nodes that are leader of a cluster
for value in chosenLevel:
    clusterSet.add(value)

bCumulative = 0.0  # cumulative value for b, will need to be averaged
for leader in clusterSet:
    clusterPartySet = set()
    for i in range(len(chosenLevel)):
        if chosenLevel[i] == leader:  # means the node is in the cluster
            clusterPartySet.add(followingGraphMetadata[i]["partij"])
    bCumulative += 1/len(clusterPartySet)

b = bCumulative/clusters
print("b equals: " + str(b))

finalValue = (a/3) + (b/3) + ((1 - abs(clusters - len(partySet))/len(partySet))/3)
print("The final value equals: " + str(finalValue))

# #pos = nx.nx_agraph.graphviz_layout(clusteringGraph)
# pos = nx.planar_layout(clusteringGraph)
# f = plt.figure(figsize=(60, 60))
# nx.draw_networkx(clusteringGraph, with_labels=False, ax=f.add_subplot(111), pos=pos, node_color=clusteringGraphNodeColours)
# nx.draw_networkx_labels(clusteringGraph, pos, clusteringGraphNodeLabels)
# plt.show()
# f.savefig("Data/Output/ClusteringGraph.png")

