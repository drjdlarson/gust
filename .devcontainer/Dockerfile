FROM python:3.7

LABEL maintainer="lager_gcs@outlook.com"
LABEL description="Dev Environment for GUST."

ARG USER_UID=1000
ARG USER_GID=1000

ENV QT_QUICK_BACKEND=software

# workarounds for all the required tools 
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 libxcb-xinerama0 libxcb-cursor0 -y
RUN apt-get install '^libxcb.*-dev' libx11-xcb-dev libglu1-mesa-dev libxrender-dev libxi-dev libxkbcommon-dev libxkbcommon-x11-dev -y
RUN apt-get install -y mesa-utils libgl1-mesa-glx

# Packages required for GUST
RUN pip install \
    wheel \
    numpy \
    PyQt5 \
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

# Sphinx stuff required for generating documentation
RUN pip install \
    Sphinx \
    sphinx-rtd-theme \
    sphinxcontrib-apidoc \
    sphinxcontrib-applehelp \
    sphinxcontrib-htmlhelp \
    sphinxcontrib-jquery \
    sphinxcontrib-jsmath \
    sphinxcontrib-qthelp \
    sphinxcontrib-serializinghtml
     
# Google Chrome to view the generated documentation
RUN apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install ./google-chrome-stable_current_amd64.deb -y
    
# Script to run once the dev container is setup. See devcontainer.json and entrypoint.bash
COPY entrypoint.bash /
RUN chmod +x ./entrypoint.bash
WORKDIR /workspaces
