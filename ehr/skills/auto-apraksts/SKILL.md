---
name: auto-apraksts
description: Uzraksta video aprakstus (caption tekstus) Instagram, TikTok, Facebook un YouTube konkrētā EHR zīmola balsī (EHR, SuperHits, Latviešu Hiti, EHR+ krieviski, Retro FM). Lieto, kad lietotājs saka "uzraksti aprakstu", "apraksts šim video", "caption šim", "teksts postam", vai iemet video/transkriptu/scenāriju un prasa tekstu publicēšanai.
---

# auto-apraksts (EHR)

No video, transkripta vai scenārija uztaisa gatavus aprakstus katrai platformai tā zīmola
balsī, kuram video paredzēts. Balss nāk no zīmola profila failiem pakā, ne no galvas.

## Pirms sāc

1. Config: `~/.ehr/config.json` (nav → "vispirms uzstādīšana, viens vārds: uzstādi", palaid
   `uzstadi`, stop). Noklusējuma zīmols = config `zimols`; platformas = config `platforms`.
2. Pakas mape (turpmāk `$PAKA`; bloku iekļauj KATRĀ Bash izsaukumā, kur to lieto):
```bash
PAKA="${CLAUDE_PLUGIN_ROOT}"
if [ ! -f "$PAKA/zimoli/zimoli.json" ]; then
  F="$(find ~/.claude/plugins -path '*ehr*' -name zimoli.json 2>/dev/null | sort -r | head -1)"
  [ -n "$F" ] && PAKA="$(cd "$(dirname "$F")/.." && pwd)" || echo "KĻŪDA: zīmolu faili nav atrasti, pārinstalē paku (/plugin install ehr@ehr-paka)"
fi
```
3. **Zīmols**: (1) lietotājs pasaka, (2) faila/mapes nosaukumā ir zīmola vārds, (3) blakus video
   ir `.captions-meta.json` (no auto-captions) ar `zimols`, (4) citādi config `zimols`.
   Ja divdomīgi, pajautā VIENU jautājumu: "Kuram zīmolam šis video?" Nekad neraksti "vispārīgā
   radio balsī", katram zīmolam ir savs profils.
4. **Izlasi zīmola profilu** `$PAKA/zimoli/<atslēga>.md` (ehr, superhits, latviesuhiti, ehrplus,
   retrofm) PILNĪBĀ pirms raksti. Tur ir balss īsumā, garumi, emoji, hashtagi, CTA formulas,
   ko nedarīt un īsti paraugi. `$PAKA/zimoli/zimoli.json` dod nosaukumu, krāsu, valodu, handles.

## Ieeja

- **Transkripts** (labākais avots): ja video jau titrēts, blakus tam ir `<nosaukums>.captions.md`
  (teksts jau izlabots). Ņem to.
- **Video fails bez transkripta**: palaid auto-captions 1. soli (`make_captions.py`, tas uztaisa
  tabulu bez rendera) un strādā no tabulas. Ja lietotājs titrus negrib, tabulu vari atstāt.
- **Scenārijs vai teksts**: strādā no tā.
- **Tikai temats** ("rīt ir Superhits rīta šova epizode ar X"): pajautā 2 līdz 3 faktus
  (kas video notiek, kāda ir atslēgas frāze/joks, vai ir aicinājums: klausies, balso, piedalies),
  tikai tad raksti.

## Rakstīšana

1. Formula: **āķis pirmajā rindā → viena doma → (ja ir) aicinājums.** NEKAD neatstāsti, kas
   video notiek pa kadriem: video pats to parāda.
2. Āķis = pirmā rinda, kas redzama pirms "vairāk". Tai jāstrādā arī bez video.
3. Katrai platformai no config `platforms` savs variants; limiti un ieražas
   `references/platformu-limiti.md`. Ja zīmola profils saka, ka zīmols kādā platformā raksta
   citādi (piem., TikTok īsāk, bez hashtagiem), profils ir pārāks par vispārīgo tabulu.
4. Valoda no zīmola: EHR+ un Retro FM raksta krieviski (ja lietotājs nesaka citādi), pārējie latviski.
   Ja profils rāda angļu ieskaitījumus vai jauktu valodu, dari tāpat, tikai tik, cik paraugos.
5. Zīmola profila paraugos atrodi tuvāko līdzīgo (tas pats formāts: intervija studijā, dj joks,
   konkurss, dziesmas premjera, pasākums) un turies pie tā ritma un garuma.
6. Emoji, hashtagi, lielo burtu lietojums, personu un raidījumu pieminēšana: tikai tā, kā zīmola
   profilā, tādā pašā daudzumā. Ja profils saka "hashtagi 0", tad 0.
7. Nekad neizdomā faktus: dīdžeju vārdus, laikus, dziesmu nosaukumus, balvas ņem no transkripta
   vai lietotāja. Ja trūkst, atstāj `[?]` un pasaki, kas jāaizpilda.
8. Domuzīmes (—): EHR, SuperHits un Latviešu Hiti tās nelieto (defise "-" ar atstarpēm vai jauns teikums).
   EHR+ un Retro FM oriģinālos tās ir; tur drīkst, bet ne vairāk kā vienu uz aprakstu, citādi tas skan pēc AI.

## Izvade

Saglabā `apraksts.md` tajā pašā mapē, kur video/transkripts (darba mapē; ja video vēl nav
darba mapē, izveido `<darbaMape>/<datums>-<nosaukums>/`). Nekad uz Desktop.

**Katras platformas GALA teksts ir fenced ``` blokā zem platformas virsraksta.** Ārpus blokiem
ir piezīmes, kas nekad neaiziet publiski. Tā cilvēks kopē bloku un ielīmē.

````markdown
# Apraksts: <video nosaukums>
Zīmols: <nosaukums> | Datums: <šodiena> | Avots: <transkripts/scenārijs> | Statuss: melnraksts

## Instagram
```
<gala teksts>
```

## TikTok
```
<gala teksts>
```

## Facebook
```
<gala teksts>
```

## YouTube
Virsraksts:
```
<līdz 100 zīmēm>
```
Apraksts:
```
<gala teksts>
```
<piezīmes ārpus blokiem: kas jāaizpilda, alternatīvs āķis, ja vajag>
````

Parādi visus variantus čatā, saņem labojumus, atzīmē statusu "apstiprināts". Ja lietotājs
prasa "vēl variantu", dod 2 alternatīvus āķus tai pašai platformai, ne visu no jauna.

## Cikls ar zīmola profilu

Kad cilvēks aprakstu būtiski IZLABO ("mēs tā nerakstām", "šo vārdu nelietojam"): pieraksti
korekciju `~/.ehr/labojumi.md` ar datumu, zīmolu un citātu (pirms/pēc). Šo failu Edgars
periodiski ieliek zīmola profilā pakā, un nākamais atjauninājums to atnes visiem datoriem.
Pasaki cilvēkam vienu rindiņu: "Pierakstīju, nākamreiz tā vairs nedarīšu."
