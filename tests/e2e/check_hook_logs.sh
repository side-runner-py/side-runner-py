#!/bin/sh
log_file=~/hook-logs/log.txt

if [ "$(grep "pre_command_hook" $log_file | wc -l)" -ne 4 ]; then
  exit 1
fi

if [ "$(grep "post_command_hook" $log_file | wc -l)" -ne 4 ]; then
  exit 1
fi

sample_log=$(head -n1 $log_file | cut -d: -f2-)

session_id="$(echo "$sample_log" | jq 'select(.session_id != null)')"
if [ "$session_id" = "" ]; then
  exit 1
fi

if [ "$(echo "$sample_log" | jq -r '.test_name')" != "Radio button" ]; then
  exit 1
fi

if [ "$(echo "$sample_log" | jq -r '.command')" != "click" ]; then
  exit 1
fi

index="$(echo "$sample_log" | jq '.command_index')"
if [ "$index" -ne 1 -a "$index" -ne 2 -a "$index" -ne 4 -a "$index" -ne 5 ]; then
  exit 1
fi
