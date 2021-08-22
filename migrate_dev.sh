#!/usr/bin/env bash
PYTHONPATH=$PYTHONPATH:. \
LOG_MODE=LOCAL \
export CONSUL_ENABLED=true
python3 cli.py migrate