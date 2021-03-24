#!/bin/bash
echo "Starting MongoDB ..."
sudo systemctl start mongod

export MONGO_DATABASE_NAME="kidney_exchange_test"
export "$PYTHONPATH"="$PWD"

python ./transplants/database/purge_db.py
python -m unittest discover
