import tweepy
import os
import random

# Get credentials from environment variables
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

# Auth & API setup
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Tweet messages list
messages = [
    "What is this?",
    "How is this?",
    "Yes it is!",
    "Hello Twitter!",
    "Automated tweet 👋",
]

# Send tweet
api.update_status(random.choice(messages))
