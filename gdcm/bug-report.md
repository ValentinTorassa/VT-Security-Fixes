<!-- Launchpad bug: https://bugs.launchpad.net/ubuntu/+source/gdcm/+filebug
     Title: [SRU] gdcm: CVE-2025-11266 OOB write in DICOM fragment parsing -->

**[Impact]**

gdcm in jammy, noble and questing is vulnerable to CVE-2025-11266: an
out-of-bounds write while parsing malformed DICOM files containing
encapsulated PixelData fragments. When `GetByteValue()->GetLength()` is less
than 3, an unsigned integer underflow drives an out-of-bounds buffer access in
`gdcmSequenceOfFragments.h`. Reachable by opening a crafted DICOM file.

**[Affected releases]**

- jammy: `needed`
- noble: `needed`
- questing: `needed`

**[Fix]**

Backport of upstream commit 5829c95 (first released in 3.2.2). Adds a
`bv->GetLength() >= 3` bounds check before the buffer access. DEP-3 patch:
`gdcm/CVE-2025-11266.patch`.

**[Test Plan]**

1. `pull-lp-source gdcm <series>`; apply the patch and build.
2. Open a crafted DICOM file with a < 3-byte encapsulated fragment and confirm
   it is rejected without an OOB write (verify under AddressSanitizer).
3. Confirm valid DICOM files still load (run the gdcm test data).

**[Where problems could occur]**

The change only adds a length guard before an existing access, so valid files
are unaffected. Regression risk is low.

**[Other info]**

- Ubuntu CVE tracker: https://ubuntu.com/security/CVE-2025-11266
- Debian bug: https://bugs.debian.org/1122862
- Upstream fix: https://github.com/malaterre/GDCM/commit/5829c95c8ac3afa9a3a3413675e948959c28a789
