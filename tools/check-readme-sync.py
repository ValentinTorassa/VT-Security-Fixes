#!/usr/bin/env python3
"""Check that README.md and tools/submit-sru.sh agree with fixes.yaml.

fixes.yaml is the registry; the README tables and the SRU script restate parts of
it by hand. This fails when they drift: a series added in one place only, a bug
number missing from a table, a severity or CVSS that changed, a patch renamed.

Standard library only (the CI runner has no PyYAML), so it reads the small YAML
subset fixes.yaml uses: one list of flat entries, flow lists/maps, nested block
maps and lists, folded strings and trailing comments.

Usage: tools/check-readme-sync.py [repo-root]
"""
import re
import sys
from pathlib import Path


def strip_comment(line):
    """Split a line into (content, comment), ignoring '#' inside quotes."""
    quote = None
    for i, ch in enumerate(line):
        if quote:
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            return line[:i].rstrip(), line[i + 1:].strip()
    return line.rstrip(), ""


def split_flow(body):
    """Split 'a, "b, c", d' on top-level commas."""
    parts, current, quote = [], "", None
    for ch in body:
        if quote:
            current += ch
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
            current += ch
        elif ch == ",":
            parts.append(current.strip())
            current = ""
        else:
            current += ch
    if current.strip():
        parts.append(current.strip())
    return parts


def scalar(text):
    text = text.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        return text[1:-1]
    if text.startswith("[") and text.endswith("]"):
        return [scalar(p) for p in split_flow(text[1:-1])]
    if text.startswith("{") and text.endswith("}"):
        result = {}
        for part in split_flow(text[1:-1]):
            key, _, value = part.partition(":")
            result[key.strip()] = scalar(value)
        return result
    return text


def load_fixes(path):
    fixes, entry, key, folded = [], None, None, False
    for raw in path.read_text().splitlines():
        line, comment = strip_comment(raw)
        if not line.strip():
            folded = False
            continue
        indent = len(line) - len(line.lstrip())
        text = line.strip()
        if text.startswith("- ") and indent == 2:
            entry = {"_comments": {}}
            fixes.append(entry)
            text, indent = text[2:], 4
        if entry is None:
            continue
        if indent == 4:
            key, _, value = text.partition(":")
            key, value = key.strip(), value.strip()
            entry["_comments"][key] = comment
            folded = value in (">", ">-", "|", "|-")
            entry[key] = "" if folded else (scalar(value) if value else None)
        elif folded:
            entry[key] = (entry[key] + " " + text).strip()
        elif text.startswith("- "):
            if not isinstance(entry.get(key), list):
                entry[key] = []
            entry[key].append(scalar(text[2:]))
        else:
            if not isinstance(entry.get(key), dict):
                entry[key] = {}
            sub, _, value = text.partition(":")
            entry[key][sub.strip()] = scalar(value)
    return fixes


def sections(readme):
    """Map CVE id -> (heading, body) for the '## ... CVE-... - package (...)' sections."""
    found = {}
    parts = re.split(r"(?m)^(## .*)$", readme)
    for heading, body in zip(parts[1::2], parts[2::2]):
        match = re.search(r"(CVE-\d{4}-\d+) - (\S+) \(([^)]*)\)", heading)
        if match:
            found[match.group(1)] = (match.group(2), match.group(3), body)
    return found


def row(body, label):
    match = re.search(rf"^\| \*\*{re.escape(label)}\*\* \| (.*) \|\s*$", body, re.M)
    return match.group(1) if match else None


