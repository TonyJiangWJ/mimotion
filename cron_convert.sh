#!/bin/bash
function convert_utc_to_shanghai {
  local cron_str=$1
  echo "UTC时间: ${cron_str}"
  minute=`echo $cron_str | awk '{print $1}'`
  hours=`echo $cron_str | awk '{print $2}'`
  lines=`echo $hours|awk -F ',' '{for (i=1;i<=NF;i++) { print $i+8 }}'`
  # echo $lines
  result=""
  while IFS= read -r line; do
  if [ -z "$result" ]; then
    result="$line"
  else
    result="$result,$line"
  fi
  done <<< "$lines"
  echo "北京时间: $minute $result * * *'"
}

