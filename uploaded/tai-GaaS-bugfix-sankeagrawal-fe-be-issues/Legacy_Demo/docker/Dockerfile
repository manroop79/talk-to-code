FROM ubuntu:latest
ENV DEBIAN_FRONTEND noninteractive

# RUN apt-get update -y && apt-get install curl
RUN apt-get update --yes && apt-get upgrade --yes 
RUN apt-get install nano software-properties-common gnupg2 python3-pip --yes

WORKDIR /app

ADD installation_media .

# Separating out requirements installs as they are commonly changed
RUN python3 -m pip install -r requirements.txt
