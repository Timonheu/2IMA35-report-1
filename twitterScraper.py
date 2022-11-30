import tweepy
import sys
import os
import wget

# OAuth Authentication
config = {}
exec(open("twitter.conf").read())

auth = tweepy.OAuthHandler(apiKey, apiSecretKey)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

handleList = ["thierrybaudet"]

for handle in handleList:
    user = api.get_user(user_id=handle)
    followers = user.followers()
    print(followers)
