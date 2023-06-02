#!/bin/bash

function inspect_next {
  cron_str=$1
  cron_str=`echo $cron_str|sed "s#'##g"`
  minute=`TZ=UTC date '+%M'`
  minute=$((10#$minute))
  hour=`TZ=UTC date '+%H'`
  hour=$((10#$hour))
  cron_minute=`echo $cron_str | awk '{print $1}'`
  cron_hours=`echo $cron_str | awk '{print $2}'`
  # echo "current $hour:$minute"
  # echo "cron hourse: $cron_hours"
  next_exec_hour=`echo $cron_hours | awk -v min="$minute" -v hour="$hour" -v cron_min="$cron_minute" -F ',' '{
    for (i=1;i<=NF;i++) {
      if ($i>hour || $i==hour && cron_min>min) {
         print $i
         break
      }
    }
  }'`
  if test -z $next_exec_hour; then
    next_exec_hour=`echo $cron_hours | awk -F ',' '{print $1}'`
  fi
  echo "next exec time: UTC($next_exec_hour:$cron_minute) 北京时间($((($next_exec_hour+8) % 24)):$cron_minute)"
}

function convert_utc_to_shanghai {
  local cron_str=$1
  echo "UTC时间: ${cron_str}"
  minute=`echo $cron_str | awk '{print $1}'`
  hours=`echo $cron_str | awk '{print $2}'`
  lines=`echo $hours|awk -F ',' '{for (i=1;i<=NF;i++) { print ($i+8)%24 }}'`
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

function persist_execute_log {
  local event_name=$1
  local new_cron_hours=$2
  echo "trigger by: ${event_name}" > cron_change_time
  echo "current system time:" >> cron_change_time
  TZ='UTC' date "+%y-%m-%d %H:%M:%S" | xargs -I {} echo "UTC: {}" >> cron_change_time
  TZ='Asia/Shanghai' date "+%y-%m-%d %H:%M:%S" | xargs -I {} echo "北京时间: {}" >> cron_change_time
  current_cron=`cat .github/workflows/run.yml|grep cron|awk '{print substr($0, index($0,$3))}'`
  echo "current cron:" >> cron_change_time
  convert_utc_to_shanghai "$current_cron" >> cron_change_time
  if test -z "$new_cron_hours"; then
    sed -i -E "s/(- cron: ')[0-9]+( [^[:space:]]+ \* \* \*')/\1$(($RANDOM % 59))\2/g" .github/workflows/run.yml
  else
    sed -i -E "s/(- cron: ')[0-9]+( [^[:space:]]+ \* \* \*')/\1$(($RANDOM % 59)) ${new_cron_hours} * * *'/g" .github/workflows/run.yml
  fi
  current_cron=`cat .github/workflows/run.yml|grep cron|awk '{print substr($0, index($0,$3))}'`
  echo "next cron:" >> cron_change_time
  convert_utc_to_shanghai "$current_cron" >> cron_change_time
  inspect_next "$current_cron" >> cron_change_time
}

