#!/bin/sh
for svc in $(docker compose config | yq '.services[]|key'); do
  echo "updating service \"$svc\""
  docker rollout "$svc"
done