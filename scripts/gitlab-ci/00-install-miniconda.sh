#!/bin/bash

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

set -ex

# The miniconda directory may exist if it has been restored from cache
if [ -d "$MINICONDA_DIR" ] && [ -e "$MINICONDA_DIR/bin/conda" ]; then
    echo "Miniconda install already present from cache: $MINICONDA_DIR"
else # if it does not exist, we need to install miniconda
    rm -rf "$MINICONDA_DIR" # remove the directory in case we have an empty cached directory
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -q -O ~/miniconda.sh;
    bash ~/miniconda.sh -b -p "$MINICONDA_DIR"
    chown -R "$USER" "$MINICONDA_DIR"
    hash -r
fi

export PATH="$MINICONDA_DIR/bin:$PATH"
conda config --set always_yes yes --set changeps1 no
conda config --add channels conda-forge

pip install .

conda update -q conda
conda info -a # for debugging