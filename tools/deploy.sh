#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 tools/validate.py
python3 tools/check_dependencies.py
python3 tools/check_field.py
python3 tools/check_copy_sync.py
python3 tools/check_metadata.py
python3 tools/check_typography.py
python3 tools/check_navigation.py
python3 tools/check_navigation_system.py
python3 tools/test_outline_generation.py
python3 tools/build_clients_css.py --check
python3 tools/check_clients.py
python3 tools/check_rules.py
python3 tools/check_engagement_pages.py
"${OPA_BIN:-opa}" eval --fail --format=pretty --data policy.rego --input build/clients-policy-input.json "data.wildlake.clients.allow = true"
case "${1:-all}" in
  site) npx --yes wrangler@4.158.0 deploy --config deploy/site.wrangler.json ;;
  mirror) npx --yes wrangler@4.158.0 deploy --config deploy/mirror.wrangler.json ;;
  all)
    npx --yes wrangler@4.158.0 deploy --config deploy/site.wrangler.json
    npx --yes wrangler@4.158.0 deploy --config deploy/mirror.wrangler.json
    ;;
  *) echo 'Usage: tools/deploy.sh [site|mirror|all]' >&2; exit 2 ;;
esac
