import os
import tweepy
import time

# Twitter credentials
API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

# Authenticate
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Simple tweet content
tweets = [
    "Hello Twitter! 🤖 Automated tweet from GitHub Actions",
    "Testing my auto-tweet system 🚀",
    "This tweet was scheduled using GitHub Actions ⚙️",
    "GitHub Actions + Twitter API = 💙",
    "Success! My auto-tweet works! 🎉"
]

# Get current day to rotate tweets
current_index = int(time.strftime("%d")) % len(tweets)
message = tweets[current_index]

# Send tweet
try:
    api.update_status(message)
    print(f"Successfully tweeted: {message}")
except tweepy.TweepError as e:
    print(f"Twitter error: {e.reason}")
except Exception as e:
    print(f"Unexpected error: {str(e)}")