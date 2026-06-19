<!-- Launchpad bug: https://bugs.launchpad.net/ubuntu/+source/<package>/+filebug
     Title: [SRU] <package>: CVE-XXXX-NNNNN <short description> -->

**[Impact]**

<package> in <affected series> is vulnerable to CVE-XXXX-NNNNN: <impact, e.g.
out-of-bounds read reachable from untrusted input>. The fix is already in the
ESM (Ubuntu Pro) pocket but `needed` in the standard pocket that non-Pro users
run.

**[Affected releases]**

- <series>: `needed` (base <base-version>)

**[Fix]**

Backport of upstream <commit/MR link> (first released in <version>). The
DEP-3 patch is attached / in this repo at `<package>/CVE-XXXX-NNNNN.patch`.

**[Test Plan]**

1. `pull-lp-source <package> <series>` and build with the patch applied.
2. <Reproducer: e.g. feed the malformed input that triggers the CVE; verify no
   crash / clean rejection under ASan.>
3. Confirm existing functionality is unchanged (run the package test suite).

**[Where problems could occur]**

The change is limited to <area>. Regression risk is <low/medium> because <reason
— e.g. it only adds bounds checks before existing reads>.

**[Other info]**

- Ubuntu CVE tracker: https://ubuntu.com/security/CVE-XXXX-NNNNN
- Upstream fix: <link>
