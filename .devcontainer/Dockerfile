FROM python:3.7

LABEL maintainer="lager_gcs@outlook.com"
LABEL description="Dev Environment for GUST."

ARG USER_UID=1000
ARG USER_GID=1000

ENV QT_QUICK_BACKEND=software

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 libxcb-xinerama0 libxcb-cursor0 -y
RUN apt-get install '^libxcb.*-dev' libx11-xcb-dev libglu1-mesa-dev libxrender-dev libxi-dev libxkbcommon-dev libxkbcommon-x11-dev -y
RUN apt-get install -y mesa-utils libgl1-mesa-glx

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


COPY entrypoint.bash /
RUN chmod +x /entrypoint.bash
# WORKDIR /workspaces

ENTRYPOINT ["/entrypoint.bash"]
CMD ["sleep", "infinity"]

# ENTRYPOINT ["/bin/bash"]
# ENTRYPOINT [ "/bin/bash", "-c", "./entrypoint.bash" ]

# CMD ["/entrypoint.bash"]