#!/bin/sh
rm -rf ~/out
mkdir -p ~/out
docker-compose up -d
while docker-compose ps | grep _runner_ | grep Up; do
  sleep 1
done
docker-compose logs
docker-compose down

failed=0
for dir in $(ls ~/out/* -td | tac); do
  python tests/e2e/checkresult.py ${dir}/result.json
  [ $? -ne 0 ] && failed=1
done
exit $failed
