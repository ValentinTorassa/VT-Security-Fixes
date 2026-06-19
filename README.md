```
 ██╗   ██╗████████╗   ███████╗███████╗ ██████╗
 ██║   ██║╚══██╔══╝   ██╔════╝██╔════╝██╔════╝
 ██║   ██║   ██║      ███████╗█████╗  ██║
 ╚██╗ ██╔╝   ██║      ╚════██║██╔══╝  ██║
  ╚████╔╝    ██║      ███████║███████╗╚██████╗
   ╚═══╝     ╚═╝      ╚══════╝╚══════╝ ╚═════╝
     Security Fixes · patches for packages the autoupdater forgot
```

# VT Security Fixes

> Some packages don't get the security update. — VT Security

A personal, growing collection of **security patches for open-source packages that
fall through the cracks of automatic updates** — the long tail of community-maintained
software where a CVE is public, an upstream fix exists, but nothing has landed in the
channel most people actually run.

Each fix here is **DEP-3 formatted** and ready to drop into `debian/patches/`, with the
provenance (upstream commit, CVE, bug links) baked into the patch header. Today the
focus is **Ubuntu `universe`** CVEs, but the layout is distro-agnostic — anything with a
public CVE and an upstream fix is fair game.

| | |
|---|---|
| **Scope** | Open-source security patches (currently Ubuntu universe) |
| **Format** | DEP-3 patches, ready for `debian/patches/` |
| **Status** | Tracked in [`fixes.yaml`](fixes.yaml) |
| **Contributing** | See [`CONTRIBUTING.md`](CONTRIBUTING.md) |

---

## Why this exists

Canonical ships automatic security updates for **main**, but **universe** packages are
community-maintained — they only get fixes if someone does the SRU (Stable Release
Update) work. For the CVEs below, fixes already exist in the **ESM (Ubuntu Pro)** pocket,
but the standard pocket — what most users run — is still vulnerable. These patches bridge
that gap, and are formatted so a maintainer can pick them up with zero rework.

---

## 🟡 CVE-2025-11021 — libsoup3 (jammy)

