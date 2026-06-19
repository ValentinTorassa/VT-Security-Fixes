#!/usr/bin/env bash
# Sanity-check every CVE patch in the repo:
#   - has a DEP-3 Description + Origin header
#   - has at least one well-formed unified-diff hunk
#   - hunk @@ line counts are internally consistent
# This does NOT build packages (needs an Ubuntu chroot for the target series).
set -uo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
fail=0

while IFS= read -r p; do
    name="${p#"$root"/}"
    err=()
    grep -q '^Description:' "$p"        || err+=("missing Description:")
    grep -q '^Origin:'      "$p"        || err+=("missing Origin:")
    grep -q '^--- a/'       "$p"        || err+=("no '--- a/' diff hunk")
    grep -q '^@@ '          "$p"        || err+=("no '@@' hunk header")

    # Per-hunk: counted +/context lines must match the @@ header.
    awk '
        /^@@ / {
            if (match($0, /\+[0-9]+(,[0-9]+)?/)) {
                s=substr($0,RSTART,RLENGTH); sub(/^\+/,"",s)
                n=index(s,","); want=(n? substr(s,n+1) : 1); got=0; inhunk=1; next
            }
        }
        inhunk && /^@@ |^--- |^Index:/ { if (got!=want){bad=1}; inhunk=0 }
        inhunk && (/^[+ ]/ || /^$/) { got++ }
        END { if (inhunk && got!=want) bad=1; exit bad }
    ' "$p" || err+=("hunk line count mismatch (would fail to apply)")

    if ((${#err[@]})); then
        printf '✗ %s\n' "$name"
        printf '    - %s\n' "${err[@]}"
        fail=1
    else
        printf '✓ %s\n' "$name"
    fi
done < <(find "$root" -name 'CVE-*.patch' -not -path '*/_template/*' | sort)

((fail)) && { echo; echo "Some patches need attention."; exit 1; }
echo; echo "All patches OK."
