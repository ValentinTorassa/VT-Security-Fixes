<!-- Launchpad bug: https://bugs.launchpad.net/ubuntu/+source/libyaml-syck-perl/+filebug
     Title: [SRU] libyaml-syck-perl: CVE-2025-11683 OOB read on empty-key YAML hashes -->

**[Impact]**

libyaml-syck-perl in jammy and noble is vulnerable to CVE-2025-11683: when
parsing a YAML hash whose key points to an empty value, the `qstr` scalar
buffer is allocated but never null-terminated, leading to an out-of-bounds
read in `token.c`. Reachable from any application that parses untrusted YAML
with YAML::Syck. Fixed in ESM but `needed` in the standard pocket.

**[Affected releases]**

- jammy: `needed` (base 1.34-1)
- noble: `needed` (base 1.34-2)

**[Fix]**

Backport of upstream commit dcf4c84 (first released in 1.36). Initializes
`qstr[0] = '\0'` at each allocation site in `token.c` and drops the redundant
`str` branch in the parser handler. DEP-3 patch:
`libyaml-syck-perl/CVE-2025-11683.patch`.

**[Test Plan]**

1. `pull-lp-source libyaml-syck-perl <series>`; apply the patch and build.
2. Parse `{"": }`-style YAML (empty-value key) and confirm no OOB read under
   AddressSanitizer.
3. Run the package test suite (`t/`); all load/dump round-trips must pass.

**[Where problems could occur]**

The change only adds null terminators and removes a dead branch, so behaviour
for valid YAML is unchanged. Regression risk is low; the test suite covers
scalar/string round-tripping that the removed `str` branch touched.

**[Other info]**

- Ubuntu CVE tracker: https://ubuntu.com/security/CVE-2025-11683
- Upstream fix: https://github.com/cpan-authors/YAML-Syck/commit/dcf4c8477b82ef439f43fd20dc099082d096df02
