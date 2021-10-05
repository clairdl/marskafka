import os
import time
import json
import sched
import random
from io import BytesIO

import tweepy
import requests
from PIL import Image
from dotenv import load_dotenv


def deoldify(src):
    r = requests.post(
        "https://api.deepai.org/api/colorizer",
        data={
            "image": src,
        },
        headers={"api-key": os.environ.get("DEEP_AI_KEY")},
    )
    return r.json()


def is_greyscale_probable(src):
    r = requests.get(src, stream=True)
    img = Image.open(BytesIO(r.content))
    img_rbg = img.convert("RGB")

    x, y = img.size
    x_step = x // 4
    y_step = y // 4

    # samples 9 pixels from the points of a grid: ((x//4 + y//4) - 1)^2 = 9
    for i in range(x_step, x, x_step):
        for j in range(y_step, y, y_step):
            r, g, b = img_rbg.getpixel((i, j))
            if r != g or g != b:
                return False
    return True


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
    now = int(time.time())
    rover_index = 0 if now % 2 == 0 else 1 # pseudo-randomise which rover we query for
    
    res = requests.get(
        "https://api.nasa.gov/mars-photos/api/v1/rovers/{}/latest_photos?api_key={}".format(
            rovers[rover_index]["name"], os.getenv("NASA_API_KEY")
        )
    )
    res = res.json()

    # return n whitelisted cam + greyscale images from i's rover
    return [
            {
                "rover_name": i["rover"]["name"],
                "sol": i["sol"],
                "earth_date": i["earth_date"],
                "camera": i["camera"]["name"],
                "img_src": i["img_src"],
            }
            for i in res["latest_photos"]
            if i["camera"]["name"] in rovers[rover_index]["camera_whitelist"]
            and is_greyscale_probable(i["img_src"])
        ]


def send_tweets(tweets):
    desc = "{} sols ({}) into {}'s mission, we received these picture from its {} camera!".format(
            tweets[0]["sol"], tweets[0]["earth_date"], tweets[0]["rover_name"], tweets[0]["camera"]
        )
    media_ids = []
    for tweet in tweets:
        filename = "{}.jpg".format(tweet["img_src"]["id"])
        # download the image locally
        r = requests.get(tweet["img_src"]["output_url"], stream=True)
        if r.status_code == 200:
            with open(filename, "wb") as file:
                for chunk in r:
                    file.write(chunk)
            media = twitterClient.simple_upload(filename)
            media_ids.append(media.media_id)
            os.remove(filename)
        else:
            print("failed at image download or something: ", src)
    
    twitterClient.update_status(desc, media_ids=media_ids)



def main():
    images = get_images()
    tweets = []
    # set sample size
    k = 1 if len(images) < 3 else 3
    # take k random elements
    for i in random.sample(images, k):
        # deoldify 
        i["img_src"] = deoldify(i["img_src"])
        tweets.append(i)
    # send it!
    if len(tweets) > 0: 
        send_tweets(tweets)
    # reschedule for tomorrow
    s.enter(5, 1, main)


if __name__ == "__main__":

    load_dotenv()
    auth = tweepy.OAuthHandler(
        os.getenv("TWT_CONSUMER_KEY"), os.getenv("TWT_CONSUMER_KEY_SECRET")
    )
    auth.set_access_token(
        os.getenv("TWT_ACCESS_TOKEN"), os.getenv("TWT_ACCESS_TOKEN_SECRET")
    )
    twitterClient = tweepy.API(auth)

    blacklist = {
        "1444262388534943744",
        "1444262425457430533",
        "1445063845819547653",
        "1445116483881762824",
        "1445116622209880072",
        "1445230777709449217",
        "1445195520813658113",
    }

    s = sched.scheduler(time.time, time.sleep)
    s.enter(1, 1, main)
    s.run()