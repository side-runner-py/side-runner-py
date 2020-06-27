#!/bin/sh
COMPOSE_FILE=$1
COMPOSE="docker-compose -f $COMPOSE_FILE"

sudo rm -rf ~/out
mkdir -p ~/out
$COMPOSE up -d
$COMPOSE logs -f runner &
logs_pid=$!
while $COMPOSE ps | grep _runner_ | grep -q Up; do
  sleep 1
done
kill $logs_pid
$COMPOSE down
