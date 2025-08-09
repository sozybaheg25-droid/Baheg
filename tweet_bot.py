import os
import tweepy
import random
from datetime import datetime

# Twitter credentials
API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

# Create v2 client
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Tweet messages
messages = [
    "Hello Twitter! 🤖 Automated tweet from GitHub Actions",
    "Testing my auto-tweet system 🚀",
    "This tweet was scheduled using GitHub Actions ⚙️",
    "GitHub Actions + Twitter API = 💙",
    "Success! My auto-tweet works! 🎉"
]

# Select random message
message = random.choice(messages)

try:
    # Post tweet using v2 API
    response = client.create_tweet(text=message)
    print(f"Successfully tweeted: {message}")
    print(f"Tweet ID: {response.data['id']}")
except tweepy.TweepyException as e:
    print(f"Twitter error: {e}")
except Exception as e:
    print(f"Unexpected error: {str(e)}")
