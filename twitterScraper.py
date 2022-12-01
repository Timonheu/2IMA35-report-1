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

    followers = client.get_users_following(user.data.id, max_results=1000)
    counter = 0
    for data in followers.data:
        print(data.username)
        counter += 1
    if counter == 1000:
        print("AAAH " + handle + "volgt te veel mensen")
