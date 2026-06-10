#!/bin/sh
HostName="${1:-}"
MetricName="${2:-}"
MetricFile="/var/lib/zabbix/capacity-agent/PlatformMetrics.tsv"

case "$MetricName" in
  CpuPercent|MemoryUsedBytes|MemoryPercent|NetworkInputBytes|NetworkOutputBytes|BlockInputBytes|BlockOutputBytes) ;;
  *)
    printf '%s\n' "0"
    exit 1
    ;;
esac

if [ -z "$HostName" ] || [ ! -f "$MetricFile" ]; then
  printf '%s\n' "0"
  exit 0
fi

awk -F '	' -v HostName="$HostName" -v MetricName="$MetricName" '
  NR == 1 {
    for (Index = 1; Index <= NF; Index++) {
      Columns[$Index] = Index
    }
    next
  }
  $1 == HostName {
    if (MetricName in Columns && $Columns[MetricName] != "") {
      print $Columns[MetricName]
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
' "$MetricFile"
