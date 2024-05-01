#!/bin/bash
docker compose -f ./environment/docker-compose.yaml build

docker compose -f ./environment/docker-compose.yaml up -d