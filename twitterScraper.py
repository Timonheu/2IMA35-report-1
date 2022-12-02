import tweepy
import json
import configparser
from os.path import exists

# Get the API keys
cp = configparser.ConfigParser()
cp.read("twitter.conf")
bearerToken = cp.get("Twitter", "bearerToken")

# Setup API connection
client = tweepy.Client(bearerToken)
client.wait_on_rate_limit = True

# Load file containing the people for which we want to collect the people they follow
people = open("Data/Input/TweedeKamer.json")
peopleDict = json.load(people)

# Per person, check if we have already scraped the followers, and if not, do so and write it to file
scrapedDirPath = "Data/Output/TwitterScrape"

for person in peopleDict["politici"]:
    # Cannot scrape if no twitter
    if not person["heeftTwitter"]:
        continue
    handle = person["twitterHandle"]

    # If already scraped, no need to do it again
    scrapeName = scrapedDirPath + "/" + handle.lower() + ".json"
    if exists(scrapeName):
        continue

    # Create a dictionary for the output
    outputPerson = dict(person)
    outputPerson["twitterHandle"] = handle.lower()
    outputPerson["follows"] = []

    # Request the people followed by person from the API
    user = client.get_user(username=handle)
    followedResponse = client.get_users_following(user.data.id, max_results=1000)
    # Add the username of each followed person to the list
    for data in followedResponse.data:
        outputPerson["follows"].append(data.username.lower())

    while not followedResponse.meta.get("next_token") is None:
        # This there are more followers left
        nextToken = followedResponse.meta["next_token"]
        followedResponse = client.get_users_following(user.data.id, max_results=1000, pagination_token=nextToken)
        for data in followedResponse.data:
            outputPerson["follows"].append(data.username.lower())

    # Write the scraped data to disk
    outputPersonJson = json.dumps(outputPerson)
    with open(scrapeName, "w") as outputFile:
        outputFile.write(outputPersonJson)
