# create from base image
FROM python:3.6.9

RUN pip install kafka-python

# copy in scripts
COPY consumer.py /consumer.py

# run command on boot
# CMD ["python3", "/consumer.py"]
