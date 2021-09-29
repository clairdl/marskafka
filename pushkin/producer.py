import os
import sched, time

import requests
from dotenv import load_dotenv
from kafka import KafkaProducer
import json

load_dotenv()

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL)

# format url
def fReqUrl(rover, sol):
    return f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos?sol={sol}&api_key={os.getenv('NASA_API_KEY')}"


# get images from nasa api and clean the response
def getImages():
    r = requests.get(fReqUrl("curiosity", 2000))
    r = r.json()

    res = [
        {"id": i["id"], "camera": i["camera"]["name"], "img_src": i["img_src"]}
        for i in r["photos"]
    ]
    # res = [{
    #   "id": int
    #   "camera": string
    #   "img_src": string
    # }...]

    return res


# SEND IT
def postToKafkaTopic():
    pass


# schedule another mainLoop tmr
def addCronjob():
    pass


# pipe images to kafka, handle errors, etc
def main():
    pass


if __name__ == "__main__":
    print(getImages())
