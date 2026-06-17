# Ubuntu Security Fixes

This repository contains prepared security patches for Ubuntu universe packages.

## CVEs addressed

### CVE-2025-11021 / CVE-2025-4945 — libsoup3 (jammy)

- **Severity**: HIGH (7.5 CVSS)
- **Issue**: Out-of-bounds read in cookie date parsing via integer overflow in parse_timezone()
- **Upstream fix**: https://gitlab.gnome.org/GNOME/libsoup/-/merge_requests/473
- **Debian bug**: https://bugs.debian.org/1116469
- **ESM already fixed**: `esm-apps/jammy: released (3.0.7-0ubuntu1+esm5)`

### CVE-2025-11683 — libyaml-syck-perl (jammy + noble)

- **Severity**: MEDIUM (6.5 CVSS)
- **Issue**: Missing null terminators in token.c causing out-of-bounds read on empty-key YAML hashes
- **Upstream fix**: https://github.com/cpan-authors/YAML-Syck/commit/dcf4c8477b82ef439f43fd20dc099082d096df02
- **ESM already fixed**: `esm-apps/jammy: released (1.34-1ubuntu0.1~esm1)`, `esm-apps/noble: released (1.34-2ubuntu0.24.04.1~esm1)`

## How to use

Each patch is a DEP-3 formatted quilt patch ready to be dropped into `debian/patches/`.

### SRU Submission Process

1. Download the Ubuntu source package:
   ```
   pull-lp-source libsoup3 jammy
   ```

2. Copy the patch into debian/patches/ and add to series

3. Update debian/changelog with a `jammy-security` entry

4. Build and upload:
   ```
   debuild -S -sa
   dput ubuntu ../<pkg>_<version>_source.changes
   ```

5. File a Launchpad bug and update the CVE tracker:
   ```
   git clone https://git.launchpad.net/ubuntu-cve-tracker
   ```

### CVE-2025-11266 — gdcm (jammy + noble + questing)

- **Severity**: MEDIUM (6.6 CVSS)
- **Issue**: Out-of-bounds write in DICOM encapsulated PixelData fragment parsing due to unsigned integer underflow
- **Upstream fix**: https://github.com/malaterre/GDCM/commit/5829c95c8ac3afa9a3a3413675e948959c28a789
- **Debian bug**: https://bugs.debian.org/1122862
- **Fixed in**: resolute/devel (3.0.24-9ubuntu1)
