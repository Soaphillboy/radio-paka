---
name: auto-captions
description: Uzliek video titrus EHR reelu stilā (Captions-app pāru izkārtojums, 2026-07 apstiprinātais paraugs) ar mlx-whisper transkripciju un Remotion renderi, akcenti zīmola krāsā (EHR, SuperHits, Latviešu Hiti, EHR+, Retro FM). Lieto, kad lietotājs saka "uzliec titrus", "notitrē", "caption", "subtitri", "titri šim video", vai iemet video/audio failu titrēšanai.
---

# Auto-captions (EHR)

Paņem video failu, transkribē ar mlx-whisper (vārdu laiki), uzliek EHR reelu stila titrus:
frāzes rādās pāros, pirmā rinda SemiBold viegli pieklusināta, otrā ExtraBold tīri balta,
rinda ielido vesela sava pirmā vārda brīdī. Akcenti zīmola krāsā pēc pieprasījuma.
Gala fails ir gatavs publicēšanai IG/TikTok/FB/YT.

## Pirms sāc

1. Config: `~/.ehr/config.json`. Ja faila nav: pasaki "vispirms uzstādīšana, viens vārds: uzstādi",
   palaid `uzstadi` skillu un apstājies.
2. Skripti dzīvo šī skilla mapē. Atrodi to tā (turpmāk `$SS`; šo bloku iekļauj KATRĀ Bash
   izsaukumā, kur lieto $SS, jo mainīgie starp izsaukumiem nesaglabājas):
```bash
SS="${CLAUDE_PLUGIN_ROOT:+$CLAUDE_PLUGIN_ROOT/skills/auto-captions}"
if [ ! -f "$SS/captions/make_captions.py" ]; then
  F="$(find ~/.claude/plugins -path '*ehr*' -name make_captions.py 2>/dev/null | sort -r | head -1)"
  [ -n "$F" ] && SS="$(cd "$(dirname "$F")/.." && pwd)" || echo "KĻŪDA: auto-captions skripti nav atrasti, pārinstalē paku (/plugin install ehr@ehr-paka)"
fi
```
3. Darba vide (venv, Whisper modelis, Remotion) dzīvo `~/.ehr/`. Ja tās nav, skripti pateiks
   "Saki Claude: uzstādi"; tad palaid `uzstadi`.

## Zīmols

Katram video ir viens zīmols, un no tā nāk akcenta krāsa un transkripcijas valoda:

| Atslēga | Zīmols | Krāsa | Valoda |
|---|---|---|---|
| `ehr` | European Hit Radio | sarkanā #E4002B | lv |
| `superhits` | SuperHits | oranžā #EF7C17 | lv |
| `latviesuhiti` | Latviešu Hiti | zilā #2B6FE0 | lv |
| `ehrplus` | EHR+ | aveņu #D41E52 | ru |
| `retrofm` | Retro FM | rozā #E32B9E | lv |

Zīmolu nosaki tā: (1) lietotājs pasaka ("Super Hits video", "tas ir EHR+"), (2) faila vai
mapes nosaukumā ir zīmola vārds, (3) citādi config `zimols` (lietotāja galvenais zīmols).
Ja divdomīgi (piem., lietotājs strādā ar vairākiem zīmoliem un nekas nav pateikts), pajautā
VIENU īsu jautājumu: "Kuram zīmolam šis video?" Padod `--zimols=<atslēga>` 1. solī; tas
pierakstās blakus video (`.captions-meta.json`), un renderis to lieto pats.

## Darbplūsma (noklusējums: renderē uzreiz, negaidi apstiprinājumu)

0. **Fails**: ja lietotājs nav iedevis failu vai precīzu ceļu, VIENMĒR vispirms pajautā,
   kur atrodas video/audio fails (ievilkt čatā vai iedot pilnu ceļu). Nemeklē pa mapēm pats.
   Der video (mp4/mov) un audio (wav/mp3/m4a). Ja fails ir Desktop vai Downloads, pirms darba
   pārcel to uz darba mapi (config `darbaMape`, apakšmape `<datums>-<nosaukums>/`), lai
   rezultāti dzīvo vienuviet; pasaki, ka pārcēli.
1. **Tabula** (transkribē, ja transkripta vēl nav):
   ```bash
   python3 "$SS/captions/make_captions.py" "<video>" --zimols=<atslēga> [--lang=lv|ru|en]
   ```
   Blakus video rodas `<nosaukums>.captions.md` (tabula), `.captions-timing.json` (laiki),
   `.captions-meta.json` (zīmols, valoda). Valoda nāk no zīmola (EHR+ = krievu), citādi
   config; ja lietotājs pasaka citu vai tā acīmredzama, padod `--lang=`.
   Ja tabula jau ir, skripts apstājas (lai nepazustu labojumi); no jauna: `--force`.
2. **Izlabo acīmredzamās transkripcijas kļūdas** captions.md tabulā pats: pareizrakstība,
   īpašvārdi, zīmolu nosaukumi (EHR, SuperHits, Latviešu Hiti, EHR+, Retro FM), dīdžeju un
   raidījumu vārdi, cipari. Īsi parādi lietotājam frāžu skaitu un aizdomīgās vietas,
   bet negaidi apstiprinājumu.
