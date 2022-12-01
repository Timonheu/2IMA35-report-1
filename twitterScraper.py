import tweepy

# OAuth Authentication
exec(open("twitter.conf").read())

# auth = tweepy.OAuthHandler(apiKey, apiSecretKey)
# auth.set_access_token(accessToken, accessTokenSecret)
# api = tweepy.API(auth)
client = tweepy.Client(bearerToken)

handleList = ["thierrybaudet"]

for handle in handleList:
    user = client.get_user(username=handle)

    followerResponse = client.get_users_following(user.data.id, max_results=1000)
    followers = []
    for data in followerResponse.data:
        followers.append(data.username)
    if len(followers) == 1000:
        print("AAAH " + handle + " volgt te veel mensen")

    # list of indexes in handleList of people that this person follows
    indexList = []
    for follower in followers:
        if follower in handleList:
            index = handleList.index(follower)
