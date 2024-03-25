# This is the default version under which randobot will run
FROM python:3.12-bookworm

# Copy python from the source image for any additional version we need to support
COPY --from=python:3.10-bookworm /usr/local/bin/python3 /usr/local/bin/python3.10
COPY --from=python:3.10-bookworm /usr/local/lib/libpython3.10.so.1.0 /usr/local/lib/libpython3.10.so.1.0
COPY --from=python:3.10-bookworm /usr/local/lib/python3.10/ /usr/local/lib/python3.10

WORKDIR /tww-rando-bot

ENV QT_QPA_PLATFORM=offscreen

RUN apt-get update && apt-get install -y \
  libegl1 \
  libgl1-mesa-glx \
  libxkbcommon-x11-0 \
  libdbus-1-3

COPY . .

RUN pip install --upgrade pip

RUN ./setup-wwrando.sh

RUN pip install -e .
