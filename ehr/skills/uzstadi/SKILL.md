---
name: uzstadi
description: EHR pakas pirmās palaišanas vednis darbinieka datorā. Uzstāda un salabo titru un aprakstu darba vidi 4 īsos posmos (~10 min sarunas, tehniskā daļa fonā). Lieto, kad lietotājs saka "uzstādi", "setup", "sāc uzstādīšanu", "kaut kas nestrādā", "turpini uzstādīšanu", vai kad cits pakas skills atklāj, ka trūkst config vai vides.
---

# uzstadi, EHR pakas palaišanas vednis

Tu esi vienīgais vārds, kas cilvēkam jāzina: "uzstādi". Četri posmi, un šis dators prot
uzlikt EHR titrus un uzrakstīt aprakstus visiem pieciem zīmoliem. Katru posmu iesāc ar VIENU
vienkāršu teikumu, kas tūlīt notiks. Nekad nerādi kļūdu tekstus bez tulkojuma cilvēku valodā.
Runā latviski, īsi, bez tehniskiem terminiem, kur var iztikt.

## Stāvoklis un atkārtojamība

Stāvoklis dzīvo `~/.ehr/config.json` laukā `meta.setup`
(piem. `{"tehniskais": true, "intervija": true, "mape": true, "parbaude": true}`). Pirms sāc:

1. Ja config eksistē: nolasi `meta.setup`, pasaki "turpinu no X posma" un ej tikai uz nepabeigtajiem.
   Ja viss ir true un cilvēks teica "kaut kas nestrādā": palaid 1. posma skriptus vēlreiz
   (tie ir droši atkārtojami) un 4. posma pārbaudi.
2. Ja neeksistē: sāc no sākuma.
3. NEKO nedublē: mapes un failus, kas jau ir, tikai papildini.

Cilvēks var apstāties jebkurā brīdī un turpināt citā dienā ar to pašu vārdu "uzstādi".

## Pakas skriptu atrašana

Šo bloku iekļauj KATRĀ Bash izsaukumā, kur vajag `$LIB` (mainīgie starp izsaukumiem nesaglabājas):
```bash
LIB="${CLAUDE_PLUGIN_ROOT:+$CLAUDE_PLUGIN_ROOT/lib}"
if [ ! -f "$LIB/setup/setup_common.sh" ]; then
  F="$(find ~/.claude/plugins -path '*ehr*' -name setup_common.sh 2>/dev/null | sort -r | head -1)"
  [ -n "$F" ] && LIB="$(cd "$(dirname "$F")/.." && pwd)"
fi
if [ ! -f "$LIB/setup/setup_common.sh" ]; then
  echo "KĻŪDA: pakas skripti nav atrasti. Pārinstalē paku (/plugin install ehr@ehr-paka) un mēģini vēlreiz."
  exit 1
fi
```

## 0. Ievads (viens teikums)

> Uzstādīšu šajā datorā divus palīgus: **titrus** EHR stilā (saki "uzliec titrus" un iedod video)
> un **aprakstus** Instagram, TikTok, Facebook un YouTube visiem pieciem zīmoliem (saki "uzraksti
> aprakstu"). Tehniskā daļa ies fonā, pa to laiku uzdošu 4 īsus jautājumus. Sākam?

## 1. posms: tehniskā vide (fonā!)

Pasaki: "Palaižu tehnisko uzstādīšanu fonā, tā aizņem 10 līdz 20 minūtes (lejupielādē
runas atpazīšanas modeli, ~3 GB). Pa to laiku turpinām."

Palaid VISU šo kā VIENU fona komandu (run_in_background), $LIB bloks tajā pašā izsaukumā:
```bash
<LIB bloks>
bash "$LIB/setup/setup_common.sh" && bash "$LIB/setup/setup_captions.sh"
```

- `setup_common.sh` kļūdas ir cilvēkvalodā; ja tā apstājas (piem., nav Homebrew), parādi tieši
  tās komandas cilvēkam, palūdz palaist Terminālī (Homebrew prasa Mac paroli, tas ir normāli)
  un pēc tam palaid fona komandu vēlreiz.
- Ja dators nav Apple Silicon (Intel): titri nestrādās, apraksti strādās. Pasaki to godīgi,
  ieraksti `meta.setup.tehniskais = "intel"` un turpini ar 2. posmu.
- Neveiksmīga modeļa lejupielāde NAV bloķētājs (notiks pirmajā lietošanas reizē).
- Kad fons beidzas, pasaki vienu rindiņu: "Tehniskā daļa gatava." Atzīmē `meta.setup.tehniskais = true`.

## 2. posms: 4 jautājumi → config

Config ceļš `~/.ehr/config.json`, šablons `$LIB/../templates/config.example.json`. Ja config
jau ir, tikai papildini tukšos laukus. Jautā pa vienam, katru ar variantiem vai piemēru:

