#!/bin/bash
# Prerequisite for running: ./run_solve_api.sh kidney_exchange_test
export MONGO_DATABASE_NAME="kidney_exchange_test"
export PYTHONPATH="$PWD"

echo "MONGO_DATABASE_NAME=$MONGO_DATABASE_NAME"
echo "PYTHONPATH=$PYTHONPATH"

python -m unittest discover
