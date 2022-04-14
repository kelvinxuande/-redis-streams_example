from redisHelpers import redisProducer
import time
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-sc", "--startcounter", type=int, default=0)
    parser.add_argument("-tt", "--throttletime", type=int, default=2)
    parser.add_argument("-pn", "--producername", type=str, default="testProducer")
    args = parser.parse_args()
    args = vars(args)   # converts args to dictionary, access with ["key"]

    counter = args["startcounter"]
    throttleTime = args["throttletime"]
    producerName = args["producername"]

    # initialise redis producer
    rp = redisProducer(REDIS_HOSTNAME="localhost", REDIS_PORT=6379)
    
    while True:
        if rp.connected:

            for streamIndex in range(2):    # loop over 0, 1
                _stream_name = f"redis-stream-{str(streamIndex)}"
                data = {
                    "producerName": producerName,
                    "timeGenerated": int(time.time() * 1000),
                    "counter": counter,
                }
                successful = rp.put_streamData(stream_name=_stream_name, data=data)
                if not successful:
                    print(f"[WARN] Failed to put_streamData: {data}; into stream: {_stream_name}. \
                            Retrying connection handled by object.")

            print("#")
            time.sleep(throttleTime) # simulate doing some work
            counter = counter + 1
        else:
            print("[WARN] redisProducer is not yet connected to redis server")