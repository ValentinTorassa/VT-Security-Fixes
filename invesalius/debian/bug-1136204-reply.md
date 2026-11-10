<!-- DRAFT - NOT SENT. Read the patch and the test results before sending.
     To:      1136204@bugs.debian.org
     Cc:      Christoph Jahnke <dev@cjahnke.de>, Andreas Tille <tille@debian.org>,
              Santiago Vila <sanvila@debian.org>
     Subject: Re: Bug#1136204: invesalius: CVE-2024-44825
     Attach:  ../CVE-2024-44825.patch
     "Control: tags -1 + patch" is a BTS command: it must stay as the first
     line of the body.
     The trixie update (invesalius_3.1.99998-7+deb13u1_trixie.debdiff in this
     folder) is not proposed here. The release team wants a fix in unstable
     before it accepts it in a point release, so this reply comes first. -->
---

Control: tags -1 + patch

Hi,

Christoph asked in July whether someone could test his patch with a
compressed and an uncompressed .inv3 file. I did that today. I am also
attaching a shorter patch that I had prepared for the same problem, in
case it is useful to have both.

Setup: 3.1.99998-8 rebuilt with dpkg-buildpackage in a fresh debian:sid
container (amd64, Python 3.14.10), once with Christoph's
0011-fix-cve-2024-44825.patch as it is on his salsa repository today,
and once with the attached patch. Each build was installed in the
container and tested as an unprivileged user.

Both builds give the same results:

- debian/tests/run-unit-test passes.
- Cranium.inv3 from invesalius-examples is a tar.gz. I repacked it as a
  plain tar as well. Extract() returns the same 11 files with the same
  contents for both forms, and so does Extract_() for the tar.gz.
- "invesalius3 --no-gui <project> --export-project out.hdf5" works with
  both forms. The two HDF5 files are equal except for the export date.
- Four crafted projects write nothing outside of the destination
  directory: a member with "..", a member with an absolute name, a
  symlink followed by a member that goes through it, and a first member
  in an absolute directory. The unpatched code writes outside in three
  of the four cases. I ran that part with 3.1.99998-7 in trixie, whose
  project.py is identical to the one in -8.

The differences I see between the two patches:

- Christoph's patch checks the names itself and raises ValueError on the
  first unsafe member, so such a project is rejected as a whole. The
  attached one uses tarfile's "data" filter, the mechanism upstream uses
  (with tar_filter). It strips a leading "/" and extracts that member
  inside of the destination. For "..", for links that point outside and
  for special files it raises a tarfile.FilterError. The list of files
  that Extract() returns is built from the filtered members.
- The attached patch is smaller (11 lines added and 11 removed, against
  70 and 25), which may matter for a stable update. It needs Python 3.12
  or later. Unstable has 3.14 and trixie has 3.13.
- In Christoph's patch the helper within_dest() is defined but never
  called. The check that does the work is the abspath()/startswith() one
  further down, so this is only cosmetic.

As far as I can tell either one fixes the problem, so please take
whichever you prefer.

One more thing I noticed while testing: invesalius-bin 3.1.99998-8 from
the archive does not work in unstable at the moment. It ships its
extension modules only as cpython-313 and has no dependency on the
Python version, so with python3 3.14 "from invesalius_cy import
floodfill" fails with an ImportError. Both "invesalius3 --no-gui" on the
sample project and debian/tests/run-unit-test stop there, which would
explain the failing autopkgtest in the migration excuses. A rebuild is
enough (both test builds above work), so the next upload fixes it. I can
file it as a separate bug if that helps.

For trixie: 3.1.99998-7 is affected by this bug and by CVE-2024-42845
(#1082875, fixed in unstable in -8). Both are marked no-dsa. I have a
3.1.99998-7+deb13u1 debdiff with the two fixes, built and tested the
same way in a trixie container. Once this bug is fixed in unstable I
would like to propose it to the team for a point release, if that is
welcome.

Thanks,
Valentín Torassa
