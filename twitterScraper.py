import tweepy
import json
import time

# Get the API keys
exec(open("twitter.conf").read())

# authenticate
client = tweepy.Client(bearerToken)

# people for which we will collect the people they follow
file = open("Data/politici.json")
politiciDict = json.load(file)

output = {}
counter = 0
for politician in politiciDict["politici"]:

    output[counter] = politician

    if not politician["heeftTwitter"]:
        counter += 1
        continue
    user = client.get_user(username=politician["twitterHandle"])

    # API response contaning the people followed by this politician
    followedResponse = client.get_users_following(user.data.id, max_results=1000)
    followed = []
    # Add the username of each followed person to the list
    for data in followedResponse.data:
        followed.append(data)
    while not followedResponse.meta.get("next_token") is None:
        # This there are more followers left
        nextToken = followedResponse.meta["next_token"]
        followedResponse = client.get_users_following(user.data.id, max_results=1000, pagination_token=nextToken)

    # list of indexes in handleList of people that this person follows
    indexList = []
    for person in followed:
        for politicus in politiciDict["politici"]:
            if person.username.lower() == politicus["twitterHandle"].lower():
                index = politiciDict["politici"].index(politicus)
                indexList.append(index)

    output[counter]["following"] = indexList
    counter += 1
    print(politician["naam"])
    time.sleep(1)

json_object = json.dumps(output)

with open("Results/Twitter Output/output.json", "w") as outfile:
    outfile.write(json_object)
