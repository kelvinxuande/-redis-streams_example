# Reference Docker Redis Pattern

## Introduction
A message broker to facillitate lossless messaging. The intent is to replace the [previous solution](https://git.siotgov.tech/kelvintan/l4t_docker-kafka_example) implemented with Kafka; with this one implemented with Redis. From preliminary tests, this solution fulfills the same set of common project requirements at lower RAM and disk memory usage.

For a primer on redis streams, please visit this [link](https://redis.io/topics/streams-intro).
This repository shows an example of how redis can be used in projects to facillitate lossless messaging between local components e.g. docker containers and to the cloud. The architecture of the example is self-explanatory and as follows:

![diagram](diagram.JPG?raw=true)

## Run Example

1. Pull repository code:
    
    `git pull https://git.siotgov.tech/kelvintan/redis-streams_example.git`

2. Pulling the required docker image:
    
    `docker pull redis:latest/ redis:7.0-rc2`

3. Make directory for local on-disk data to be stored in:
    ```
    mkdir data/
    cd data/
    mkdir redis-server-data/
    ```

4. (If required) install redis cilent for python in runtime environment

    `pip3 install redis==3.5.3`
    
5. Start redis container:

    `docker run -d --rm --net host --name local-redis-server -v /home/<user>/data/redis-server-data/:/data redis:7.0-rc1 redis-server /data/redis.conf --loglevel warning`
    
6. Open 3 other terminals, 1 for example producer, 2 for example consumers:

    ```
    python3 producer.py -sc 0
    python3 consumer.py -cn redis-stream-0
    python3 consumer.py -cn redis-stream-1
    ```
