# marskafka

Marskafka is a Kafka data processing pipeline that uses deep learning to colorize & [tweet images](https://twitter.com/marskafka) from NASA’s Mars Rover API
1. Images from our Mars Rovers are consumed from NASA's API and are filtered between two topics:
- `queue.bwimg` for greyscale images
- `stream.colorimg` for RGB images
2. An instance of the [deoldify](https://github.com/jantic/DeOldify) deep learning network listens to the greyscale queue, colorizes the images, and forwards them to the colored stream
3. Both topics will them merge at nabokov– a [twitter bot](https://twitter.com/marskafka) that takes 3 images from the current epoch (daily) and tweets them to [this account](https://twitter.com/marskafka)

I built this to learn about distributed computing, publish/subscribe models, and stream processing

## Codebase structure

| Directory              |      Description          |
| :-------------------- | :-----------------------: |
| [pushkin](pushkin)    | HTTP service that consumes Mars API & pipes to kafka     |
| [tolstoy](tolstoy)    | Deep learning service                 |
| [nabokov](nabokov)    | Twitter Bot                           |

## Notes
- i had initially wanted to deploy and expose my own instance of [deoldify](https://github.com/jantic/DeOldify) and use my own API keys
- however, i misjudged the complexity of this task:

![meme](https://i.ibb.co/6NwZ806/5ornlp.jpg)
- so i'm temporarily using [this api](https://deepai.org/machine-learning-model/colorizer) for my colorization needs, as i don't have the time to dive into MLOps with AWS Lambda, and AWS SageMaker, 
