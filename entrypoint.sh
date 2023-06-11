#!/bin/sh

cd web/
flask db upgrade
cd ..
python run.py
