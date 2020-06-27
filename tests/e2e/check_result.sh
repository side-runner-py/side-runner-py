#!/bin/sh

failed=0
for dir in $(ls ~/out/* -td | tac); do
  python tests/e2e/check_result.py ${dir}/result.json
  [ $? -ne 0 ] && failed=1
done
exit $failed
