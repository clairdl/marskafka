import os
import tweepy
from dotenv import load_dotenv


def getApiInstance():
    consumer_key = os.getenv("TWT_CONSUMER_KEY")
    consumer_secret = os.getenv("TWT_CONSUMER_KEY_SECRET")
    access_token = os.getenv("TWT_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWT_ACCESS_TOKEN_SECRET")
    print(consumer_key, type(consumer_key))

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)

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

        api.update_with_media(
            filename, status=f"tweeting live from warm and sunny colorado!"
        )
        os.remove(filename)
    else:
        print("image download failed, src: ", src)


if __name__ == "__main__":
    # init env
    load_dotenv()
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
