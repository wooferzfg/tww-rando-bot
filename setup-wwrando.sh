#!/bin/bash -ex

for rando in wwrando; do
    (cd $rando &&
        python3.10 -m venv /venv/$rando --upgrade-deps &&
        /venv/$rando/bin/pip install --no-cache-dir -r requirements.txt)
done
for rando in wwrando-s7 wwrando-mixed-pools wwrando-random-settings; do
    (cd $rando &&
        python3.12 -m venv /venv/$rando --upgrade-deps &&
        /venv/$rando/bin/pip install --no-cache-dir -r requirements.txt)
done
