import os
import tweepy
import csv
import requests
import random
from datetime import datetime
import time
import io
import sys
import chardet
import json

print("=== Starting Twitter Bot ===")
print(f"Execution time: {datetime.utcnow().isoformat()} UTC")

# Load credentials
API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
SHEET_URL = os.environ['SHEET_URL']

print("✅ Environment variables loaded")

# Create Twitter client
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

def detect_encoding(content):
    """Detect encoding of byte content"""
    result = chardet.detect(content)
    encoding = result['encoding'] or 'utf-8'
    confidence = result['confidence']
    print(f"🔠 Detected encoding: {encoding} (confidence: {confidence:.2f})")
    return encoding

def fetch_untweeted_rows():
    """Fetch rows from Google Sheet that haven't been tweeted"""
    try:
        print(f"\n📥 Fetching Google Sheet from: {SHEET_URL}")
        response = requests.get(SHEET_URL)
        print(f"🔁 Response status: {response.status_code}")
        
        response.raise_for_status()
        
        # Detect and decode with proper encoding
        encoding = detect_encoding(response.content)
        try:
            decoded_content = response.content.decode(encoding)
        except UnicodeDecodeError:
            decoded_content = response.content.decode('utf-8', errors='replace')
        
        # Parse CSV
        csv_file = io.StringIO(decoded_content)
        reader = csv.reader(csv_file)
        rows = list(reader)
        
        print(f"📊 Found {len(rows)} total rows")
        
        untweeted = []
        for i, row in enumerate(rows):
            # Skip header row (i=0) and empty rows
            if i == 0 or not row or not row[0].strip():
                continue
                
            # Check if already tweeted (Column 2)
            if len(row) > 1 and row[1].strip():
                continue
                
            untweeted.append({
                "index": i,
                "text": row[0].strip()[:280],
                "sheet_row": i + 1  # Google Sheets rows are 1-indexed
            })
            
        print(f"✅ Found {len(untweeted)} untweeted rows")
        return untweeted
        
    except Exception as e:
        print(f"❌ Sheet fetch error: {str(e)}", file=sys.stderr)
        return []

def send_tweet(message):
    """Send a tweet and return tweet ID"""
    try:
        response = client.create_tweet(text=message)
        return response.data['id']
    except tweepy.TweepyException as e:
        print(f"❌ Twitter error: {e}")
        return None

def tweet_new_messages():
    """Tweet new messages from sheet"""
    untweeted = fetch_untweeted_rows()
    
    if not untweeted:
        print("✅ No new tweets to send")
        return True
        
    # Track successful tweets
    successful_tweets = 0
    
    # Try to send up to 1 tweets (if available)
    for _ in range(min(1, len(untweeted))):
        # Select random untweeted message
        message = random.choice(untweeted)
        untweeted.remove(message)  # Remove from selection pool
        
        print(f"\n✏️ Selected tweet: '{message['text']}'")
        
        # Send tweet
        tweet_id = send_tweet(message['text'])
        if not tweet_id:
            continue
            
        successful_tweets += 1
        print(f"🐦 Successfully tweeted! ID: {tweet_id}")
        
        # Add delay between tweets (avoid rate limits)
        time.sleep(5)
    
    print(f"\n🏁 Sent {successful_tweets} tweets")
    return successful_tweets > 0

# Run the main function
if __name__ == "__main__":
    print("\n🚀 Starting tweet process")
    success = tweet_new_messages()
    print(f"\n🏁 Execution {'succeeded' if success else 'failed'}")
    exit(0 if success else 1)

