#!/bin/sh
HostName="${1:-}"
StatusFile="/var/lib/zabbix/capacity-agent/PlatformStatus.tsv"

if [ -z "$HostName" ] || [ ! -f "$StatusFile" ]; then
  printf '%s\n' "0"
  exit 0
fi

awk -F '	' -v HostName="$HostName" '
  NR == 1 {
    next
  }
  $1 == HostName {
    if ($2 == "1") {
      print "1"
    } else {
      print "0"
    }
    Found = 1
    exit
  }
  END {
    if (!Found) {
      print "0"
    }
  }
' "$StatusFile"
