#!/bin/bash
echo "Starting MongoDB ..."
sudo systemctl start mongod

export MONGO_DATABASE_NAME="kidney_exchange"
export PYTHONPATH="$PWD"

echo $PYTHONPATH

python transplants/frontend/app.py --mode "$1"
