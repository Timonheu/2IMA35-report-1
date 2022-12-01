import tweepy

# Get the API keys
exec(open("twitter.conf").read())

# authenticate
client = tweepy.Client(bearerToken)

# people for which we will collect the people they follow
handleList = ["thierrybaudet"]

for handle in handleList:
    user = client.get_user(username=handle)

    # API response contaning the people followed by this politician
    followedResponse = client.get_users_following(user.data.id, max_results=1000)
    followed = []
    # Add the username of each followed person to the list
    for data in followedResponse.data:
        followed.append(data.username)
    if len(followed) == 1000:
        # This means the limit of our request was reached and the politician follows at least 1000 people
        print("AAAH " + handle + " volgt te veel mensen")

    # list of indexes in handleList of people that this person follows
    indexList = []
    for politician in followed:
        if politician in handleList:
            index = handleList.index(politician)
