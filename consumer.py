# https://redis-py.readthedocs.io/en/stable/commands.html#redis.commands.cluster.RedisClusterCommands.xrange

from redisHelpers import redisConsumer
import time
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-tt", "--throttletime", type=int, default=1)
    parser.add_argument("-cn", "--streamname", type=str, required=True) # redis-stream-0
    args = parser.parse_args()
    args = vars(args)   # converts args to dictionary, access with ["key"]

    throttleTime = args["throttletime"]
    streamName = args["streamname"]

    rc = redisConsumer(REDIS_HOSTNAME="localhost", REDIS_PORT=6379)

    while True:
        if rc.connected:

            resp = rc.fetch_latestData(stream_name=streamName)
            if type(resp) == type(tuple()):
                print(f"[DEBUG] Got resp: {resp}")
                key = resp[0]
                payload = resp[1]
                print(f"[DEBUG] Do some processing here with payload: {payload}")
                print(f"[DEBUG] Trying to delete data with key: {key} in streamName: {streamName} after processing message")
                successful = rc.delete_data(stream_name=streamName, key=key)
                if not successful:
                    print(f"[WARN] Failed to delete_data: {payload}; \
                        from stream: {streamName}. \
                            Retrying connection handled by object.")
            elif type(resp) == type(list()):
                # empty list
                print("[WARN] No data found in stream")
            else:
                # type None
                print("[WARN] redisConsumer not connected to redis server. Retrying connection handled by object.")

            time.sleep(throttleTime)    # simulate doing some work
        else:
            print("[WARN] redisConsumer is not yet connected to redis server")
