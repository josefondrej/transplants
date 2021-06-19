#!/bin/bash

echo "Starting MongoDB ..."
sudo systemctl start mongod

export MONGO_DATABASE_NAME="${1:-kidney_exchange}"
export PYTHONPATH="$PWD"

echo "MONGO_DATABASE_NAME=$MONGO_DATABASE_NAME"
echo "PYTHONPATH=$PYTHONPATH"

python transplants/frontend/solve_api.py
