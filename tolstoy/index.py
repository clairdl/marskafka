import os
import json
import requests
from dotenv import load_dotenv

from kafka import KafkaConsumer, KafkaProducer

def deoldify(src):
  # TODO: using a public api for now but i want to deploy my own model on AWS
  r = requests.post(
      "https://api.deepai.org/api/colorizer",
      data={
          'image': src,
      },
      headers={'api-key': os.environ.get('DEEP_AI_KEY')}
  )
  return r.json()


if __name__ == '__main__':
    load_dotenv()

    KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
    MARS_BW_TOPIC = os.environ.get('MARS_BW_TOPIC')
    MARS_COLOR_TOPIC = os.environ.get('MARS_COLOR_TOPIC')

    consumer = KafkaConsumer(
        MARS_BW_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda val: json.loads(val),
    )
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda val: json.dumps(val).encode(),
    )
    print('heello???')
    for message in consumer:
        print("\n just consumed this: ", message.value)  # DEBUG
        r = deoldify(message.value['img_src'])
        print(r)
        producer.send(MARS_COLOR_TOPIC, value=r['output_url'])
        print("\n and produced this: ", r['output_url'])
