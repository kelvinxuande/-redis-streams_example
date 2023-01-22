import time
from json import loads
from kafka import KafkaConsumer
import logging

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
        consumer = KafkaConsumer(
                    'timed_id',
                    # whether to connect from connected docker container or dockerhost (localhost)
                    # bootstrap_servers='kafka:9093',
                    bootstrap_servers='localhost:9092',
                    # whether to start receving from the earliest message or from the latest
                    auto_offset_reset='earliest',
                    # auto_offset_reset='latest',
                    enable_auto_commit=True, 
                    group_id='consumer_group_1',
                    value_deserializer=lambda x: loads(x.decode('utf-8'))
                )
        successfully_connected = True
    except:
        streamLogger.info("Waiting for successful connection")
        time.sleep(check_interval)

out_sync_time = 5
streamLogger.info("Sleeping for {} seconds to simulate out-of-sync starts".format(out_sync_time))
time.sleep(out_sync_time)

for message in consumer:
    # streamLogger.info(message)
    extracted_message = message.value
    streamLogger.info(extracted_message)
    streamLogger.info("Treat new messages as trigger and do some processing with each message here")
