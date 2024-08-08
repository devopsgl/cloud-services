#!/bin/bash
docker compose -f ./environment/docker-compose.yaml build applcation-store
docker compose -f ./environment/docker-compose.yaml build groups

docker compose -f ./environment/docker-compose.yaml up -d application-store
docker compose -f ./environment/docker-compose.yaml up -d groups
docker compose -f ./environment/docker-compose.yaml logs -f