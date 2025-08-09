import os
import tweepy
import random
from datetime import datetime

print("=== Starting Twitter Bot ===")
print(f"Execution time: {datetime.utcnow().isoformat()} UTC")

# Twitter credentials
API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

print("Credentials loaded successfully")

# Create v2 client
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Test authentication
try:
    user = client.get_me(user_auth=True)
    print(f"Authenticated as: @{user.data.username} (ID: {user.data.id})")
except Exception as e:
    print(f"Authentication failed: {str(e)}")
    raise

# Tweet messages
messages = [
    "Hello Twitter! 🤖 Automated tweet from GitHub Actions",
    "Testing my auto-tweet system 🚀",
    "This tweet was scheduled using GitHub Actions ⚙️",
    "GitHub Actions + Twitter API = 💙",
    "Success! My auto-tweet works! 🎉",
    "Exploring the power of automation 🤖💬",
    "Digital birds singing automated songs 🐦🎶",
    "Code to cloud to tweet - fully automated! ☁️➡️🐦"
]

# Select random message
message = random.choice(messages)
print(f"Selected tweet: '{message}' ({len(message)} characters)")

# Send tweet
try:
    response = client.create_tweet(text=message)
    print(f"Successfully tweeted! Tweet ID: {response.data['id']}")
    print(f"Link: https://twitter.com/{user.data.username}/status/{response.data['id']}")
except tweepy.TweepyException as e:
    print(f"Twitter API error: {e}")
    # Extract error details
    if e.api_codes:
        print(f"API error codes: {e.api_codes}")
    if e.api_messages:
        print(f"API messages: {e.api_messages}")
    raise
except Exception as e:
    print(f"Unexpected error: {str(e)}")
    raise

print("=== Execution completed successfully ===")
