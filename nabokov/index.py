import os
import json
import tweepy
import requests
from dotenv import load_dotenv
from kafka import KafkaConsumer


def getApiInstance():
    consumer_key = os.getenv("TWT_CONSUMER_KEY")
    consumer_secret = os.getenv("TWT_CONSUMER_KEY_SECRET")
    access_token = os.getenv("TWT_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWT_ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)


def tweetImg(src, desc, api, id):
    filename = "%s.jpg".format(id)
    # download the image locally
    r = requests.get(src, stream=True)
    if r.status_code == 200:
        with open(filename, "wb") as file:
            for chunk in r:
                file.write(chunk)
        # tweet & delete ( ͡° ͜ʖ ͡°)
        media = api.simple_upload(filename)
        os.remove(filename)
        print(media)
        api.update_status(desc, media_ids=[media.media_id])
    else:
        print("failed to tweet image: ", src)


print("hi0")
if __name__ == "__main__":
    # init env
    load_dotenv()
    KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
    MARS_COLOR_TOPIC = os.environ.get("MARS_COLOR_TOPIC")

    HANDLE = "marskafka"
    api = getApiInstance()

    consumer = KafkaConsumer(
        MARS_COLOR_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda val: json.loads(val),
    )
    print("hi1")
    for message in consumer:
        print(message.value)

        desc = "{} sols into {}'s mission, we received this picture from its {} camera!".format(
            message.value["sol"], message.value["rover_name"], message.value["camera"]
        )

        tweetImg(
            message.value["img_info"]["output_url"],
            desc,
            api,
            message.value["img_info"]["id"],
        )
