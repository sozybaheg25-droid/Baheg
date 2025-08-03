import os
import tweepy
from datetime import datetime

# Get Twitter credentials from GitHub secrets
API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

# Authenticate
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Customize your messages here
messages = [
    "هلا بالحلوين",
    "مين متواجد",

]

# Select message (rotate through list)
index = (datetime.utcnow().day % len(messages))
message = messages[index]

# Send tweet
try:
    api.update_status(message)
    print(f"Successfully tweeted: {message}")
except Exception as e:
    print(f"Error: {str(e)}")