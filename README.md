# ehr-paka

Privāts Claude Code plugin marketplace European Hit Radio (EHR) komandas datoriem. Viens plugins
`ehr` ar trim skilliem, ar ko darbinieka Mac prot uzlikt EHR stila titrus un uzrakstīt video
aprakstus visiem pieciem zīmoliem. Papildina EHR Satura Sistēmas dashboardu (Docker konteineris
EHR serverī, `http://10.0.0.33:8080`), ar to pagaidām nesazinās, tikai zina adresi.

Klientam: **KLIENTS.md** (3 komandas + "uzstādi"). Edgaram uzstādīšanas dienai: `docs/UZSTADISANAS-DIENA.md`.

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

Fine-grained PAT (tikai šis repo, Contents read-only, 90 d) + git URL rewrite klienta Macā,
skat. `docs/UZSTADISANAS-DIENA.md`. Tokens šajā repo nekad nedzīvo (`.token` ir gitignored).

## Vēl nav (apzināti)

- cover-foto EHR stilā (V1.1: pēc komandas paraugiem)
- dashboarda API (kartītes lasīšana/rakstīšana no skilliem)
- titru vizuālais redaktors (titri_app.py no satura-sistema-paka)
