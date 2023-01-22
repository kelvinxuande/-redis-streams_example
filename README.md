# Reference Docker Kafka Pattern
This repository seeks to serve as a reference for using kafka as a means of communicating between docker containers. This setup was tested on Nvidia Jetson devices. An illustration of the setup used in this reference is shown below:

![basic-flowchart](images/basic-flowchart.PNG?raw=true)

1) Before testing the reference setup, please ensure that docker and docker-compose has been installed. A reference shell script for installation is [included](https://git.siotgov.tech/kelvintan/l4t_docker-kafka_example/src/branch/master/install_docker_compose.sh).
2) Starting reference setup with docker-compose:
`sudo docker-compose up --build`
and `ctrl-c` when you are done

Additional notes:
- Depending on the method of starting, you may find these [reference commands](https://docs.docker.com/compose/reference/) useful
`sudo docker-compose up -d [--build]`
`sudo docker-compose down --rmi all`
- To reference the underlying docker commands, use [docker-without-compose.txt](https://git.siotgov.tech/kelvintan/l4t_docker-kafka_example/src/branch/master/docker-without-compose.txt) as a starting reference
