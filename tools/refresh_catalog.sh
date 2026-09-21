#!/usr/bin/env bash
# Refresh the vendored catalog to a given upstream commit, and prove what changed.
set -euo pipefail
SHA="${1:?usage: refresh_catalog.sh <commit-sha>}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

git clone -q https://github.com/zhenghh04/application_catalog "$TMP/c"
git -C "$TMP/c" checkout -q "$SHA"
rm -rf "$TMP/c/.git"
cp "$ROOT/data/catalog/PROVENANCE.md" "$TMP/PROVENANCE.md"

echo "== files that differ from the current vendored copy =="
diff -rq "$ROOT/data/catalog" "$TMP/c" 2>/dev/null | grep -v PROVENANCE || echo "  none"

rm -rf "$ROOT/data/catalog"; mv "$TMP/c" "$ROOT/data/catalog"
mv "$TMP/PROVENANCE.md" "$ROOT/data/catalog/PROVENANCE.md"
echo "== update the pinned SHA in data/catalog/PROVENANCE.md to $SHA =="

cd "$ROOT"
python -m benchmark.catalog --parity
python -m benchmark.catalog --fill | head -6
echo "== the repairs may now be redundant or stale — check the lines above =="
python -m audit.oracle --diff --corpus v7 || {
  echo "!! the oracle changed. A catalog refresh moved a verdict — read the diff before committing."
  exit 1; }
