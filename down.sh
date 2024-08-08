#!/bin/bash
docker compose -f ./environment/docker-compose.yaml down  application-store
docker compose -f ./environment/docker-compose.yaml down groups
