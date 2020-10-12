FROM python:3.8-buster

WORKDIR /twwr-spoiler-log-bot

ENV QT_QPA_PLATFORM=offscreen

RUN apt-get update && apt-get install -y \
  libgl1-mesa-glx \
  libxkbcommon-x11-0 \
  libdbus-1-3

RUN mkdir -p wwrando
COPY wwrando/requirements.txt wwrando
RUN cd wwrando && pip install -r requirements.txt

COPY setup.py ./
RUN pip install -e .

COPY . .
