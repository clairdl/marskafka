# marskafka - blogpost soon! (lots of yummy diagrams included)
a kafka pipeline that beams black and white Mars rover pics through [deoldify](https://github.com/jantic/DeOldify), a colorization neural network, and posts the results to twitter daily

http service ––> kafka.topic.**imgbw**.queue –––> deep learning processor ––> kafka.topic.**imgcolorw**.queue ––> twitter bot!

## Codebase structure

| Directory              |      Description          |
| :-------------------- | :-----------------------: |
| [pushkin](pushkin)    | HTTP service that consumes Mars API & pipes to kafka     |
| [tolstoy](tolstoy)    | Deep learning service                 |
| [nabokov](nabokov)    | Twitter Bot                           |

## notes
- i had initially wanted to deploy and expose my own instance of [deoldify](https://github.com/jantic/DeOldify), using my own API keys
- however, i misjudged the complexity of this task:

![meme](https://i.ibb.co/6NwZ806/5ornlp.jpg)
- and although it sounds fun, i don't currently have time to deep dive into devops, AWS Lambda, and AWS SageMaker, so i'm temporarily using [this api](https://deepai.org/machine-learning-model/colorizer) for my colorization deep learning needs
