from dotenv import load_dotenv
load_dotenv()

print("API_KEY:", os.getenv('API_KEY') and "***exists***")
print("API_SECRET:", os.getenv('API_SECRET') and "***exists***")
print("ACCESS_TOKEN:", os.getenv('ACCESS_TOKEN') and "***exists***")
print("ACCESS_TOKEN_SECRET:", os.getenv('ACCESS_TOKEN_SECRET') and "***exists***")