3. **Akcenti** (tikai ja config `captions.accents` ir true): pirms renderēšanas pajautā,
   kurus vārdus izcelt zīmola krāsā, piedāvā 2 līdz 4 kandidātus (zīmola vārds, cipari,
   "punch" vārdi) un izvēlētajiem ieliec `==vārds==` tabulā. Ja "nevajag", renderē bez un
   netincini. Ja `accents` ir false, akcentus nepiedāvā (bet izpildi, ja lietotājs pats prasa).
   Pastāvīgi ieslēgt/izslēgt: `python3 "$SS/../../lib/read_config.py" --set captions.accents true|false`.
4. **Renderē**:
   ```bash
   python3 "$SS/captions/caption_render.py" "<video>"
   ```
   Rezultāts: `<nosaukums>-titri.mp4` (1440x2560 burn-in) blakus video. Pēc rendera parādi
   3 vai 4 kadrus (`ffmpeg -ss <s> -i fails -frames:v 1 kadrs.jpg`) un pasaki, kur fails.
5. Labojumi: labo captions.md un palaid to pašu render komandu vēlreiz. Transkripcija
   otrreiz nenotiek, pārrenderēšana ir ātra.

Papildu režīmi (tikai ja lietotājs prasa):
- `--preview` ātrs 1080x1920 melnraksts `<nosaukums>-preview.mp4`
- `--alpha` caurspīdīgs titru overlay `<nosaukums>-titri-alpha.webm` (WebM VP9 + alpha), vienīgais
  caurspīdīgais formāts, ko CapCut saprot. Audio ievadei ieslēdzas automātiski; garums `--dur=SEC`.
- `--alpha --prores` ProRes 4444 `.mov` (2160x3840) FCP/Premiere montāžai (CapCut to NEatbalsta)
- `--y=NNNN` cits titru augstums (1080x1920 telpā), ja kadrējums nestandarta; pastāvīgi:
  `read_config.py --set captions.captionY NNNN`
- `--zimols=KEY` renderī, ja zīmols jāmaina jau esošam darbam
- `--out=/ceļš` cits izvades fails

## Tabulas atzīmes (captions.md)

- `==vārds==` = akcents zīmola krāsā (pop animācija)
- `~~vārds~~` = Instagram gradienta akcents (burti uzlec pa vienam)
- `**vārds**` neko nemaina (vecais marķieris; visi vārdi vienā izmērā)
- Izdzēsta rinda = frāzi nerāda
- Frāzi var sadalīt vairākās rindās ar to pašu # (sākums `↳`); katra apakšrinda parādās
  no sava pirmā vārda laika
- Vārdu skaitu frāzē drīkst mainīt (laiki izlīdzinās frāzes logā)
- `<nosaukums>.captions-title.json` blakus video pievieno intro virsrakstus (title/titleBehind), ja sagatavots

## Stila noteikumi

- Rindas ekrānā rādās pāros: pirmā SemiBold ~85% baltā, otrā (vai viena pati) ExtraBold tīri
  balta; pārus renderis saliek pats (>1 s pauze = jauns pāris)
- Vārdi rindā: līdz 3 (4, ja rinda īsa); grupēšanu dara make_captions.py, nepārkārto bez vajadzības
- Titru augstums captionY=1120 (kā EHR paraugā, nedaudz virs vidus)
- Video paredzēts vertikāls (9:16). Horizontālu video renderis apgriezīs (objectFit cover),
  pabrīdini pirms renderēšanas
- Fonts Montserrat, kā paraugā

## Darbs ar CapCut (EHR komanda montē tur)

- Parastais ceļš: eksportē gatavo video no CapCut (bez titriem), notitrē, publicēšanai iet
  `<nosaukums>-titri.mp4`. Titri iededzināti, CapCut vairs nevajag.
- Ja titrus vajag kā SLĀNI CapCut projektā (vēl montēs): lai eksportē video VAI tikai audio
  (WAV/MP3) no timeline SĀKUMA un iedod tev; palaid ar `--alpha` → `<nosaukums>-titri-alpha.webm`.
  CapCut pusē: Import → .webm uz treka VIRS video → pievilkt pie 0:00. Overlay sākas no nulles
  un ir tikpat garš kā eksportētais materiāls, tāpēc laiki saskan paši.
  Ja eksportē izgrieztu gabalu no vidus, titru laiki nobīdīsies, tāpēc vienmēr no sākuma.
- ProRes alpha `.mov` CapCut caurspīdīgumu nerāda, tāpēc CapCut lietotājiem vienmēr .webm.

## Gotchas

- make_captions.py pats pārslēdzas uz `~/.ehr/venv-captions` python (tur ir mlx_whisper);
  caption_render.py iet ar parasto python3
- WhisperX nelietot latviešu valodai; mlx-whisper large-v3 ar word_timestamps ir pareizais rīks
- Pirmajā reizē lejupielādējas Whisper modelis (~3 GB), tas ir normāli un notiek vienreiz
- Smagus avotus (4K, ProRes) caption_render.py pārkodē uz vieglāku proxy un pēc rendera izdzēš
- Renderis iet ar concurrency 1; 60 s video parasti renderējas 2 līdz 4 minūtēs. Ja šķiet
  "uzkāries", vispirms pārbaudi sistēmas noslodzi (citas smagas programmas, swap)
- Alpha `.webm` renderis ir lēnāks: 60 s klipam ap 8 līdz 12 min. Normāli
- Ja video ir tikai mūzika bez runas, transkripts būs tukšs vai izdomāts; rīks domāts runai
- Ja captions.md nav, vispirms make_captions.py
- Gatavo failu VIENMĒR blakus avota video (darba mapē), nekad uz Desktop
