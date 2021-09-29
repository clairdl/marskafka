import os
import sched, time

from kafka import KafkaProducer
import requests

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL)

# get images from nasa api and clean the response
def getImages():
  pass

# SEND IT
def postToKafkaTopic():
  pass

# schedule another mainLoop tmr
def addCronjob():
  pass

# pipe get images to kafka, handle errors, etc
def main():
  pass

if __name__ == "__main__":
  main()
