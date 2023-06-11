#!/bin/sh

cd app/
alembic upgrade
python run.py
