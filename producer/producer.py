import time
from json import dumps
from kafka import KafkaProducer
import logging

import ntplib
from time import ctime
c = ntplib.NTPClient()

def _setup_logger():
    ### see streamReceiver for complete example on comprehensive logging
    # get logger
    streamLogger = logging.getLogger(__name__)
    # set level
    streamLogger.setLevel(logging.INFO)
    # setup logger format
    formatter = logging.Formatter('%(asctime)s|%(name)s|%(message)s')
    # setup a stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    streamLogger.addHandler(stream_handler)
    return streamLogger

streamLogger = _setup_logger()

check_interval = 3
successfully_connected = False

while not successfully_connected:
    try:
        producer = KafkaProducer(
            # bootstrap_servers='kafka:9093',
            bootstrap_servers='localhost:9092',
            value_serializer=lambda x: dumps(x).encode('utf-8')
        )
        successfully_connected = True
        print("successfully connected to bootstrap_servers!")
    except Exception as e:
        print(e)
        streamLogger.info("waiting for successful connection")
        time.sleep(check_interval)

idx = 0
while True:
    # sanity check internet connection from within container
    response = c.request('pool.ntp.org')

    data = { 
        'idx': idx, 
        'time-from-internet': str(ctime(response.tx_time)) 
        }
    producer.send('timed_id', value=data)
    streamLogger.info(data)
    time.sleep(1)
    idx += 1
