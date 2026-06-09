#!/bin/sh
HostName="${1:-}"
FactName="${2:-}"
FactFile="/var/lib/zabbix/capacity-agent/EnterpriseFacts.tsv"

case "$FactName" in
  LicenseStatus|ComplianceStatus|BacklevelStatus|LifecycleStatus|EndOfSupportDate) ;;
  *)
    printf '%s\n' "UnsupportedFact"
    exit 1
    ;;
esac

if [ -z "$HostName" ] || [ ! -f "$FactFile" ]; then
  printf '%s\n' "Unknown"
  exit 0
fi

awk -F '	' -v HostName="$HostName" -v FactName="$FactName" '
  NR == 1 {
    for (Index = 1; Index <= NF; Index++) {
      Columns[$Index] = Index
    }
    next
  }
  $1 == HostName {
    if (FactName in Columns && $Columns[FactName] != "") {
      print $Columns[FactName]
    } else {
      print "Unknown"
    }
    Found = 1
    exit
  }
  END {
    if (!Found) {
      print "Unknown"
    }
  }
' "$FactFile"
