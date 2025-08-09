import os
import tweepy
import csv
import requests
import random
from datetime import datetime
import time
import sys

print("=== Starting Twitter Bot ===")
print(f"Execution time: {datetime.utcnow().isoformat()} UTC")

# Load credentials
API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
SHEET_URL = os.environ['SHEET_URL']

print(f"Environment variables loaded: SHEET_URL={SHEET_URL[:30]}...")

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
    print(f"✅ Authenticated as: @{username}")
except Exception as e:
    print(f"❌ Authentication failed: {str(e)}")
    raise

def fetch_untweeted_rows():
    """Fetch rows from Google Sheet that haven't been tweeted"""
    try:
        print(f"\n📥 Fetching Google Sheet from: {SHEET_URL}")
        start_time = time.time()
        response = requests.get(SHEET_URL)
        response_time = time.time() - start_time
        
        print(f"🔁 Response status: {response.status_code}")
        print(f"⏱️ Response time: {response_time:.2f}s")
        print(f"📄 Response size: {len(response.text)} characters")
        
        response.raise_for_status()
        
        # Print first 200 characters of response
        sample = response.text[:200].replace('\n', '\\n')
        print(f"📝 Sample response: '{sample}'...")
        
        # Parse CSV data
        reader = csv.reader(response.text.splitlines())
        rows = list(reader)
        
        print(f"\n📊 Found {len(rows)} total rows in CSV")
        
        # Print header row
        if rows:
            print(f"🔠 Header row: {rows[0]}")
        
        untweeted = []
        for i, row in enumerate(rows):
            # Skip header row
            if i == 0:
                continue
                
            # Skip empty rows
            if not row or len(row) == 0:
                continue
                
            # Print row structure
            print(f"\n🔍 Row {i} analysis:")
            print(f"  Raw row: {row}")
            print(f"  Columns: {len(row)}")
            
            # Check if at least first column exists
            if len(row) > 0 and row[0].strip():
                print(f"  Column 1: '{row[0]}'")
                
                # Check status column (if exists)
                status = ""
                if len(row) > 1:
                    status = row[1].strip()
                    print(f"  Column 2 (status): '{status}'")
                else:
                    print("  Column 2: Not present")
                    
                # Check if untweeted
                if not status:
                    print("✅ Row is untweeted!")
                    untweeted.append({
                        "index": i,
                        "text": row[0].strip()[:280],
                        "row": row
                    })
                else:
                    print("⏭️ Row already tweeted")
            else:
                print("❌ Row skipped - empty first column")
                
        print(f"\n📊 Found {len(untweeted)} untweeted rows")
        return untweeted, rows
        
    except Exception as e:
        print(f"❌ Sheet fetch error: {str(e)}", file=sys.stderr)
        return [], []

def tweet_new_messages():
    """Tweet new messages from sheet and mark them as tweeted"""
    untweeted, all_rows = fetch_untweeted_rows()
    
    if not untweeted:
        print("✅ No new tweets to send")
        return True
        
    # Select one random untweeted message
    message = random.choice(untweeted)
    print(f"\n✏️ Selected tweet: '{message['text']}' ({len(message['text'])} chars)")
    
    try:
        # Send tweet
        response = client.create_tweet(text=message['text'])
        tweet_id = response.data['id']
        print(f"🐦 Successfully tweeted! ID: {tweet_id}")
        print(f"🔗 Link: https://twitter.com/{username}/status/{tweet_id}")
        
        print(f"📝 Would update row {message['index']} with tweet ID")
        return True
        
    except tweepy.TweepyException as e:
        print(f"❌ Twitter error: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}", file=sys.stderr)
        return False

# Run the main function
if __name__ == "__main__":
    print("\n🚀 Starting tweet process")
    success = tweet_new_messages()
    print(f"\n🏁 Execution {'succeeded' if success else 'failed'}")
    exit(0 if success else 1)
