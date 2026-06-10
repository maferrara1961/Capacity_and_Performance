#!/usr/bin/env bash
set -eu

python3 -m CapacityEngine.Scheduler.SyntheticDataCommand backfill-planning-metrics "$@"
