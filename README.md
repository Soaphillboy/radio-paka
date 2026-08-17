# ehr-paka

Claude Code plugin marketplace European Hit Radio (EHR) komandas datoriem (publisks repo `Soaphillboy/radio-paka`, lokāli `projekti/ehr-paka`; publisks, lai
klientiem nevajag tokenus, nosaukums bez EHR, lai pēc vārda nav atrodams; pakā nav noslēpumu, tikai skilli, skripti un zīmolu profili no publiskiem postiem). Viens plugins
`ehr` ar trim skilliem, ar ko darbinieka Mac prot uzlikt EHR stila titrus un uzrakstīt video
aprakstus visiem pieciem zīmoliem. Papildina EHR Satura Sistēmas dashboardu (Docker konteineris
EHR serverī, adrese klienta CRM kartītē, ne šajā repo), ar to pagaidām nesazinās, tikai zina adresi.

Klientam: **KLIENTS.md** (2 komandas + "uzstādi"). Edgaram uzstādīšanas dienai: `docs/UZSTADISANAS-DIENA.md`.

## Struktūra

```
ehr-paka/
├── .claude-plugin/marketplace.json     ← marketplace "ehr-paka", plugins: ehr
├── KLIENTS.md                          ← klienta instrukcija
├── docs/UZSTADISANAS-DIENA.md          ← Edgara checklist
└── ehr/                                ← plugins
    ├── .claude-plugin/plugin.json      ← versija (celt pie katra izlaiduma)
    ├── skills/
    │   ├── uzstadi/                    ← 4 posmu vednis, config ~/.ehr/config.json
    │   ├── auto-captions/              ← EHR titri (2026-07 paraugs); captions/*.py + remotion-src/
    │   └── auto-apraksts/              ← apraksti IG/TT/FB/YT zīmola balsī
    ├── zimoli/                         ← zimoli.json (krāsas, valoda, handles) + <zimols>.md balss profili
    ├── lib/                            ← read_config.py, setup/setup_common.sh, setup/setup_captions.sh
    └── templates/                      ← config.example.json, darba-mape/ (CLAUDE.md, settings)
```

Darbinieka datorā viss stāvoklis dzīvo `~/.ehr/` (config.json, venv-captions, Whisper modelis
HF kešā, remotion-captions, work/, labojumi.md) un `~/EHR-saturs/` (darba mape). Plugin update
tos neaiztiek.

## Izlaidums

1. Labo skillus / zīmolu profilus, `ehr/.claude-plugin/plugin.json` versiju un CHANGELOG.
2. Lokāls tests: `claude plugin validate <pilns ceļš uz ehr-paka>` un `... /ehr` (absolūtie ceļi);
   pilnais: `claude plugin marketplace add <šī mape>` + `claude plugin install ehr@ehr-paka`,
   pēc tam uninstall + marketplace remove.
3. `git commit && git push`. Klienti: `/plugin marketplace update ehr-paka` + `/reload-plugins`.

## Piekļuve klientiem

Repo ir publisks: `/plugin marketplace add https://github.com/Soaphillboy/radio-paka` bez tokeniem
un bez GitHub konta (pilnā https adrese; `owner/repo` īsforma klonē pa SSH un bez atslēgas failo).
Šajā repo nekad neliec neko iekšēju: klienta adreses, paroles, e-pastus, nepubliskus datus.

## Vēl nav (apzināti)

- cover-foto EHR stilā (V1.1: pēc komandas paraugiem)
- dashboarda API (kartītes lasīšana/rakstīšana no skilliem)
- titru vizuālais redaktors (titri_app.py no satura-sistema-paka)
