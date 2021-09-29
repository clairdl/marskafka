import os
import sched, time

import requests
from dotenv import load_dotenv
from kafka import KafkaProducer
import json

# format url
def fReqUrl(rover, sol):
    return f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos?sol={sol}&api_key={os.getenv('NASA_API_KEY')}"


# get images from nasa api and clean the response
def getImages():
    # todo: better sampling from the api, support more cams and rovers
    whitelist = {'FHAZ', 'RHAZ', 'NAVCAM', 'PANCAM' 'FRONT_HAZCAM_LEFT_A', 'FRONT_HAZCAM_RIGHT_A', 'REAR_HAZCAM_LEFT', 'REAR_HAZCAM_RIGHT' }
    r = requests.get(fReqUrl("curiosity", 2000))
    r = r.json()

    res = [
        {"sol": i["sol"], "camera": i["camera"]["name"], "img_src": i["img_src"]}
        for i in r["photos"] if i["camera"]["name"] in whitelist
    ]
    # res = [{
    #   "sol": int
    #   "camera": str
    #   "img_src": str
    # }...]
    print(res)
    return res


# schedule another mainLoop tmr
def addCronjob():
    pass


if __name__ == "__main__":
    load_dotenv()
    # had to hardcode the server address from docker config
    # because KAFKA_BROKER_URL is not in my env for some reason
    producer = KafkaProducer(
        bootstrap_servers="0.0.0.0:9092",
        value_serializer=lambda v: json.dumps(v).encode(),
    )

    for i in getImages():
        postToKafkaTopic(getImages())
        producer.send("queue.bwimgs", value=message.encode())
