#!/bin/bash
# Prerequisite for running: run_web_api.sh test
echo "Starting MongoDB ..."
sudo systemctl start mongod

export PYTHONPATH="$PWD"

python -m unittest discover
