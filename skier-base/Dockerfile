FROM ubuntu:15.04
MAINTAINER eyesismine@gmail.com

# Install supervisord

RUN apt-get update

RUN apt-get install -y curl git nano wget mercurial

RUN apt-get -y install supervisor && \
    mkdir -p /var/log/supervisor && \
    mkdir -p /etc/supervisor/conf.d

# Make required directories
RUN mkdir /var/skier/

# Install dependencies
RUN apt-get -y install gnupg python3 virtualenv nodejs-legacy npm redis-server redis-tools python3.4-dev libyaml-dev pandoc

RUN npm install -g keybase-installer
RUN keybase-installer

# Setup virtualenv
RUN virtualenv -p /usr/bin/python3.4 /var/skier/venv

# Set virtualenv
ENV VIRTUAL_ENV="/var/skier/venv"
ENV PATH="/var/skier/venv/bin:$PATH"

# Install python dependencies
RUN pip install -r https://git.sundwarf.me/Skier/Skier/raw/master/requirements.txt

