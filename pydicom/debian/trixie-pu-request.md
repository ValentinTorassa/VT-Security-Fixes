# Superseded: track the existing release-team request

Verified on 2026-11-16: Karsten Schöke confirmed that he already filed
[Debian bug #1148120](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1148120)
on 2026-09-17. It is awaiting release-team approval for
pydicom/2.4.3-2+deb13u1.

**Do not submit this draft to submit@bugs.debian.org.** Continue under
1148120@bugs.debian.org and coordinate any updated debdiff with the maintainers.
The unsent draft below is retained only as preparation/history.

---

<!-- SUPERSEDED - do not file a duplicate of #1148120. Not sent.
     Andreas approved filing on 2026-11-16 and merged MR !1.
     The attached debdiff must be the 2026-11-15 Salsa trixie version,
     SHA-256 6c969a38fba21de307726f4d71990bd3e3c5946e52cf545a17ea57eea10c0f93.
     Leave the personal review checkbox unticked until Valentin reviews it.
     Reportbug/mail guidance: https://www.debian.org/doc/manuals/developers-reference/pkgs.en.html#upload-stable
     This is a release-team request, not an upload of the package. -->

To: submit@bugs.debian.org
Subject: trixie-pu: package pydicom/2.4.3-2+deb13u1

Package: release.debian.org
Severity: normal
Tags: trixie
X-Debbugs-Cc: pydicom@packages.debian.org
Control: affects -1 + src:pydicom
User: release.debian.org@packages.debian.org
Usertags: pu

[ Reason ]
pydicom 2.4.3-2 in trixie is affected by CVE-2026-32711 (#1131492), which
is fixed in unstable since 3.0.2-1. The security tracker marks it <no-dsa>
(minor issue). This update fixes it in a point release.

[ Impact ]
pydicom.fileset.FileSet trusts the Referenced File ID values of a DICOMDIR.
A crafted DICOMDIR can point them outside of the File-set root, and an
application that loads it and then calls FileSet.copy() or FileSet.write()
reads, copies or moves files outside of that directory with the user's
permissions.

[ Tests ]
The proposed source is the Debian Med debian/trixie branch including MR !1,
merged by Andreas Tille on 2026-11-16. Its changelog, control, gbp.conf,
patch and patch series match the source built on 2026-11-15:
- Full build with dpkg-buildpackage -us -uc in a Debian trixie container
  on amd64.
- Upstream test suite at build time: 2117 passed, 535 skipped, 30 warnings.
  The earlier 2.4.3-2 baseline run had 2110 passing tests.
- The four issue-specific regression tests failed against the original
  fileset.py and passed with the backport in the 2026-11-10 checks.
- Lintian was run on the built packages: no errors. Existing documentation
  warnings remain, including the missing pydicom manual page and references
  to the package build path in the generated documentation.
- Salsa CI passed build, build i386, build source, test-build-any,
  test-build-all, lintian, autopkgtest, piuparts, blhc and test-uscan.

The debrebuild CI job failed. I have not diagnosed that failure; Andreas
merged MR !1 despite the reproducibility issue. The job is available at:
https://salsa.debian.org/med-team/pydicom/-/jobs/10658822

[ Risks ]
The patch is the existing Debian Med backport of upstream's fix for the
2.4 series (commit ed4ddea, released as 2.4.5). It checks that Referenced
File IDs resolve inside the File-set root, raising PermissionError for
paths outside it. A DICOMDIR with external references is rejected, as
intended. The private property RecordNode._file_id is replaced by
RecordNode.file_id_path().

The upstream backport also includes its test fixture and tests, plus
small comment/formatting changes, including one comment in cli/codify.py.
The tests require python3-pyfakefs <!nocheck>; trixie has 5.8.0-1.

[ Checklist ]
  [x] *all* changes are documented in the d/changelog
  [ ] I reviewed all changes and I approve them
  [x] attach debdiff against the package in (old)stable
  [x] the issue is verified as fixed in unstable

[ Changes ]
  * 0006-Insert-CVE-2026-32711-patch.patch: the existing Debian Med
    upstream backport, with DEP-3 Origin, Bug and Bug-Debian fields.
  * debian/control: add python3-pyfakefs <!nocheck> for the new tests.
  * debian/gbp.conf: select debian/trixie and pristine-tar.
  * debian/patches/series and debian/changelog updated accordingly.

[ Other info ]
MR !1: https://salsa.debian.org/med-team/pydicom/-/merge_requests/1
Pipeline: https://salsa.debian.org/med-team/pydicom/-/pipelines/1215095
Debian Security Tracker:
https://security-tracker.debian.org/tracker/CVE-2026-32711

I am not a Debian member, so the upload will need a sponsor from the
Debian Med team. Andreas gave the go-ahead to file this request on
2026-11-16.
