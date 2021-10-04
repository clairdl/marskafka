import os
import json
import sched, time
from io import BytesIO
from random import randint
from datetime import datetime

import requests
from PIL import Image
from dotenv import load_dotenv
from kafka import KafkaProducer

# gets images from nasa api and filters out images from undesirable cameras
def get_images():
    rovers = [
        {"name": "curiosity", "camera_whitelist": {"FHAZ", "RHAZ", "NAVCAM"}},
        {
            "name": "perseverance",
            "camera_whitelist": {
                "NAVCAM_LEFT",
                "NAVCAM_RIGHT",
                "FRONT_HAZCAM_LEFT_A",
                "FRONT_HAZCAM_RIGHT_A",
                "REAR_HAZCAM_LEFT",
                "REAR_HAZCAM_RIGHT",
            },
        },
    ]
    filtered = []

    for rover in rovers:
        # TODO: set req url to the 'latest photos' endpoint
        res = requests.get(
            "https://api.nasa.gov/mars-photos/api/v1/rovers/{}/photos?sol={}&api_key={}".format(
                rover["name"], 1998, os.getenv("NASA_API_KEY")
            )
        )

        res = res.json()
        
        filtered.extend(
            [
                {
                    "rover_name": i["rover"]["name"],
                    "sol": i["sol"],
                    "camera": i["camera"]["name"],
                    "img_src": i["img_src"],
                }
                for i in res["photos"]
                if i["camera"]["name"] in rover["camera_whitelist"]
            ]
        )

    return filtered


def is_greyscale_probable(img):
    r = requests.get(img["img_src"], stream=True)
    img = Image.open(BytesIO(r.content))
    img_rbg = img.convert("RGB")

    x, y = img.size
    x_step = x // 4
    y_step = y // 4

    # samples 9 pixels from the points of a grid: ((x//4 + y//4) - 1)^2 = 9
    for i in range(x_step, x, x_step):
        for j in range(y_step, y, y_step):
            print(x, i, y, j, img_rbg.getpixel((i,j)))
            r, g, b = img_rbg.getpixel((i, j))
            if r != g or g != b:
                return False
    return True


# since this is a simple producer that produces daily batches i _should_ make it an executable and schedule it with a cronjob, but i'm doing this to simulate a high-throughput data stream thus i'm going to keep the thread alive with sched:
# see: https://stackoverflow.com/a/93179
# tldr: if you pass time.sleep as the delayfunc, it blocks the thread
def main():
    KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
    MARS_BW_TOPIC = os.environ.get("MARS_BW_TOPIC")
    MARS_COLOR_TOPIC = os.environ.get("MARS_COLOR_TOPIC")

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda val: json.dumps(val).encode(),
    )

    images = get_images()

    for i in images:
        if is_greyscale_probable(i) == True:
            producer.send(MARS_BW_TOPIC, value=i)
            print("\nSENT TO TOPIC.BW:\n", i)
        else:
            producer.send(MARS_COLOR_TOPIC, value=i)
            print("\nSENT TO TOPIC.COLOR:\n", i)
        break

    s.enter(15, 1, main)  # TODO: set timer to once per day


if __name__ == "__main__":
    load_dotenv()
    # run main event loop immediately
    s = sched.scheduler(time.time, time.sleep)
    s.enter(1, 1, main)
    s.run()
