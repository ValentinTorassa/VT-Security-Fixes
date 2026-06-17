# Ubuntu Security Fixes

Patches for open CVEs in Ubuntu **universe** packages — community-maintained packages that don't receive automatic security updates from Canonical.

All three CVEs below already have fixes published in the **ESM (Ubuntu Pro)** pocket. The patches here bridge the gap to the standard pocket (what most users run).

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
2. **Download source**: `pull-lp-source <pkg> jammy`
3. **Apply patch**: copy `.patch` into `debian/patches/`, add to `series`
4. **Changelog**: `dch -v "<version>.1" -D jammy-security "SECURITY UPDATE: ..."`
5. **Build & upload**: `debuild -S -sa && dput ubuntu ../*.changes`

> The patches are DEP-3 formatted — they include Origin, Bug links, and upstream commit references. Ready for `debian/patches/`.

---

## How to check if a fix was merged

The merge doesn't happen on GitHub — it happens on **Launchpad** (Ubuntu's platform). Here's how to track each step:

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

## Repository structure

```
libsoup3/            → CVE-2025-11021 / CVE-2025-4945
libyaml-syck-perl/   → CVE-2025-11683
gdcm/                → CVE-2025-11266
```

Each folder contains the `.patch` file and packaging diffs (`changelog.diff`, `series.diff`).
