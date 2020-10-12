FROM python:3.8-buster

WORKDIR /twwr-spoiler-log-bot

RUN mkdir -p wwrando
COPY wwrando/requirements.txt wwrando
RUN cd wwrando && pip install -r requirements.txt

COPY setup.py ./
RUN pip install -e .

COPY . .
