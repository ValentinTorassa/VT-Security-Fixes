# Adding a new fix

This repo is a rolling collection of security fixes for **Ubuntu universe**
packages — packages that do **not** receive automatic security updates outside
of ESM (Ubuntu Pro). Each fix lives in its own per-package directory and ships
everything a sponsor needs to push a Stable Release Update (SRU).

## When does a CVE belong here?

A package is a candidate if **all** of these hold:

- It lives in **universe** (`apt-cache show <pkg> | grep ^Section` → `universe/...`).
- The CVE is **`needed`** in a standard pocket on [ubuntu.com/security](https://ubuntu.com/security/cves)
  (i.e. not yet fixed for non-Pro users).
- A clean **upstream fix** exists (commit / MR / release) we can backport DEP-3 style.

If it's already `released` everywhere in the standard pocket, skip it.

## Scaffold a new fix

```bash
tools/new-fix.sh <package> <CVE-ID>
# e.g.
tools/new-fix.sh curl CVE-2026-12345
```

This creates `<package>/` from `_template/` with the CVE id filled in. Then:

1. **`<package>/CVE-XXXX-NNNNN.patch`** — paste the upstream diff under the
   DEP-3 header. Keep the diff body **byte-for-byte from upstream** (don't
   re-indent it by hand — that's how patches stop applying). Fill in `Origin`,
   `Applied-Upstream`, and any `Bug-*` links.
2. **`<package>/changelog.diff`** — one `SECURITY UPDATE` stanza per affected
   release. Confirm the base version first with `rmadison <package>`.
3. **`<package>/bug-report.md`** — the Launchpad bug text a sponsor will read.
4. Add a row to the status table in [`README.md`](README.md) and to
   [`fixes.yaml`](fixes.yaml).

## Verify before you commit

```bash
tools/verify-patches.sh          # checks every patch is DEP-3 + well-formed
```

For a real build you need an Ubuntu box (or chroot) for the target series —
this is **not possible on a plain Debian/other host**:

```bash
pull-lp-source <package> <series>        # e.g. jammy
cp ../<package>/CVE-*.patch debian/patches/
echo CVE-XXXX-NNNNN.patch >> debian/patches/series
quilt push -a                            # must apply with zero fuzz errors
dch -v <version> -D <series>-security "SECURITY UPDATE: ..."
debuild -S -d -sa                        # source-only build
```

## Submit (the maintainer does this)

The actual upload is **outward-facing and irreversible** — it is always done by
the maintainer with their own Launchpad account and GPG key, never automated:

1. File a Launchpad bug per package using `bug-report.md`, then replace every
   `+bug/TODO` in the patch headers with the real bug number.
2. Sign with the GPG key registered on your Launchpad profile (the changelog
   maintainer line **must** match that key's identity).
3. Either upload directly (`dput ubuntu ../*.changes`) if you have MOTU/upload
   rights, or attach the debdiff to the bug and subscribe `ubuntu-sponsors`.

See [README.md → How to check if a fix was merged](README.md#how-to-check-if-a-fix-was-merged)
to track it from `needed` → `released`.
