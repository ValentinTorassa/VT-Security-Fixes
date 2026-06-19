<!-- Launchpad bug: https://bugs.launchpad.net/ubuntu/+source/libsoup3/+filebug
     Title: [SRU] libsoup3: CVE-2025-11021 OOB read in cookie date parsing -->

**[Impact]**

libsoup3 in jammy is vulnerable to CVE-2025-11021 (and the related
CVE-2025-4945): an out-of-bounds read in cookie expiration-date parsing caused
by an integer overflow in `parse_timezone()` and missing range validation in
the date/time parsers (`soup-date-utils.c`). A malicious server can trigger it
via a crafted `Set-Cookie` date. Fixed in ESM (`esm-apps/jammy: released
(3.0.7-0ubuntu1+esm5)`) but `needed` in the standard pocket.

**[Affected releases]**

- jammy: `needed` (base 3.0.7-0ubuntu1) — all later releases already patched.

**[Fix]**

Backport of GNOME libsoup MR !473 (first released upstream in 3.4.0). Adds
range checks to `parse_day`/`parse_year`/`parse_time`, overflow guards in
`parse_timezone`, and `g_date_valid_dmy()` validation in `parse_textual_date`.
DEP-3 patch: `libsoup3/CVE-2025-11021-CVE-2025-4945.patch`.

**[Test Plan]**

1. `pull-lp-source libsoup3 jammy`; apply the patch and build.
2. Feed a cookie with an out-of-range timezone/date string (e.g. via the
   cookie-jar test) and confirm it is rejected with no OOB read (verify under
   AddressSanitizer).
3. Run the libsoup test suite; cookie/date tests must still pass.

**[Where problems could occur]**

The change only tightens validation in the date parsers, so previously-accepted
malformed dates are now rejected. Regression risk is low; the one behavioural
note is the `soup_date_time_is_past` optimization threshold moving 2020 → 2025
(matches upstream).

**[Other info]**

- Ubuntu CVE tracker: https://ubuntu.com/security/CVE-2025-11021
- Related: https://ubuntu.com/security/CVE-2025-4945
- Debian bug: https://bugs.debian.org/1116469
- Upstream fix: https://gitlab.gnome.org/GNOME/libsoup/-/merge_requests/473
