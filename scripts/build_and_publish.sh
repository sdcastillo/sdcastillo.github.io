#!/usr/bin/env bash
# Sam News thin wrapper → midterms2026 publish gate.
set -euo pipefail
MIDTERMS="${MIDTERMS_ROOT:-/home/sandcastle/midterms2026}"
if [[ ! -x "$MIDTERMS/scripts/build_and_publish.sh" && ! -f "$MIDTERMS/scripts/build_and_publish.sh" ]]; then
  MIDTERMS="/home/ubuntu/midterms2026"
fi
exec bash "$MIDTERMS/scripts/build_and_publish.sh" "$@"
