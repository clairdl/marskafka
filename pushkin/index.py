import os
import sched, time
import json
import requests
from datetime import datetime
from random import randint
from dotenv import load_dotenv
from kafka import KafkaProducer

# format url
def fReqUrl(rover, sol):
    return f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos?sol={sol}&api_key={os.getenv('NASA_API_KEY')}"


# get images from nasa api and clean the response
def getImages():
    # TODO: better sampling from the api, support more cams and rovers
    whitelist = {
        "FHAZ",
        "RHAZ",
        "NAVCAM",
        "PANCAM" "FRONT_HAZCAM_LEFT_A",
        "FRONT_HAZCAM_RIGHT_A",
        "REAR_HAZCAM_LEFT",
        "REAR_HAZCAM_RIGHT",
    }
    r = requests.get(fReqUrl("curiosity", 2000))
    r = r.json()
    # e.g. https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=2000&api_key=
    res = [
        {"sol": i["sol"], "camera": i["camera"]["name"], "img_src": i["img_src"]}
        for i in r["photos"]
        if i["camera"]["name"] in whitelist
    ]
    return res

# since this is a simple producer that sends data in batches to Kafka, i _should_ make it an executable script and
# schedule it with a cronjob... but i'm doing this to simulate a high-throughput service that produces lots of
# data in streams, so i'm going to keep the thread alive with sched:
# see: https://stackoverflow.com/a/93179
# tldr: if you pass time.sleep as the delayfunc, it blocks the thread
def main():
    KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
    MARS_BW_TOPIC = os.environ.get("MARS_BW_TOPIC")

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda val: json.dumps(val).encode(),
    )


    r = getImages()
    if len(r) > 0:
        v = r[randint(0, len(r)-1)]
    else:
        v = []
    print('res: ', r, v)
    producer.send(MARS_BW_TOPIC, value=v)

    # for i in getImages():
    #     print("line 62 in pushkin/index.py: ", i)

    s.enter(15, 1, main)


if __name__ == "__main__":
    load_dotenv()
    # run main event loop immediately
    s = sched.scheduler(time.time, time.sleep)
    s.enter(1, 1, main)
    s.run()
