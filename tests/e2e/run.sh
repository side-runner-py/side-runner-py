#!/bin/sh
BROWSER=${1:-chrome}
COMPOSE="docker-compose -f docker-compose-$BROWSER.yml"

rm -rf ~/out
mkdir -p ~/out
$COMPOSE up -d
while $COMPOSE ps | grep _runner_ | grep Up; do
  sleep 1
done
$COMPOSE logs
$COMPOSE down

failed=0
for dir in $(ls ~/out/* -td | tac); do
  python tests/e2e/checkresult.py ${dir}/result.json
  [ $? -ne 0 ] && failed=1
done
exit $failed
