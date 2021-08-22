#!/usr/bin/env bash
PYTHONPATH=$PYTHONPATH:. \
LOG_MODE=LOCAL \

export CONSUL_ENABLED=false
export DEBUG=true

python3 main.py