def check(root):
    errors = []
    fixes = load_fixes(root / "fixes.yaml")
    readme = (root / "README.md").read_text()
    script = (root / "tools/submit-sru.sh").read_text()
    readme_sections = sections(readme)
    if not fixes:
        return ["fixes.yaml: no fixes parsed"]

    for fix in fixes:
        cve, package = fix.get("cve"), fix.get("package")
        where = f"{cve} ({package})"
        affected = fix.get("affected") or []
        if cve not in readme_sections:
            errors.append(f"{where}: no README section '## ... {cve} - {package} (...)'")
            continue
        readme_package, heading_series, body = readme_sections[cve]
        if readme_package != package:
            errors.append(f"{where}: README section names package {readme_package!r}")
        heading = [s.strip() for s in heading_series.split("+")]
        if heading != affected:
            errors.append(f"{where}: README heading lists {heading}, fixes.yaml affected is {affected}")

        affected_row = row(body, "Affected") or ""
        listed = re.findall(r"`([a-z]+)`", affected_row.split("(")[0])
        if listed != affected:
            errors.append(f"{where}: README Affected row lists {listed}, fixes.yaml has {affected}")
        for series in (fix.get("ignored") or {}):
            if series not in affected_row:
                errors.append(f"{where}: ignored series {series} not explained in the Affected row")

        severity_row = row(body, "Severity") or ""
        severity = (fix.get("severity") or "").upper()
        if not severity_row.startswith(severity):
            errors.append(f"{where}: README severity {severity_row!r}, fixes.yaml says {severity}")
        cvss = re.search(r"CVSS (\d+(?:\.\d+)?)", fix["_comments"].get("severity", ""))
        if cvss and f"CVSS {cvss.group(1)}" not in severity_row:
            errors.append(f"{where}: README severity row lacks CVSS {cvss.group(1)}")

        standard_row = row(body, "Standard status") or ""
        for series, state in (fix.get("standard") or {}).items():
            if f"`{series}: {state}`" not in standard_row:
                errors.append(f"{where}: README Standard status lacks `{series}: {state}`")
        for series, state in (fix.get("esm") or {}).items():
            if state not in (row(body, "ESM status") or ""):
                errors.append(f"{where}: README ESM status lacks {series} {state}")

        # Check the visible text, not just the link target, so a wrong number shown
        # next to a right URL still fails.
        for field, label, shown in (("launchpad_bug", "Launchpad bug", "[LP: #{}]"),
                                    ("debian_bug", "Debian bug", "[#{}]")):
            number = fix.get(field)
            if number and shown.format(number) not in (row(body, label) or ""):
                errors.append(f"{where}: README '{label}' row does not show {shown.format(number)}")
        patch = fix.get("patch")
        if patch and patch not in (row(body, "Patch") or ""):
            errors.append(f"{where}: README Patch row does not link {patch}")
        if patch and not (root / patch).is_file():
            errors.append(f"{where}: patch file {patch} does not exist")

        match = re.search(rf'"{re.escape(package)}\|([a-z,]+)\|([^|]+)\|', script)
        if not match:
            errors.append(f"{where}: no entry in tools/submit-sru.sh")
        else:
            if match.group(1).split(",") != affected:
                errors.append(f"{where}: submit-sru.sh builds {match.group(1)}, fixes.yaml affected is {affected}")
            if match.group(2) != patch:
                errors.append(f"{where}: submit-sru.sh uses patch {match.group(2)}")

    dates = {fix.get("reviewed_at") for fix in fixes}
    review = re.search(r"(?m)^## Status review - (\d{4}-\d{2}-\d{2})$", readme)
    if len(dates) != 1:
        errors.append(f"fixes.yaml: entries have different reviewed_at dates {sorted(dates)}")
    elif not review or review.group(1) not in dates:
        errors.append(f"README status review date {review.group(1) if review else 'missing'} "
                      f"does not match fixes.yaml reviewed_at {dates.pop()}")
    known = {fix.get("cve") for fix in fixes}
    for cve in readme_sections:
        if cve not in known:
            errors.append(f"{cve}: README section has no fixes.yaml entry")
    return errors


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    errors = check(root)
    for error in errors:
        print(f"✗ {error}", file=sys.stderr)
    if errors:
        print(f"{len(errors)} mismatch(es) between fixes.yaml, README.md and submit-sru.sh", file=sys.stderr)
        return 1
    print(f"✓ README.md and submit-sru.sh agree with fixes.yaml ({len(load_fixes(root / 'fixes.yaml'))} fixes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
