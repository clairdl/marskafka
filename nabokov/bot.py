import os
import tweepy
from dotenv import load_dotenv


class MarsKafkaTwitterClient():
    handle = "marskafka"
    config = {}  # auth keys will be injected here

    def __init__(self):
        self.authenticate()

    def authenticate(self):
        # load env vars and inject keys into self.config
        load_dotenv()
        self.config["consumer_key"] = os.getenv("TWT_CONSUMER_KEY")
        self.config["consumer_secret"] = os.getenv("TWT_CONSUMER_KEY_SECRET")
        self.config["access_token"] = os.getenv("TWT_ACCESS_TOKEN")
        self.config["access_token_secret"] = os.getenv("TWT_ACCESS_TOKEN_SECRET")
        # authenticate with twitter
        self.auth = tweepy.OAuthHandler(
            self.config["consumer_key"], self.config["consumer_secret"]
        )
        self.auth.set_access_token(
            self.config["access_token"], self.config["access_token_secret"]
        )
        try:
            self.api.verify_credentials()
            # only save client instance if credentials are valid
            self.api = tweepy.API(auth)
            print('all is well')
        except:
            print("\n twitter 0auth failed, check your credentials and run again \n")

if __name__ == '__main__':
    newClient = MarsKafkaTwitterClient()