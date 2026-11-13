#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 tools/validate.py
python3 tools/check_dependencies.py
python3 tools/check_copy_sync.py
python3 tools/check_metadata.py
case "${1:-all}" in
  site) npx --yes wrangler@4.158.0 deploy --config deploy/site.wrangler.json ;;
  mirror) npx --yes wrangler@4.158.0 deploy --config deploy/mirror.wrangler.json ;;
  all)
    npx --yes wrangler@4.158.0 deploy --config deploy/site.wrangler.json
    npx --yes wrangler@4.158.0 deploy --config deploy/mirror.wrangler.json
    ;;
  *) echo 'Usage: tools/deploy.sh [site|mirror|all]' >&2; exit 2 ;;
esac
