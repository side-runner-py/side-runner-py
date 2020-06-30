#!/bin/sh
log_file=~/hook-logs/log.txt

# check logging count per test
if [ "$(grep "pre_test_hook" $log_file | wc -l)" -ne 3 ]; then
  exit 1
fi
if [ "$(grep "post_test_hook" $log_file | wc -l)" -ne 3 ]; then
  exit 1
fi

# check logging count per command
if [ "$(grep "pre_command_hook" $log_file | wc -l)" -ne 5 ]; then
  exit 1
fi
if [ "$(grep "post_command_hook" $log_file | wc -l)" -ne 5 ]; then
  exit 1
fi

# check log message per test
sample_log=$(grep "pre_test_hook" $log_file | head -n1 | cut -d: -f2-)
if [ "$(echo "$sample_log" | jq -r '.test_name')" != "Radio button" ]; then
  exit 1
fi

# check log message per command
sample_log=$(grep "pre_command_hook" $log_file | head -n1 | cut -d: -f2-)
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
