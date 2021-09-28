#!/usr/bin/env bash

protoc -I protos/ protos/identification.proto --python_out=app/domain/chat/participant
protoc -I protos/ protos/node.proto --python_out=app/domain/chat/participant
protoc -I protos/ protos/responses.proto --python_out=app/domain/chat/participant
protoc -I protos/ protos/contacts.proto --python_out=app/domain/chat/participant
protoc -I protos/ protos/messages.proto --python_out=app/domain/chat/messages