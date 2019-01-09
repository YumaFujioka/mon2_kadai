#!/bin/sh

python MimoSimulator.py
python MimoSimulator.py -m mmse
python MimoSimulator.py -m mld
python MimoSimulator.py -o 8
python MimoSimulator.py -o 8 -m mmse
python MimoSimulator.py -o 8 -m mld
