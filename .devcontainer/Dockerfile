FROM ubuntu:bionic

LABEL maintainer="lager_gcs@outlook.com"
LABEL description="Dev Environment for GUST."

ARG USER_UID=1000
ARG USER_GID=1000

RUN apt-get update \
    && apt-get install -y --no-install-recommends software-properties-common \
    && rm -rf /var/lib/apt/lists/*
RUN add-apt-repository -y ppa:deadsnakes/ppa
    

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    git \
    ruby \
    ruby-dev \
    rubygems \
    python3.7 \
    python3-dev \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 2 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1 \
    && update-alternatives  --set python /usr/bin/python3.7

RUN wget https://bootstrap.pypa.io/get-pip.py \
    && python get-pip.py

# Packages required for gust
RUN python -m pip install \
    numpy \
    PyQt5 \
    pyinstaller==4.9 \
    requests \
    werkzeug==2.0.3 \
    pyserial \
    scipy \
    pillow \
    dronekit \
    pyqtgraph \
    PyQt5-Tools \
    flask \
    flask-restx \
    gunicorn 

RUN wget https://bootstrap.pypa.io/get-pip.py \
    && python get-pip.py

COPY entrypoint.bash /
RUN chmod +x /entrypoint.bash
WORKDIR /workspace
ENTRYPOINT ["/bin/bash", "-c", "/entrypoint.bash"]

