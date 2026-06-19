#!/usr/bin/env bash
# Scaffold a new per-package fix directory from _template/.
# Usage: tools/new-fix.sh <package> <CVE-ID>
set -euo pipefail

pkg="${1:-}"
cve="${2:-}"
if [[ -z "$pkg" || -z "$cve" ]]; then
    echo "usage: $0 <package> <CVE-ID>   e.g. $0 curl CVE-2026-12345" >&2
    exit 2
fi
if [[ ! "$cve" =~ ^CVE-[0-9]{4}-[0-9]{4,}$ ]]; then
    echo "error: '$cve' is not a CVE id (CVE-YYYY-NNNNN)" >&2
    exit 2
fi

root="$(cd "$(dirname "$0")/.." && pwd)"
dst="$root/$pkg"
if [[ -e "$dst" ]]; then
    echo "error: $pkg/ already exists" >&2
    exit 1
fi

mkdir -p "$dst"
today="$(date +%F)"
for f in CVE-XXXX-NNNNN.patch changelog.diff bug-report.md; do
    out="${f/CVE-XXXX-NNNNN/$cve}"
    sed -e "s/CVE-XXXX-NNNNN/$cve/g" \
        -e "s/<package>/$pkg/g" \
        -e "s/<YYYY-MM-DD>/$today/g" \
        "$root/_template/$f" > "$dst/$out"
done

echo "Created $pkg/ for $cve:"
ls -1 "$dst" | sed 's/^/  /'
echo
echo "Next: fill in $pkg/$cve.patch (paste upstream diff verbatim),"
echo "      then update README.md and fixes.yaml."
