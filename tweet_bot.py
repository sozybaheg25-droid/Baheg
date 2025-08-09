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
DEFAULT_COMMUNITY = os.environ.get('DEFAULT_COMMUNITY', '')  # Optional default community

print(f"Environment variables loaded: SHEET_URL={SHEET_URL[:30]}...")
if DEFAULT_COMMUNITY:
    print(f"Using default community: {DEFAULT_COMMUNITY}")

# Create Twitter client
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Create v1.1 API for community posting
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api_v1 = tweepy.API(auth)

# Test authentication
try:
    user = client.get_me(user_auth=True)
    username = user.data.username
    print(f"✅ Authenticated as: @{username}")
except Exception as e:
    print(f"❌ Authentication failed: {str(e)}")
    raise

def detect_encoding(content):
    """Detect encoding of byte content"""
    result = chardet.detect(content)
    encoding = result['encoding'] or 'utf-8'
    confidence = result['confidence']
    print(f"🔠 Detected encoding: {encoding} (confidence: {confidence:.2f})")
    return encoding

def fetch_untweeted_rows():
    """Fetch rows from Google Sheet with proper encoding"""
    try:
        print(f"\n📥 Fetching Google Sheet from: {SHEET_URL}")
        start_time = time.time()
        response = requests.get(SHEET_URL)
        response_time = time.time() - start_time
        
        print(f"🔁 Response status: {response.status_code}")
        print(f"⏱️ Response time: {response_time:.2f}s")
        print(f"📄 Response size: {len(response.content)} bytes")
        
        response.raise_for_status()
        
        # Detect and decode with proper encoding
        encoding = detect_encoding(response.content)
        try:
            decoded_content = response.content.decode(encoding)
        except UnicodeDecodeError:
            # Fallback to UTF-8
            print("⚠️ Decoding failed, trying UTF-8 fallback")
            decoded_content = response.content.decode('utf-8', errors='replace')
        
        # Print sample text
        sample = decoded_content[:200].replace('\n', '\\n')
        print(f"📝 Sample content: '{sample}'...")
        
        # Parse CSV with proper encoding
        csv_file = io.StringIO(decoded_content)
        reader = csv.reader(csv_file)
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
            if not row or len(row) == 0 or not row[0].strip():
                continue
                
            # Extract data from columns
            tweet_text = row[0].strip()[:280]
            status = row[1].strip() if len(row) > 1 else ""
            community_id = row[2].strip() if len(row) > 2 else DEFAULT_COMMUNITY
            
            # Check if already tweeted
            if status:
                print(f"⏭️ Row {i} skipped - already tweeted")
                continue
                
            print(f"✅ Row {i} is untweeted")
            untweeted.append({
                "index": i,
                "text": tweet_text,
                "community": community_id,
                "row": row
            })
                
        print(f"\n📊 Found {len(untweeted)} untweeted rows")
        return untweeted, rows
        
    except Exception as e:
        print(f"❌ Sheet fetch error: {str(e)}", file=sys.stderr)
        return [], []

def send_tweet(text, community_id):
    """Send tweet to specific community using Twitter API v1.1"""
    try:
        # Validate community ID format
        if community_id and not community_id.isdigit():
            print(f"⚠️ Invalid community ID: '{community_id}' - must be numeric")
            community_id = None
            
        # Create tweet parameters
        params = {"status": text}
        if community_id:
            params["community_id"] = community_id
            print(f"📢 Posting to community: {community_id}")
        else:
            print("🌐 Posting to public timeline")
            
        # Send tweet using v1.1 API
        status = api_v1.update_status(**params)
        tweet_id = status.id
        print(f"🐦 Successfully tweeted! ID: {tweet_id}")
        print(f"🔗 Link: https://twitter.com/{username}/status/{tweet_id}")
        return tweet_id
        
    except tweepy.TweepyException as e:
        # Extract error details
        errors = e.api_messages if hasattr(e, 'api_messages') else [str(e)]
        print(f"❌ Twitter error: {', '.join(errors)}", file=sys.stderr)
        
        # Log full error details for debugging
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_details = e.response.json()
                print(f"🔍 Error details: {json.dumps(error_details, indent=2)}")
            except:
                print(f"🔍 Raw error response: {e.response.text[:500]}")
                
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}", file=sys.stderr)
        return None

def tweet_new_messages():
    """Tweet new messages from sheet"""
    untweeted, all_rows = fetch_untweeted_rows()
    
    if not untweeted:
        print("✅ No new tweets to send")
        return True
        
    # Select one random untweeted message
    message = random.choice(untweeted)
    print(f"\n✏️ Selected tweet: '{message['text']}'")
    print(f"🏠 Community: {message['community'] or 'None'}")
    
    tweet_id = send_tweet(message['text'], message['community'])
    return tweet_id is not None

# Run the main function
if __name__ == "__main__":
    print("\n🚀 Starting tweet process")
    success = tweet_new_messages()
    print(f"\n🏁 Execution {'succeeded' if success else 'failed'}")
    exit(0 if success else 1)
