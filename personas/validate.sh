#!/usr/bin/env bash
set -euo pipefail

# Validation script for the AI persona framework
# Checks structural integrity, cross-references, and format compliance

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PASS=0
FAIL=0
WARN=0

green() { printf '\033[0;32m%s\033[0m\n' "$1"; }
red()   { printf '\033[0;31m%s\033[0m\n' "$1"; }
yellow(){ printf '\033[0;33m%s\033[0m\n' "$1"; }

pass() { ((PASS++)) || true; green "  ✓ $1"; }
fail() { ((FAIL++)) || true; red   "  ✗ $1"; }
warn() { ((WARN++)) || true; yellow "  ⚠ $1"; }

echo "=== Persona Framework Validation ==="
echo ""

# ---------------------------------------------------------------------------
# 1. Index-to-disk sync
# ---------------------------------------------------------------------------
echo "--- 1. Index-to-disk sync ---"

# Extract file paths from index.md tables (second column, backtick-wrapped)
index_files=()
while IFS= read -r line; do
  file=$(echo "$line" | grep -oE '`[^`]+\.md`' | tr -d '`' | head -1 || true)
  if [[ -n "$file" && "$file" != *"panels/"* ]]; then
    index_files+=("$file")
  fi
done < "$SCRIPT_DIR/index.md"

# Check each index entry exists on disk
for f in "${index_files[@]}"; do
  if [[ -f "$SCRIPT_DIR/$f" ]]; then
    pass "index → disk: $f"
  else
    fail "index → disk: $f (NOT FOUND)"
  fi
done

# Check each disk persona is in the index
while IFS= read -r -d '' diskfile; do
  rel="${diskfile#"$SCRIPT_DIR/"}"
  # Skip non-persona files
  case "$rel" in
    _shared/*|panels/*|index.md|panels-personas.md|tools.yaml|validate.sh|validate.py) continue ;;
  esac
  if grep -qF "$rel" "$SCRIPT_DIR/index.md"; then
    pass "disk → index: $rel"
  else
    fail "disk → index: $rel (NOT IN INDEX)"
  fi
done < <(find "$SCRIPT_DIR" -name '*.md' -not -path '*/_shared/*' -not -path '*/panels/*' -print0 | sort -z)

echo ""

# ---------------------------------------------------------------------------
# 2. Panel-to-persona resolution
# ---------------------------------------------------------------------------
echo "--- 2. Panel participant resolution ---"

for panel in "$SCRIPT_DIR"/panels/*.md; do
  panel_name=$(basename "$panel")
  # Extract markdown link targets from Participants section
  while IFS= read -r link; do
    target=$(echo "$link" | grep -oE '\(\.\.\/[^)]+\)' | tr -d '()' || true)
    if [[ -z "$target" ]]; then continue; fi
    resolved="$SCRIPT_DIR/panels/$target"
    if [[ -f "$resolved" ]]; then
      pass "$panel_name → $(basename "$target")"
    else
      fail "$panel_name → $target (NOT FOUND)"
    fi
  done < <(sed -n '/^## Participants/,/^## /p' "$panel" | grep -E '^\- ' || true)
done

echo ""

# ---------------------------------------------------------------------------
# 3. Persona section structure
# ---------------------------------------------------------------------------
echo "--- 3. Persona section structure ---"

required_sections=("## Role" "## Allowed Tools" "## Tool Setup" "## Evaluate For" "## Output Format" "## Principles" "## Anti-patterns")

while IFS= read -r -d '' pfile; do
  rel="${pfile#"$SCRIPT_DIR/"}"
  case "$rel" in
    _shared/*|panels/*|index.md|panels-personas.md|tools.yaml|validate.sh|validate.py) continue ;;
  esac
  missing=()
  for section in "${required_sections[@]}"; do
    if ! grep -qF "$section" "$pfile"; then
      missing+=("$section")
    fi
  done
  if [[ ${#missing[@]} -eq 0 ]]; then
    pass "sections: $rel"
  else
    fail "sections: $rel — missing: ${missing[*]}"
  fi
done < <(find "$SCRIPT_DIR" -name '*.md' -not -path '*/_shared/*' -not -path '*/panels/*' -print0 | sort -z)

echo ""

# ---------------------------------------------------------------------------
# 4. Shared reference check (base-tools)
# ---------------------------------------------------------------------------
echo "--- 4. Shared base-tools reference ---"

while IFS= read -r -d '' pfile; do
  rel="${pfile#"$SCRIPT_DIR/"}"
  case "$rel" in
    _shared/*|panels/*|index.md|panels-personas.md|tools.yaml|validate.sh|validate.py) continue ;;
  esac
  if grep -q 'base-tools\.md' "$pfile"; then
    pass "base-tools ref: $rel"
  else
    fail "base-tools ref: $rel (MISSING)"
  fi
done < <(find "$SCRIPT_DIR" -name '*.md' -not -path '*/_shared/*' -not -path '*/panels/*' -print0 | sort -z)

echo ""

# ---------------------------------------------------------------------------
# 5. Tool Setup standardization
# ---------------------------------------------------------------------------
echo "--- 5. Tool Setup standardization ---"

while IFS= read -r -d '' pfile; do
  rel="${pfile#"$SCRIPT_DIR/"}"
  case "$rel" in
    _shared/*|panels/*|index.md|panels-personas.md|tools.yaml|validate.sh|validate.py) continue ;;
  esac
  if grep -q 'tool-setup\.md' "$pfile"; then
    pass "tool-setup ref: $rel"
  else
    fail "tool-setup ref: $rel (MISSING)"
  fi
done < <(find "$SCRIPT_DIR" -name '*.md' -not -path '*/_shared/*' -not -path '*/panels/*' -print0 | sort -z)

echo ""

# ---------------------------------------------------------------------------
# 6. Panel structure
# ---------------------------------------------------------------------------
echo "--- 6. Panel section structure ---"

panel_sections=("## Purpose" "## Participants" "## Process" "## Output Format" "## Constraints" "## Conflict Resolution")

for panel in "$SCRIPT_DIR"/panels/*.md; do
  pname=$(basename "$panel")
  missing=()
  for section in "${panel_sections[@]}"; do
    if ! grep -qF "$section" "$panel"; then
      missing+=("$section")
    fi
  done
  if [[ ${#missing[@]} -eq 0 ]]; then
    pass "panel sections: $pname"
  else
    fail "panel sections: $pname — missing: ${missing[*]}"
  fi
done

echo ""

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo "=== Summary ==="
green "  Passed: $PASS"
if [[ $FAIL -gt 0 ]]; then
  red "  Failed: $FAIL"
else
  green "  Failed: $FAIL"
fi
if [[ $WARN -gt 0 ]]; then
  yellow "  Warnings: $WARN"
fi

if [[ $FAIL -gt 0 ]]; then
  echo ""
  red "VALIDATION FAILED"
  exit 1
else
  echo ""
  green "ALL CHECKS PASSED"
  exit 0
fi
