FROM python:3.8-buster

WORKDIR /tww-rando-bot

ENV QT_QPA_PLATFORM=offscreen

RUN apt-get update && apt-get install -y \
  libegl1 \
  libgl1-mesa-glx \
  libxkbcommon-x11-0 \
  libdbus-1-3

COPY . .

RUN pip install --upgrade pip

RUN cd wwrando && pip install -r requirements.txt

RUN cd wwrando-dev-tanjo3 && pip install -r requirements.txt

RUN cd wwrando-s5-tournament && pip install -r requirements.txt

RUN cd wwrando-random-settings && pip install -r requirements.txt

RUN pip install -e .