1. **Vārds**: "Kā tevi sauc, tieši tā, kā tavs profils dashboardā?" → `vards`
2. **Galvenais zīmols**: "Ar kuru zīmolu tu strādā visvairāk: EHR, SuperHits, Latviešu Hiti,
   EHR+ vai Retro FM? Ja ar vairākiem, kurš ir biežākais? Katram video zīmolu var pateikt
   atsevišķi, šis ir tikai noklusējums." → `zimols` (atslēga: ehr / superhits / latviesuhiti /
   ehrplus / retrofm). Valodu ieliec pēc zīmola (`ehrplus` un `retrofm` → `language: "ru"`, citi → `"lv"`),
   ja cilvēks nepasaka citādi.
3. **Dashboards**: "Kāda ir dashboarda adrese pārlūkā, kad esi birojā? (Atver to un nokopē
   adresi no pārlūka.)" Ja uzstāda Edgars, viņš adresi zina. → `dashboard`. Adrese configā ir tikai
   atsauce (Claude to ieraksta darba mapes CLAUDE.md un piemin, kad vajag), skilli ar
   dashboardu pagaidām nesazinās; nesoli citādi.
4. **Akcenti titros**: "Titri ir balti, kā EHR reelos līdz šim. Vai gribi, lai pirms katra video
   piedāvāju izcelt 2 līdz 4 vārdus zīmola krāsā? Vari mainīt jebkurā brīdī." → `captions.accents`
   true/false.

Darba mape: nejautā, noklusējums `~/EHR-saturs` → `darbaMape`. Ja cilvēks pats grib citu vietu,
der jebkura, TIKAI NE `~/Documents`, `~/Desktop`, `~/Downloads` (iCloud izlādē failus un lauž renderus).

`platforms`: atstāj šablona vērtību (instagram, tiktok, facebook, youtube).
`meta`: `packVersion` (no `$LIB/../.claude-plugin/plugin.json`, VIENMĒR pārraksta), `installedAt`
(šodiena), `installedBy` ("edgars" ja uzstāda Edgars, citādi "pats").

Ierakstīšana: `python3 "$LIB/read_config.py" --set <lauks> <vērtība>` katram laukam (vai uzraksti
visu failu no šablona vienā reizē ar Write, ja config vēl nav). Beigās
`python3 "$LIB/read_config.py" --check`. Atzīmē `meta.setup.intervija = true`.

## 3. posms: darba mape

1. Izveido `darbaMape` (noklusēti `~/EHR-saturs`), ja nav.
2. Iekopē `$LIB/../templates/darba-mape/` saturu tajā (CLAUDE.md, LASIMANI.md, .claude/settings.json);
   esošos failus nepārraksti.
3. CLAUDE.md aizvieto `{{VARDS}}`, `{{ZIMOLS_NAME}}` (zīmola pilnais vārds), `{{DASHBOARD}}`.
4. Pasaki: "No šī brīža Claude Code atver šo mapi (`~/EHR-saturs`). Katram video sava apakšmape,
   gatavie faili paliek te." Ja Claude Code šobrīd atvērts citā mapē, parādi, kā to pārslēgt
   (Claude Desktop → mapes izvēle), un turpini.

Atzīmē `meta.setup.mape = true`.

## 4. posms: pārbaude ar īstu video

1. Pagaidi, kamēr 1. posma fons ir beidzies (ja vēl nav, pasaki, cik aptuveni palicis, un pagaidi).
2. Palūdz vienu īsu vertikālu video ar runu (jebkurš viņu reels, 15 līdz 60 s). Ja tāda nav pie
   rokas, izlaid pārbaudi, atzīmē `meta.setup.parbaude = "izlaista"` un pasaki, ka pirmajā īstajā
   reizē modelis vēl var lejupielādēties.
3. Palaid `auto-captions` skillu uz tā (pilnā plūsma: tabula → labojumi → renderis) un parādi kadrus.
4. Palaid `auto-apraksts` skillu uz tā paša transkripta vienam zīmolam, parādi Instagram variantu.
5. Ja abi izdevās: atzīmē `meta.setup.parbaude = true`.

## Noslēgums

Viens ekrāns cilvēkam (bez tehniskiem ceļiem):

> Gatavs. Trīs frāzes, kas tev jāzina:
> - "uzliec titrus" + video fails
> - "uzraksti aprakstu" + video vai teksts (un pasaki zīmolu, ja tas nav tavs galvenais)
> - "uzstādi", ja kaut kas nestrādā
>
> Atjauninājumi reizi nedēļā: `/plugin marketplace update ehr-paka`, tad `/reload-plugins`.
> Ja kaut kas neiet: edgars@creators.lv

Ja uzstāda Edgars: pēc noslēguma īsi pieraksti viņam, kas šajā datorā ir īpašs (Intel, cita
darba mape, cits dashboards), lai to ieliek klienta kartītē.
