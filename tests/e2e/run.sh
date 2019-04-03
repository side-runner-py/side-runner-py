#!/bin/sh
mkdir -p ~/out
docker-compose up -d
while docker-compose ps | grep _runner_ | grep Up; do
  sleep 1
done
docker-compose logs
docker-compose down
outdir=$(ls ~/out/* -td | head -n 1)
python tests/e2e/checkresult.py ${outdir}/result.json
