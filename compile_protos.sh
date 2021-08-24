#!/usr/bin/env bash

protoc -I protos/ protos/identification.proto --python_out=app/domain/chat/participant
protoc -I protos/ protos/node.proto --python_out=app/domain/chat/participant