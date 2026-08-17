# Uzstādīšanas diena EHR birojā (Edgaram)

Mērķis: 3 līdz 4 Mac (Artūrs, Anete, Viorika, Ilze?) ar `ehr` paku, katrs ~15 min, no kuriem
~10 min fonā. Strādā paralēli: kamēr vienā datorā iet fons, nākamajā sāc.

## Pirms brauciena (vakarā pirms)

- [ ] Repo ir PUBLISKS (github.com/Soaphillboy/ehr-paka → Settings → Danger zone), tāpēc
      nekādi tokeni un GitHub konti klientiem nav vajadzīgi. Pārbaude no jebkura datora bez
      pieteikšanās: `git ls-remote https://github.com/Soaphillboy/ehr-paka` (rāda `main`).
- [ ] Pārbaudi, ka repo ir pushots un `main` satur jaunāko: `cd ~/claude-os/projekti/ehr-paka && git status && git log -1`
- [ ] Ja iespējams, iepriekšējā dienā aizsūti komandai vienu rindu, ko palaist Terminālī, lai
      lejupielādē lielos gabalus fonā (Homebrew + ffmpeg + node + python), tad uz vietas paliek
      tikai plugin + modelis:
      ```
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" && brew install ffmpeg node python@3.12
      ```
- [ ] Līdzi: `autocaptions ehr paraugs.mov` (parādīšanai) + KLIENTS.md izdruka vai PDF

## Pie katra datora (~15 min)

1. Claude Code atvērts. Ielīmē 2 rindas:
   `/plugin marketplace add https://github.com/Soaphillboy/ehr-paka` un `/plugin install ehr@ehr-paka`.
   (Pilnā HTTPS adrese, ne `Soaphillboy/ehr-paka` īsforma: īsforma klonē pa SSH un bez atslēgas failo.)
2. "uzstādi". Fons sāk iet. Atbildi uz 4 jautājumiem kopā ar cilvēku (vārds, zīmols,
   dashboarda adrese birojā, akcenti). Dashboarda adrese ir tava piezīmēs (klienta CRM
   kartīte), pakā tā apzināti nav ierakstīta.
3. Pāriet pie nākamā datora. Atgriezies, kad fons beidzies.
4. Pārbaude ar viņu īstu video (auto-captions + auto-apraksts). Parādi kadrus.
5. Pieraksti, kas šajā datorā īpašs (Intel, cita mape) → klienta CRM kartītē.

## Gotchas

- Ja marketplace add prasa GitHub login: pārbaudi, vai komandā ir pilnā https adrese un vai repo joprojām publisks.
- Pēc katra `marketplace update` vajag `/reload-plugins`.
- Ja "uzstādi" apstājas uz Homebrew: cilvēks pats ievada Mac paroli Terminālī, tad "uzstādi" vēlreiz.
- Intel Mac: apraksti jā, titri nē; pasaki uzreiz.
- Modeļa lejupielāde birojā ar lēnu internetu var aizņemt 10+ min uz datoru; tāpēc paralēli.

## Pēc dienas

- [ ] Nepabeigtos punktus klienta CRM kartītē ar termiņiem
- [ ] `~/.ehr/labojumi.md` no katra datora (ja jau ir) → zīmolu profilos pakā → jauna versija
- [ ] Gala rēķins 250 EUR pēc pieņemšanas (līgums: pēc darbu pieņemšanas)
