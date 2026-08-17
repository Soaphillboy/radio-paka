# Uzstādīšanas diena EHR birojā (Edgaram)

Mērķis: 3 līdz 4 Mac (Artūrs, Anete, Viorika, Ilze?) ar `ehr` paku, katrs ~15 min, no kuriem
~10 min fonā. Strādā paralēli: kamēr vienā datorā iet fons, nākamajā sāc.

## Pirms brauciena (vakarā pirms)

- [ ] GitHub: fine-grained PAT tikai repo `ehr-paka`, Contents: Read-only, 90 dienas
      (github.com → Settings → Developer settings → Fine-grained tokens). Ieraksti to
      `~/claude-os/projekti/ehr-paka/.token` (gitignored) un uzraksti piekļuves komandu:
      ```
      git config --global "url.https://x-access-token:<TOKENS>@github.com/Soaphillboy/ehr-paka.insteadOf" "https://github.com/Soaphillboy/ehr-paka"
      ```
- [ ] Pārbaudi, ka repo ir pushots un `main` satur jaunāko: `cd ~/claude-os/projekti/ehr-paka && git status && git log -1`
- [ ] Ja iespējams, iepriekšējā dienā aizsūti komandai vienu rindu, ko palaist Terminālī, lai
      lejupielādē lielos gabalus fonā (Homebrew + ffmpeg + node + python), tad uz vietas paliek
      tikai plugin + modelis:
      ```
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" && brew install ffmpeg node python@3.12
      ```
- [ ] Līdzi: `autocaptions ehr paraugs.mov` (parādīšanai) + KLIENTS.md izdruka vai PDF

## Pie katra datora (~15 min)

1. Claude Code atvērts. Ielīmē 3 rindas: piekļuves komanda, `/plugin marketplace add`,
   `/plugin install ehr@ehr-paka`.
2. "uzstādi". Fons sāk iet. Atbildi uz 4 jautājumiem kopā ar cilvēku (vārds, zīmols,
   dashboards `http://10.0.0.33:8080`, akcenti).
3. Pāriet pie nākamā datora. Atgriezies, kad fons beidzies.
4. Pārbaude ar viņu īstu video (auto-captions + auto-apraksts). Parādi kadrus.
5. Pieraksti, kas šajā datorā īpašs (Intel, cita mape) → klienta CRM kartītē.

## Gotchas

- Bez piekļuves komandas marketplace add prasīs GitHub login vai klusi failos.
- Pēc katra `marketplace update` vajag `/reload-plugins`.
- Ja "uzstādi" apstājas uz Homebrew: cilvēks pats ievada Mac paroli Terminālī, tad "uzstādi" vēlreiz.
- Intel Mac: apraksti jā, titri nē; pasaki uzreiz.
- Modeļa lejupielāde birojā ar lēnu internetu var aizņemt 10+ min uz datoru; tāpēc paralēli.

## Pēc dienas

- [ ] Nepabeigtos punktus klienta CRM kartītē ar termiņiem
- [ ] `~/.ehr/labojumi.md` no katra datora (ja jau ir) → zīmolu profilos pakā → jauna versija
- [ ] Gala rēķins 250 EUR pēc pieņemšanas (līgums: pēc darbu pieņemšanas)
