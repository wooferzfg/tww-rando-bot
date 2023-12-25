#!/bin/bash -ex

for rando in wwrando wwrando-dev-tanjo3 wwrando-random-settings wwrando-mixed-pools; do
    (cd $rando &&
        python -m venv /venv/$rando --upgrade-deps &&
        /venv/$rando/bin/pip install --no-cache-dir -r requirements.txt)
done
