#! /usr/bin/env bash

export PYTHONPATH=.
export ALEMBIC_CONFIG=alembic.ini

echo "----------------------- 0 ---------------------------"
echo $PWD
# Let the DB start
# python /app/app/backend_pre_start.py
python app/backend_pre_start.py

echo "----------------------- 1 ---------------------------"
# Run migrations
python -m alembic upgrade head

echo "----------------------- 2 ---------------------------"
# Create initial data in DB
# python /app/app/initial_data.py
python app/initial_data.py

echo "----------------------- 3 ---------------------------"