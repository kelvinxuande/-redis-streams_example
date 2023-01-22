# create from base image
FROM python:3.6.9

RUN pip install kafka-python ntplib

# copy in scripts
COPY producer.py /producer.py

# run command on boot
# CMD ["python3", "/producer.py"]
