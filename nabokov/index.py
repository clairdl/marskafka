import os
import tweepy
from dotenv import load_dotenv

if __name__ == "__main__":
    # init env
    load_dotenv()
    consumer_key = os.getenv("TWT_CONSUMER_KEY")
    consumer_secret = os.getenv("TWT_CONSUMER_KEY_SECRET")
    access_token = os.getenv("TWT_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWT_ACCESS_TOKEN_SECRET")
    KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
    MARS_COLOR_TOPIC = os.environ.get("MARS_COLOR_TOPIC")

    HANDLE = "marskafka"
    api = getApiInstance()
    imgid = 0

    consumer = KafkaConsumer(
        MARS_COLOR_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda val: json.loads(val),
    )

    for message in consumer:
        print(message.value)


def getApiInstance():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    try:
        api.verify_credentials()
        # only save client instance if credentials are valid
        api = tweepy.API(auth)
        print("twitter auth successful")
    except:
        raise PermissionError(
            "err in <nabokov/index.py> `authenticate()`: twitter auth failed, check your credentials in `.env` and run again \n"
        )
    return api


def tweetImg(src, text):
    filename = f"{imgid}.jpg"
    imgid += 1
    r = requests.get(src, stream=True)
    if r.status_code == 200:
        file = open(filename, "wb")
        try:
            for chunk in r:
                file.write(chunk)
        finally:
            file.close()

        api.update_with_media(filename, status=f"tweeting live from warm and sunny colorado")
        os.remove(filename)
    else:
        print("image download failed, src: ", src)
