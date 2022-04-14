from redis import Redis
import time

class redisProducer:
    def __init__(self, REDIS_HOSTNAME, REDIS_PORT, ttl=10000): # "localhost", 6379, set ttl back to 86400000 for 24 hours in ms
        self.REDIS_HOSTNAME = REDIS_HOSTNAME
        self.REDIS_PORT = REDIS_PORT
        self.ttl = ttl

        # initialise redis connection
        self.redisConnection = None
        self.connected = False
        self.getRedisConnection()

    def getRedisConnection(self):
        self.connected = False
        backoffTime = 1
        while not self.connected:
            # self.redisConnection = Redis(self.REDIS_HOSTNAME, self.REDIS_PORT, retry_on_timeout=True)
            self.redisConnection = Redis(self.REDIS_HOSTNAME, self.REDIS_PORT, decode_responses=True)
            try:
                self.redisConnection.ping()
                self.connected = True
                print("[INFO] Successfully connected to redis server!")
            except Exception as e:
                print(f"[WARN] Error redis connection: {e}; retrying in {backoffTime} seconds")
                time.sleep(backoffTime)

    def put_streamData(self, stream_name, data):
        try:
            print(f"[DEBUG] stream_name: {stream_name}; data: {data}")

            insertedKey = self.redisConnection.xadd(stream_name, data)
            print(f"[DEBUG] Successfully inserted data into stream: {stream_name} with key: {insertedKey}")

            # timeTarget = int(time.time() * 1000) - self.ttl
            # numDeleted = self.redisConnection.xtrim(stream_name, approximate=False, minid=timeTarget)
            # print(f"[DEBUG] Number of items deleted from stream: {stream_name}: {numDeleted}")
            
            length = self.redisConnection.xlen(stream_name)
            print(f"[DEBUG] Current length of stream: {stream_name}: {length}")
            
            return True
        except ConnectionError as e:
            print(f"[WARN] Error redis connection: {e}; will retry getRedisConnection")
            self.getRedisConnection()
            return False


class redisConsumer:
    def __init__(self, REDIS_HOSTNAME, REDIS_PORT): # "localhost", 6379
        self.REDIS_HOSTNAME = REDIS_HOSTNAME
        self.REDIS_PORT = REDIS_PORT
        self.redisConnection = None
        self.connected = False
        self.getRedisConnection()

    def getRedisConnection(self):
        self.connected = False
        backoffTime = 1
        while not self.connected:
            self.redisConnection = Redis(self.REDIS_HOSTNAME, self.REDIS_PORT, retry_on_timeout=True, decode_responses=True)
            try:
                self.redisConnection.ping()
                self.connected = True
                print("[INFO] Successfully connected to redis server!")
            except Exception as e:
                print(f"[WARN] Error redis connection: {e}; retrying in {backoffTime} seconds")
                time.sleep(backoffTime)

    def fetch_latestData(self, stream_name):
        try:
            resp = self.redisConnection.xrevrange(
                name=stream_name, max='+', min='-', count=1
            )
            assert isinstance(resp, list)
            if len(resp) == 0:
                return resp # an empty list
            else:
                resp = resp[0]
                return resp # a tuple
        except ConnectionError as e:
            print(f"[WARN] Error redis connection: {e}; will retry getRedisConnection")
            self.getRedisConnection()
            return None

    def delete_data(self, stream_name, key):
        try:
            self.redisConnection.xdel(stream_name, key)
            return True
        except ConnectionError as e:
            print(f"[WARN] Error redis connection: {e}; will retry getRedisConnection")
            self.getRedisConnection()
            return False
