#!/usr/bin/env bash
set -euo pipefail

# Infer a semver bump, update .symver, commit, and tag HEAD.
# Heuristic: breaking change marker -> major; feat -> minor; default patch; prompt allows override.

ROOT=$(git rev-parse --show-toplevel)
cd "$ROOT"

VERSION_FILE=".symver"
DEFAULT_VERSION="v1.0.0"

semver_valid() {
  [[ "$1" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]
}

semver_compare() {
  # returns -1 if $1 < $2, 0 if equal, 1 if $1 > $2
  local a=${1#v} b=${2#v}
  IFS=. read -r a1 a2 a3 <<<"$a"
  IFS=. read -r b1 b2 b3 <<<"$b"
  for i in 1 2 3; do
    local va vb
    va=$(eval echo "\$a$i")
    vb=$(eval echo "\$b$i")
    if ((va < vb)); then echo -1; return; fi
    if ((va > vb)); then echo 1; return; fi
  done
  echo 0
}

semver_bump() {
  local base=$1 kind=$2
  local major minor patch
  IFS=. read -r major minor patch <<<"${base#v}"
  case "$kind" in
    major) major=$((major+1)); minor=0; patch=0 ;;
    minor) minor=$((minor+1)); patch=0 ;;
    patch) patch=$((patch+1)) ;;
    *) echo "unknown bump: $kind" >&2; return 1 ;;
  esac
  echo "v${major}.${minor}.${patch}"
}

die() { echo "$1" >&2; exit 1; }

status=$(git status --porcelain)
[[ -n "$status" ]] && die "Working tree not clean. Commit or stash changes first."

if [[ ! -f "$VERSION_FILE" ]]; then
  echo "$DEFAULT_VERSION" > "$VERSION_FILE"
  echo "Initialized $VERSION_FILE to $DEFAULT_VERSION"
fi

current_version=$(tr -d ' \n' < "$VERSION_FILE")
semver_valid "$current_version" || current_version="$DEFAULT_VERSION"

last_tag=$(git tag --list 'v*' --sort=-v:refname | head -n1 || true)
[[ -z "$last_tag" ]] && last_tag="$DEFAULT_VERSION"

if [[ $(semver_compare "$last_tag" "$current_version") -gt 0 ]]; then
  echo "Warning: $VERSION_FILE ($current_version) is behind latest tag ($last_tag). Using $last_tag as base."
  current_version="$last_tag"
fi

diff_range="$last_tag..HEAD"
log_summary=$(git log $diff_range --oneline || true)

proposed="patch"
if echo "$log_summary" | grep -qi "BREAKING CHANGE"; then
  proposed="major"
elif echo "$log_summary" | grep -Eqi "\bfeat\b"; then
  proposed="minor"
fi

echo "Latest tag: $last_tag"
echo "Current version: $current_version"
echo "Changes since last tag:"
git log $diff_range --oneline || true

echo "Proposed bump: $proposed"
read -rp "Select bump [major/minor/patch] (default: $proposed): " choice
choice=${choice:-$proposed}
case "$choice" in
  major|minor|patch) ;;
  *) die "Invalid choice: $choice" ;;
esac

next_version=$(semver_bump "$current_version" "$choice")

if [[ $(semver_compare "$next_version" "$last_tag") -le 0 ]]; then
  die "Next version $next_version is not greater than latest tag $last_tag"
fi

echo "$next_version" > "$VERSION_FILE"
git add "$VERSION_FILE"
git commit -m "chore: bump version to $next_version"
git tag -a "$next_version" -m "Release $next_version"

echo "Tagged $next_version. Push with:"
echo "  git push origin HEAD --tags"
