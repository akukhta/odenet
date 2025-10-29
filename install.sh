#!/bin/bash
set -e

if [ ! -d ".venv" ]; then
    python3.7 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
fi

source .venv/bin/activate
jupyter lab "OdeNetAccess.ipynb"
deactivate