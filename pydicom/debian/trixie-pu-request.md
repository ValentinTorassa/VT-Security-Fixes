<!-- DRAFT - DO NOT SEND YET.
     Send only after debian-med replies to email-debian-med.md. If the team
     prefers the update without the new build dependency, rebuild without the
     pyfakefs tests and regenerate the debdiff first.
     File it with `reportbug release.debian.org` (type "pu", suite trixie) or by
     mail to submit@bugs.debian.org with these pseudo-headers, attaching
     pydicom_2.4.3-2+deb13u1_trixie.debdiff from this folder.
     The "I reviewed all changes and I approve them" box is left unticked on
     purpose: tick it after reading the debdiff.
     If the sponsor uploads with a different debian/changelog date, regenerate
     the debdiff. -->

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
All on amd64, in fresh debian:trixie containers updated on 2026-11-10:
- Full build with dpkg-buildpackage -us -uc. The patch applies without
  fuzz.
- Upstream test suite at build time: 2110 passed with 2.4.3-2 and 2117
  passed with this update. The seven additional tests come with the
  patch.
- The four new tests that cover this issue fail against the fileset.py of
  2.4.3-2 and pass with this update.
- lintian: no new tags compared with 2.4.3-2.
- Reverse dependencies in trixie (heudiconv, python3-dcmstack,
  python3-dicompylercore, python3-guiqwt, python3-nibabel): none of them
  uses RecordNode._file_id, the private property that the patch replaces.

[ Risks ]
Low. The patch is upstream's own fix for the 2.4 series (commit ed4ddea,
released as 2.4.5), limited to pydicom/fileset.py and its tests. It adds
a check that every Referenced File ID is relative and resolves inside of
the File-set root, and raises PermissionError otherwise. A DICOMDIR that
refers to files outside of its own directory is rejected from now on,
which is the intended change. One private property, RecordNode._file_id, becomes the
method RecordNode.file_id_path().

The new tests need pyfakefs, so python3-pyfakefs <!nocheck> is added to
Build-Depends. Trixie has 5.8.0-1 and the tests pass with it.

[ Checklist ]
  [x] *all* changes are documented in the d/changelog
  [ ] I reviewed all changes and I approve them
  [x] attach debdiff against the package in (old)stable
  [x] the issue is verified as fixed in unstable

[ Changes ]
  * CVE-2026-32711.patch (upstream ed4ddea): reject Referenced File IDs
    that point outside of the File-set root when a DICOMDIR is loaded,
    copied or written.
  * debian/control: add python3-pyfakefs <!nocheck> to Build-Depends for
    the tests added by that patch.
  * debian/patches/series and debian/changelog updated accordingly.

[ Other info ]
I am not a Debian member, so the upload will need a sponsor from the
Debian Med team.
