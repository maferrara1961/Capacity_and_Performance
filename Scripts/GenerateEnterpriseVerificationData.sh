#!/usr/bin/env bash
set -eu

python3 -m CapacityEngine.Scheduler.SyntheticDataCommand generate-enterprise-verification-data "$@"
