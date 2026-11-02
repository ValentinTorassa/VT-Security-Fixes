<!-- DRAFT - NOT SENT. Plain-text mail: send everything below the "---" line.
     To:      debian-med@lists.debian.org
     Cc:      Emmanuel Arias <eamanu@debian.org>, Étienne Mollier <emollier@debian.org>
     Subject: gdcm: finishing 3.0.24-5+deb13u1 for trixie (security fixes)
     Addresses come from debian/changelog (neither is listed in Uploaders).
     The trixie-pu request (trixie-pu-request.md) goes after debian-med replies,
     not together with this mail. -->
---

Hi,

I would like to help get the outstanding gdcm security fixes into trixie,
and I am writing first because Emmanuel has already started this work.

The debian/trixie branch on salsa has a 3.0.24-5+deb13u1 entry with the
CVE-2025-11266 fix, prepared in February and not uploaded so far. The
security tracker still lists trixie as affected by five more issues that
are fixed in unstable since 3.0.24-11: CVE-2025-48429, CVE-2025-52582,
CVE-2025-53618, CVE-2025-53619 and CVE-2026-3650. All are marked no-dsa
as minor issues, except CVE-2026-3650, which is postponed until fixed
upstream (it now is). The same set went to bullseye LTS in DLA-4652-1.

On a local copy of debian/trixie I added the four patches from unstable
for those issues, unchanged apart from two lines of upstream commit
trailer that I left out of the CVE-2026-3650 header. They apply without
fuzz on 3.0.24-5. I extended the existing changelog entry and kept
Emmanuel's part under his name. I built it in a clean trixie container.
The autopkgtest passes and lintian shows no new warnings. I also
compared the old and new binaries on 95 sample DICOM files and with
reproducers for CVE-2025-11266 and CVE-2026-3650.

That comparison turned up one regression. The frame size check from the
CVE-2025-53618/53619 patch makes gdcmconv --jpeg fail on odd-sized
images, because of the padding byte. Upstream fixed this in 9ced0f9
("Accepth odd length", released in 3.2.9), which unstable does not have
yet. I added it to the trixie update as a separate patch and reported
it for unstable, with the same patch, as #1152837.

Would it be all right if I finish debian/trixie this way and open a
merge request on salsa? If you would rather handle it yourselves, or if
there is a reason it was held back, I am happy to step back. If the MR
is accepted I would then file the trixie-pu request, and I would need a
sponsor for the upload. The proposed-updates freeze for 13.8 is in two
weeks, which is probably too soon, so I would aim for 13.9 in January.
The debdiff is ready to share.

Some background: I prepared the Ubuntu backport of the upstream
CVE-2025-11266 fix (upstream commit 5829c95) for jammy and noble, which
is how I came to this package. This would be my first contribution to
Debian, so corrections on process are very welcome.

I have also prepared the same set for bookworm on top of the
debian/bookworm branch (3.0.21-1+deb12u1, including Étienne's
CVE-2024-* patches). As bookworm is now in LTS, I would offer that one
to the LTS team separately, unless you prefer to handle it differently.

Thanks,
Valentín Torassa
