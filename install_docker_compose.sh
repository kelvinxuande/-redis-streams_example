#!/bin/bash
#Install dependencies
sudo apt update -y
sudo apt install -y python3-pip

#Upgrade all necessary tools
pip3 install --upgrade setuptools
pip3 install --upgrade pip

#Install docker-compose
#note: safer way of installing as sudo apt install docker.io docker-compose installs an older version
pip3 install docker-compose