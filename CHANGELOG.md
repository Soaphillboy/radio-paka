# CHANGELOG

## 1.0.0 (2026-08-17)

Pirmais izlaidums: EHR komandas datoru paka (V1 papildinājums dashboardam).

- `uzstadi`: 4 posmu vednis (~10 min sarunas, tehniskā daļa fonā), config `~/.ehr/config.json`
  (vārds, galvenais zīmols, dashboarda adrese, akcenti), darba mape `~/EHR-saturs`, pārbaude ar īstu video.
- `auto-captions`: 2026-07-23 apstiprinātais EHR titru stils (pāru rindas, Montserrat, captionY 1120)
  pārnests no `ehr-captions` mapes uz plugin formu; venv/Remotion `~/.ehr/`; akcenta krāsa un
  valoda pēc zīmola (`--zimols=`), zīmols pierakstās `.captions-meta.json`; make_captions.py pats
  pārslēdzas uz venv python.
- `auto-apraksts`: apraksti IG/TT/FB/YT ar 5 zīmolu balss profiliem `zimoli/*.md` (no publiskajiem
  IG/TikTok aprakstiem 2026-08), izvade `apraksts.md` ar fenced blokiem; labojumi krājas `~/.ehr/labojumi.md`.
- `lib/setup`: setup_common.sh (Apple Silicon, brew, ffmpeg, node, python, settings env) +
  setup_captions.sh (mlx-whisper, modelis, Remotion), droši atkārtojami.

Apzināti nav: cover-foto (V1.1), dashboarda API, titru redaktors.
