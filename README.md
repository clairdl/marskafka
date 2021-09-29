# marskafka
a kafka pipeline that pipes B&W Mars rover pics through a colorization neural network, and posts the results to twitter daily

## Codebase structure

| Directory             |      Description                      |
| :————————————————————:| :————————————————————————————————————:|
| [pushkin](pushkin)    | Consumes Mars API, pipes to kafka     |
| [tbd](tbd)            | Deep learning lambdas                 |
| [nabokov](nabokov)    | Twitter Bot                           |
| [kafka](kafka)        | Kafka pipeline & config               |

## notes

- havent figured out the deep learning stuff yet, i'm working on getting the end-to-end system operational
- will probably setup a seperate python service that consumes the kafka topics and either:
    - directly sends the images to [_nabokov_](nabokov)
    - or just sends it back through kafka
- will probably have to get another AWS free tier and look into some serverless computing services, so i don't have to mess around with any ML-ops stuff, i can just start calling lambdas on a pretrained network and consume an s3 bucket
    
