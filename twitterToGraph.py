from os import listdir
import json
import numpy as np

twitterScrapesDir = "Data/Output/TwitterScrape"
twitterScrapes = []

# Load all files
for scrapeFilePath in listdir(twitterScrapesDir):
    if scrapeFilePath.endswith(".json"):
        with open(twitterScrapesDir + "/" + scrapeFilePath, "r") as scrapeFile:
            scrape = json.load(scrapeFile)
            twitterScrapes.append(scrape)

# Create the graph based on the following relation
peopleCount = len(twitterScrapes)
followingGraph = np.zeros((peopleCount, peopleCount))   # followingGraph[i][j] ==> i follows j

for i in range(peopleCount):
    for j in range(peopleCount):
        # Person cannot follow himself
        if i == j:
            continue

        # Check if i follows j
        personI = twitterScrapes[i]
        personJ = twitterScrapes[j]
        if personJ["twitterHandle"] in personI["follows"]:
            followingGraph[i][j] = 1

# Write the graph to file
with open("Data/Output/followingGraph.json", "w") as outputFile:
    followingGraph.tofile(outputFile)

# Also write the people file on which the graph is based to file
with open("Data/Output/followingGraphMetadata.json", "w") as outputFile:
    twitterScrapesJson = json.dumps(twitterScrapes)
    outputFile.write(twitterScrapesJson)

print(followingGraph)