| | |
|---|---|
| **Severity** | HIGH (CVSS 7.5) |
| **Issue** | Out-of-bounds read in cookie date parsing — integer overflow in `parse_timezone()` |
| **Package** | `libsoup3` |
| **Affected** | `jammy` only (all other releases already patched) |
| **ESM status** | ✅ `esm-apps/jammy: released (3.0.7-0ubuntu1+esm5)` |
| **Standard status** | ❌ `jammy: needed` |
| **Upstream fix** | [GNOME MR !473](https://gitlab.gnome.org/GNOME/libsoup/-/merge_requests/473) |
| **Debian bug** | [#1116469](https://bugs.debian.org/1116469) |
| **Patch** | [`libsoup3/CVE-2025-11021-CVE-2025-4945.patch`](libsoup3/CVE-2025-11021-CVE-2025-4945.patch) |

### Track merge status
- [Ubuntu CVE page](https://ubuntu.com/security/CVE-2025-11021)
- [Launchpad package](https://launchpad.net/ubuntu/+source/libsoup3)
- CLI: `rmadison libsoup3 \| grep jammy`

---

## 🟡 CVE-2025-11683 — libyaml-syck-perl (jammy + noble)

| | |
|---|---|
| **Severity** | MEDIUM (CVSS 6.5) |
| **Issue** | Missing null terminators in `token.c` — out-of-bounds read on empty-key YAML hashes |
| **Package** | `libyaml-syck-perl` |
| **Affected** | `jammy`, `noble` |
| **ESM status** | ✅ `esm-apps/jammy: released (1.34-1ubuntu0.1~esm1)`, `esm-apps/noble: released (1.34-2ubuntu0.24.04.1~esm1)` |
| **Standard status** | ❌ `jammy: needed`, `noble: needed` |
| **Upstream fix** | [dcf4c84](https://github.com/cpan-authors/YAML-Syck/commit/dcf4c8477b82ef439f43fd20dc099082d096df02) (v1.36) |
| **Patch** | [`libyaml-syck-perl/CVE-2025-11683.patch`](libyaml-syck-perl/CVE-2025-11683.patch) |

### Track merge status
- [Ubuntu CVE page](https://ubuntu.com/security/CVE-2025-11683)
- [Launchpad package](https://launchpad.net/ubuntu/+source/libyaml-syck-perl)
- CLI: `rmadison libyaml-syck-perl \| grep -E "jammy\|noble"`

---

## 🟡 CVE-2025-11266 — gdcm (jammy + noble + questing)

| | |
|---|---|
| **Severity** | MEDIUM (CVSS 6.6) |
| **Issue** | OOB write in DICOM fragment parsing — missing bounds check before buffer access |
| **Package** | `gdcm` |
| **Affected** | `jammy`, `noble`, `questing` |
| **Upstream fix** | [5829c95](https://github.com/malaterre/GDCM/commit/5829c95c8ac3afa9a3a3413675e948959c28a789) (v3.2.2) |
| **Debian bug** | [#1122862](https://bugs.debian.org/1122862) |
| **Patch** | [`gdcm/CVE-2025-11266.patch`](gdcm/CVE-2025-11266.patch) |

### Track merge status
- [Ubuntu CVE page](https://ubuntu.com/security/CVE-2025-11266)
- [Launchpad package](https://launchpad.net/ubuntu/+source/gdcm)
- CLI: `rmadison gdcm`

---

## How to submit an SRU

1. **File a Launchpad bug** for each CVE at `bugs.launchpad.net/ubuntu/+source/<pkg>`
   (a ready-to-paste `bug-report.md` lives in each package folder)
2. **Download source**: `pull-lp-source <pkg> jammy`
3. **Apply patch**: copy `.patch` into `debian/patches/`, add to `series`
4. **Changelog**: `dch -v "<version>.1" -D jammy-security "SECURITY UPDATE: ..."`
5. **Build & upload**: `debuild -S -sa && dput ubuntu ../*.changes`

> The patches are DEP-3 formatted — they include Origin, Bug links, and upstream commit
> references. Ready for `debian/patches/`.

---

## How to check if a fix was merged

The merge doesn't happen on GitHub — it happens on **Launchpad** (Ubuntu's platform).
Here's how to track each step:

| What to check | How | Meaning |
|---|---|---|
| **CVE tracker status** | [ubuntu.com/security/cves](https://ubuntu.com/security/cves) — search the CVE ID | If it says "Fixed" or shows a released version, the patch shipped |
| **Package version** | `rmadison <pkg>` on any Ubuntu machine | Look for `-security` or `-updates` pocket with the patched version |
| **Launchpad bug** | The bug you filed when submitting | Status goes: New → In Progress → Fix Committed → Fix Released |
| **UCT git repo** | `git clone lp:ubuntu-cve-tracker && grep <pkg> active/CVE-*` | `needed` changes to `released (<version>)` |
| **USN notice** | [ubuntu.com/security/notices](https://ubuntu.com/security/notices) | Canonical publishes a USN when the fix ships |

### Quick check (once you have the Launchpad bug number):
```bash
# Check if the fix shipped
rmadison libsoup3 | grep jammy-security

# Check the CVE tracker
git clone --depth 1 git://git.launchpad.net/ubuntu-cve-tracker
grep jammy_libsoup3 ubuntu-cve-tracker/active/CVE-2025-11021
```

---

## Repository layout

```
fixes.yaml             → machine-readable index of every fix + its status
CONTRIBUTING.md        → how to add a new fix
_template/             → scaffolding for a new package fix
tools/
  new-fix.sh           → bootstrap a new package folder from the template
  verify-patches.sh    → sanity-check every patch in the repo
  submit-sru.sh        → build source-only SRU uploads for every fix (Ubuntu only)
libsoup3/              → CVE-2025-11021 / CVE-2025-4945
libyaml-syck-perl/     → CVE-2025-11683
gdcm/                  → CVE-2025-11266
```

Each package folder contains the `.patch` file, a ready-to-file `bug-report.md`, and any
packaging diffs (`changelog.diff`, `*.debdiff`).

### Add a fix

```bash
./tools/new-fix.sh <package> <CVE-id>   # scaffold from _template/
./tools/verify-patches.sh               # check everything still applies cleanly
```

### Build the SRU uploads

On an **Ubuntu** box/schroot for the target series (won't run on Debian), one
script builds source-only uploads for every fix — `pull-lp-source`, apply patch,
`quilt push -a`, `dch`, `debuild -S`:

```bash
./tools/submit-sru.sh            # build all, unsigned source packages
./tools/submit-sru.sh --sign     # sign with your Launchpad GPG key
./tools/submit-sru.sh --upload   # sign + dput ubuntu  (irreversible — yours to run)
```

The signing/`dput` (and filing the Launchpad bug per package) are intentionally
left to you: they're outward-facing and tied to your Launchpad identity.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the full workflow.

---

<sub>Maintained by <b>Valentín Torassa</b> · part of the <b>VT Security</b> toolset ·
companion to <a href="https://github.com/ValentinTorassa/PhantomLog">PhantomLog</a> and
<a href="https://github.com/ValentinTorassa/VT-SecretShare">VT-SecretShare</a></sub>
