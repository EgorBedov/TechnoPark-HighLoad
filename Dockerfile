FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y --no-install-recommends apt-utils

RUN apt-get -y install python3-pip

RUN pip3 install pyinstaller

COPY . .

RUN cd src && rm main && pyinstaller -F main.py

EXPOSE 80

USER root

CMD ./build/bin/static_server --config files/static_server.conf
