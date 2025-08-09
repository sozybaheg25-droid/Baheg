import os
import tweepy
import csv
import requests
import random
from datetime import datetime
import time

print("=== Starting Twitter Bot ===")
print(f"Execution time: {datetime.utcnow().isoformat()} UTC")

# Load credentials
API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
SHEET_URL = os.environ['SHEET_URL']

# Create Twitter client
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Test authentication
try:
    user = client.get_me(user_auth=True)
    username = user.data.username
    print(f"Authenticated as: @{username}")
except Exception as e:
    print(f"❌ Authentication failed: {str(e)}")
    raise

def fetch_untweeted_rows():
    """Fetch rows from Google Sheet that haven't been tweeted"""
    try:
        response = requests.get(SHEET_URL)
        response.raise_for_status()
        
        # Parse CSV data
        reader = csv.reader(response.text.splitlines())
        rows = list(reader)
        
        # Find untweeted rows (Column B empty)
        untweeted = []
        for i, row in enumerate(rows):
            # Skip header row and empty rows
            if i == 0 or not row or len(row) < 2: 
                continue
                
            # Check if tweeted (Column B should be empty)
            if len(row) < 2 or not row[1].strip():
                untweeted.append({
                    "index": i,
                    "text": row[0].strip()[:280],  # Truncate to 280 chars
                    "row": row
                })
                
        print(f"📊 Found {len(untweeted)} untweeted rows")
        return untweeted, rows
        
    except Exception as e:
        print(f"❌ Sheet fetch error: {str(e)}")
        return [], []

def update_sheet_status(row_index, tweet_id):
    """Update Google Sheet with tweet status (requires Google Sheets API)"""
    # This is placeholder logic - see note below
    print(f"📝 Would update row {row_index} with tweet ID {tweet_id}")
    print("ℹ️ Actual update requires Google Sheets API implementation")

def tweet_new_messages():
    """Tweet new messages from sheet and mark them as tweeted"""
    untweeted, all_rows = fetch_untweeted_rows()
    
    if not untweeted:
        print("✅ No new tweets to send")
        return
        
    # Select one random untweeted message
    message = random.choice(untweeted)
    print(f"✏️ Selected tweet: '{message['text']}' ({len(message['text'])} chars)")
    
    try:
        # Send tweet
        response = client.create_tweet(text=message['text'])
        tweet_id = response.data['id']
        print(f"🐦 Successfully tweeted! ID: {tweet_id}")
        print(f"🔗 Link: https://twitter.com/{username}/status/{tweet_id}")
        
        # Update sheet (conceptual - see implementation note)
        update_sheet_status(message['index'], tweet_id)
        return True
        
    except tweepy.TweepyException as e:
        print(f"❌ Twitter error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

# Run the main function
if __name__ == "__main__":
    success = tweet_new_messages()
    print(f"🏁 Execution {'succeeded' if success else 'failed'}")
