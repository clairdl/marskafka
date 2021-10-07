# marskafka

Marskafka is a distributed kafka network with 3 docker-composed microservices that interact with eachother through kafka's message brokering system. The general flow is:
1. Images from our dearest little Mars rovers up above, of which the majority are greyscale, are consumed from a NASA API and are filtered between two topics:
- `queue.bwimg` for greyscale images
- `stream.colorimg` for RGB images
2. An instance of the [deoldify](https://github.com/jantic/DeOldify) deep learning network listens to the greyscale queue, colorizes, and forwards to the colored queue
3. Both topics will them merge at nabokov– where a [twitter bot](https://twitter.com/marskafka) ranks images from the current epoch (daily) and tweets the "most interesting" one (this is subjective of course, but I'm currently ranking by image noise)

It was written for educational purposes to learn about Kafka, pub/sub models, and stream processing; it would be quite the comical example of over-engineering otherwise!

## Codebase structure

| Directory              |      Description          |
| :-------------------- | :-----------------------: |
| [pushkin](pushkin)    | HTTP service that consumes Mars API & pipes to kafka     |
| [tolstoy](tolstoy)    | Deep learning service                 |
| [nabokov](nabokov)    | Twitter Bot                           |

## Notes
- i had initially wanted to deploy and expose my own instance of [deoldify](https://github.com/jantic/DeOldify), using my own API keys
- however, i misjudged the complexity of this task:

![meme](https://i.ibb.co/6NwZ806/5ornlp.jpg)
- so i'm temporarily using [this api](https://deepai.org/machine-learning-model/colorizer) for my colorization needs, as i don't have the time to dive into MLOps with AWS Lambda, and AWS SageMaker, 
