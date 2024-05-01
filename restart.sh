#!/bin/bash
./down.sh
docker compose -f ./environment/docker-compose.yaml build
./up.sh