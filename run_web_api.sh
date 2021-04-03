#!/bin/bash
echo "Starting MongoDB ..."
sudo systemctl start mongod

export MONGO_DATABASE_NAME="kidney_exchange_test"
export PYTHONPATH="$PWD"

echo $PYTHONPATH

python transplants/solve_web_api/app.py
