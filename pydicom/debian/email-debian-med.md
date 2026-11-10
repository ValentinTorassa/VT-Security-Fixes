<!-- SENT on 2026-11-10 17:21 UTC from valentintorassacolombero@gmail.com (body below the "---" line).
     To:      debian-med@lists.debian.org
     Cc:      Andreas Tille <tille@debian.org>, Emmanuel Arias <eamanu@debian.org>
     Subject: pydicom: CVE-2026-32711 for trixie (2.4.3-2+deb13u1)
     Attach:  pydicom_2.4.3-2+deb13u1_trixie.debdiff
     Uploaders in debian/control are Yaroslav Halchenko and Michael Hanke. The
     last upload (2.4.3-2, April 2025) is signed by Étienne Mollier.
     The trixie-pu request (trixie-pu-request.md) goes after the team replies,
     not together with this mail. -->
---

Hi,

After gdcm (#1153126) I looked for other Debian Med packages that read
medical image files and still have open CVEs in trixie. pydicom is one
of them, and I have an update ready if the team wants it.

pydicom 2.4.3-2 in trixie is affected by CVE-2026-32711 (#1131492). A
crafted DICOMDIR can set Referenced File ID to a path outside of the
File-set root, and FileSet then reads, copies or moves those files. The
security tracker marks it no-dsa (minor issue). Unstable and forky are
fixed since 3.0.2-1.

Upstream also released the fix for the 2.4 series, as 2.4.5 (commit
ed4ddea). I took the changes to fileset.py and their tests from that
commit and left out the rest (version number, CI configuration, typos
in other files). The result is 2.4.3-2+deb13u1.

What I checked, in clean trixie containers:

- Full build with dpkg-buildpackage. The test suite goes from 2110
  passed to 2117 passed.
- The four new tests for this issue fail against the old fileset.py and
  pass with the new one.
- lintian shows nothing new.
- The patch replaces a private property of RecordNode (_file_id) with a
  method (file_id_path). None of the packages in trixie that depend on
  python3-pydicom use it: heudiconv, python3-dcmstack,
  python3-dicompylercore, python3-guiqwt and python3-nibabel.

One thing for you to decide: the new tests use pyfakefs, so the update
adds python3-pyfakefs <!nocheck> to Build-Depends. Trixie has 5.8.0-1
and the tests pass with it. If you would rather not add a build
dependency in a stable update, I can leave those tests out of the patch.

Would it be all right if I file the trixie-pu request for this? As with
gdcm, I would need a sponsor for the upload. The debdiff is attached
(601 lines, most of them tests).

I also have an update for invesalius in trixie (CVE-2024-42845 and
CVE-2024-44825). The second one is still open in unstable, so I replied
in #1136204 first, with a patch and test results.

Bookworm (2.3.1-1) is affected as well. I have not looked at it yet.

I am not subscribed to the list, so please keep me in Cc.

Thanks,
Valentín Torassa
