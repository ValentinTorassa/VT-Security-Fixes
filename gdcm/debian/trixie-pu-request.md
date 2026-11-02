<!-- BORRADOR - NO ENVIAR TODAVIA.
     Va recien despues de que debian-med conteste el mail de email-debian-med.md
     y el MR en salsa este aceptado (o Emmanuel diga que lo mandes vos).
     Antes de mandarlo conviene que el arreglo de la regresion (upstream 9ced0f9) este
     tambien en unstable: el release team suele pedir que todo lo que entra por pu ya
     este arreglado en unstable, y 3.0.24-14 todavia no lo tiene.
     Se manda con `reportbug release.debian.org` (tipo "pu", suite trixie) o a mano
     a submit@bugs.debian.org con estos pseudo-headers, adjuntando
     gdcm_3.0.24-5+deb13u1_trixie.debdiff de esta carpeta.
     La casilla "I reviewed all changes and I approve them" queda sin marcar a
     proposito: la marcas vos despues de leer el debdiff.
     Si el sponsor sube con otra fecha en debian/changelog, regenerar el debdiff. -->

To: submit@bugs.debian.org
Subject: trixie-pu: package gdcm/3.0.24-5+deb13u1

Package: release.debian.org
Severity: normal
Tags: trixie
X-Debbugs-Cc: gdcm@packages.debian.org, eamanu@debian.org
Control: affects -1 + src:gdcm
User: release.debian.org@packages.debian.org
Usertags: pu

[ Reason ]
gdcm 3.0.24-5 in trixie is affected by six CVEs that are fixed in
unstable since 3.0.24-11: CVE-2025-11266, CVE-2025-48429, CVE-2025-52582,
CVE-2025-53618, CVE-2025-53619 and CVE-2026-3650. The security tracker
marks the first five <no-dsa> (minor issue) and CVE-2026-3650 <postponed>
until fixed upstream, which it now is. This update fixes them in a point
release.

[ Impact ]
Opening a crafted DICOM file with anything that uses libgdcm (gdcminfo,
gdcmconv, python3-gdcm, the VTK bindings, or third-party viewers) can
cause out-of-bounds reads and an out-of-bounds write in the
encapsulated-fragment, RLE, JPEG and overlay code paths, or a
multi-gigabyte allocation from a single Value Length field (memory
exhaustion).

[ Tests ]
All on amd64, in fresh debian:trixie containers updated on 2026-11-01:
- Full build (arch any and all) with dpkg-buildpackage -us -uc. All
  patches apply without fuzz.
- autopkgtest (run-unit-test) passes with the null runner in a separate
  clean container.
- lintian: no new errors or warnings compared with 3.0.24-5+b3. Two new
  informational tags: out-of-date-standards-version (from the new
  changelog date) and patch-not-forwarded-upstream on
  CVE-2025-48429.patch, which is an upstream commit.
- Exported dynamic symbols: none removed. One weak symbol added,
  gdcm::RLEHeader::Read(std::istream&), from the CVE-2025-48429 patch.
- CVE-2026-3650: the upstream test added by the patch (not built in
  Debian) compiled against libgdcm-dev. Peak RSS is 1,054,496 KiB with
  3.0.24-5+b3 and 6,724 KiB with this update, which rejects the 1 GiB
  Value Length before allocating.
- CVE-2025-11266: two crafted files (a last fragment of 0 or 2 bytes
  followed by a bogus tag) crash gdcmdump 3.0.24-5+b3 with SIGSEGV. With
  this update the new length check stops it before the read, and the
  assertion that follows aborts, as in unstable.
- 95 sample files (pydicom 2.4.3 test data) through gdcminfo, gdcmdump,
  gdcmconv --raw and gdcmconv --jpeg, with the old and new binaries:
  91 give identical results. The four differences:
  * MR_truncated.dcm, truncated on purpose, is now rejected by the
    CVE-2026-3650 length check.
  * MR_small_padded.dcm, with 128 bytes of padding after the pixel
    data, is no longer re-encoded to JPEG because of the
    CVE-2025-53618/53619 frame size check. Unstable and upstream behave
    the same.
  * liver_1frame.dcm and liver_expb_1frame.dcm (1-bit) already crashed
    gdcmconv --jpeg in 3.0.24-5+b3 (SIGSEGV). They now stop on an
    assertion (SIGABRT) instead.
  Without CVE-2025-53618_CVE-2025-53619-regression.patch, two more files
  (3x3 RGB images) could no longer be JPEG-encoded. With it their
  output is identical to 3.0.24-5+b3.

[ Risks ]
Low. Five of the six patches are the ones in unstable since 3.0.24-11
(June 2026, now 3.0.24-14 in forky), applied unchanged except for two
lines of upstream commit trailer dropped from one header. Four of those
are small bounds or length checks in parsing code. The largest, for
CVE-2025-48429, rewrites the file-local RLEHeader class in
gdcmRLECodec.cxx and does not touch the public API. The CVE-2026-3650
patch also adds an upstream unit test that is not built in Debian
(GDCM_BUILD_TESTING is OFF). The sixth patch is upstream's one-line fix
(9ced0f9, released in 3.2.9) for a regression introduced by the
CVE-2025-53618/53619 check. It lets the JPEG encoder accept the one
padding byte of odd-length values. Files that are truncated or carry
extra trailing pixel data are now rejected in some paths, as in
unstable. The bullseye LTS update DLA-4652-1 shipped the same CVE fixes.

[ Checklist ]
  [x] *all* changes are documented in the d/changelog
  [ ] I reviewed all changes and I approve them
  [x] attach debdiff against the package in (old)stable
  [x] the issue is verified as fixed in unstable

[ Changes ]
  * CVE-2025-11266.patch (upstream 5829c95): length check before reading
    the last bytes of an encapsulated PixelData fragment
    (gdcmSequenceOfFragments.h). Already on the debian/trixie branch on
    salsa (Emmanuel Arias, February 2026), never uploaded.
  * CVE-2025-52582.patch (upstream 14825ce): refuse to extract overlays
    when overlay and image information are inconsistent
    (gdcmPixmapReader.cxx, gdcmJPEG2000Codec.cxx, gdcmOverlay.h).
  * CVE-2025-53618_CVE-2025-53619.patch (upstream f0e359c): check the
    frame size against the buffer size in JPEGBITSCodec::InternalCode.
  * CVE-2025-48429.patch (upstream 0393310): validate the RLE header
    (segment count, truncated header, offsets beyond the buffer) in
    RLECodec.
  * CVE-2026-3650.patch (upstream 9d65a21): reject Value Lengths larger
    than the remaining stream before allocating, in the explicit and
    implicit data element and fragment readers. Also guard two
    length - N accesses in SequenceOfFragments.
  * CVE-2025-53618_CVE-2025-53619-regression.patch (upstream 9ced0f9):
    accept a frame one byte longer than expected (odd-length padding)
    in the same check.
  * debian/patches/series and debian/changelog updated accordingly.

[ Other info ]
The debian/trixie branch on salsa already carries the 3.0.24-5+deb13u1
changelog entry and CVE-2025-11266.patch. This update extends that entry.
Unstable (3.0.24-14) does not have upstream 9ced0f9 yet. The same patch
is proposed there in <LINK: MR o bug para unstable>. I am not a Debian
member, so the upload
will need a sponsor from the Debian Med team.
