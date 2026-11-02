<!-- BORRADOR - NO ENVIADO. Mail en texto plano: copiar todo lo que esta debajo de la linea "---".
     To:      debian-med@lists.debian.org
     Cc:      Emmanuel Arias <eamanu@debian.org>, Étienne Mollier <emollier@debian.org>
     Subject: gdcm: finishing 3.0.24-5+deb13u1 for trixie (security fixes)
     Las direcciones salen de debian/changelog (ninguno de los dos figura en Uploaders).

     NOTAS PARA VALEN (01/11/2026)
     - Estado rechequeado hoy: el tracker sigue marcando trixie 3.0.24-5 vulnerable a
       los 6 CVE (5 <no-dsa> "Minor issue"; CVE-2026-3650 <postponed> "revisit when
       fixed upstream"). No hay DSA, no hay nada en trixie-proposed-updates, no hay bug
       pu abierto, la rama debian/trixie de salsa no se movio desde el 17/02 y no hubo
       nada sobre gdcm en debian-med ni debian-release. DLA-4652-1 es solo bullseye LTS.
     - Fechas: 13.8 sale el sabado 21/11 y proposed-updates se congela el fin de semana
       anterior (14-15/11). Con un primer mail que todavia espera respuesta, 13.8 es
       muy justo. 13.9 estaba propuesto para el 09/01/2027, pero en el hilo de
       planificacion se pidio pasarlo al 16/01/2027: confirmar la fecha antes de citarla.
     - Lo nuevo de hoy: el 19/10 nunca se habia guardado la comparacion con los binarios
       nuevos. Al correrla aparecio una REGRESION: el parche de CVE-2025-53618/53619
       (identico en unstable) hace fallar `gdcmconv --jpeg` en imagenes de tamano impar,
       por el byte de padding. Upstream ya lo arreglo (9ced0f9, "Accepth odd length",
       en 3.2.9) y unstable no lo tiene. Lo agregue como sexto parche
       (CVE-2025-53618_CVE-2025-53619-regression.patch) y una linea en el changelog,
       que ahora tiene fecha de hoy. El mail lo cuenta y ofrece llevarlo a unstable.
       No hay bug en Debian sobre esto; reportarlo/abrir el MR a master es decision tuya.
     - Otros cambios respecto del borrador del 20/10 (~/debian-work/gdcm/trixie/
       email-debian-med.md, que quedo como estaba): se corrigio lo de CVE-2026-3650 (no
       es "stable update", es postponed hasta el fix upstream), se agrego el resumen de
       pruebas y el parrafo de fechas, y se menciona DLA-4652-1.
     - Lo que quedo listo: gdcm_3.0.24-5+deb13u1_trixie.debdiff (en esta carpeta) y el
       borrador del pedido pu en trixie-pu-request.md (va DESPUES de la respuesta de
       debian-med, no junto con este mail).
     - Detalles para decidir vos:
       * Dos headers DEP-3 traen "Bug-Debian: htts://..." (typo heredado de unstable y
         del commit de Emmanuel). Lo deje igual para que los parches sean identicos a
         unstable; si preferis arreglarlo es una letra en CVE-2025-11266.patch y
         CVE-2026-3650.patch.
       * La entrada de changelog esta firmada con el gmail; el sponsor la re-fecha al
         subir. Dice "Team upload." porque el sponsor seria del equipo.
       * El borrador viejo hablaba de bookworm; lo mantuve (ofrecerlo a LTS aparte).
         Ojo: el debdiff de bookworm NO tiene el arreglo de la regresion.
       * Este repo es PUBLICO: la rama gdcm-trixie-pu quedo solo local, sin push. -->

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
yet. I added it to the trixie update as a separate patch, and I can
prepare the same change for unstable.

Would it be all right if I finish debian/trixie this way and open a
merge request on salsa? If you would rather handle it yourselves, or if
there is a reason it was held back, I am happy to step back. If the MR
is accepted I would then file the trixie-pu request, and I would need a
sponsor for the upload. The proposed-updates freeze for 13.8 is in two
weeks, which is probably too soon, so I would aim for the point release
after that. The debdiff is ready to share.

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
