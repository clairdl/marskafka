import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

# check .env.example details
auth = tweepy.OAuthHandler(os.getenv('TWT_CONSUMER_KEY'), os.getenv('TWT_CONSUMER_KEY_SECRET'))
auth.set_access_token(os.getenv('TWT_ACCESS_TOKEN'), os.getenv('TWT_ACCESS_TOKEN_SECRET'))

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("200")
except:
    print("err")