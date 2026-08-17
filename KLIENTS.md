# EHR Satura Sistēma darbinieka datorā: uzstādīšana

TEV NEKAS NAV JĀPROGRAMMĒ. Tu runā, Claude dara.

## Kas vajadzīgs

- Mac ar Apple Silicon (M1 vai jaunāks); Intel Mac: apraksti strādās, titri ne
- Claude Desktop ar Claude Code (komandai jau ir)
- ~8 GB brīvas vietas (runas atpazīšanas modelis)
- Internets pirmajai uzstādīšanai (modelis ~3 GB)
- Apple Command Line Tools (pirmajā reizē Mac pats piedāvās logu ar pogu Install: spied Install,
  NE "Get Xcode"; logs mēdz paslēpties aiz citiem logiem; ~5 min)

## Uzstādīšana (3 komandas + 1 vārds, ~15 min, lielākā daļa fonā)

Piekļuves komandu (1. rinda) iedod Edgars: vai nu izdarāt kopā uzstādīšanas dienā, vai
saņem e-pastā. Atver Claude Code un ieraksti pa vienai:

```
<piekļuves komanda no Edgara>
```
```
/plugin marketplace add https://github.com/Soaphillboy/ehr-paka
```
```
/plugin install ehr@ehr-paka
```

Tad vienkārši uzraksti čatā:

```
uzstādi
```

Claude visu izskaidros un izdarīs pats: tehnisko daļu fonā, pa to laiku 4 īsi jautājumi
(vārds, galvenais zīmols, dashboarda adrese, vai titros vajag krāsainos akcentus), tad
pārbaude ar vienu īstu video. Vari apstāties jebkurā brīdī: nākamreiz atkal uzraksti
"uzstādi", un tas turpinās no vietas, kur paliki.

## Ikdienā (3 frāzes)

| Saki | Kas notiek |
|---|---|
| "uzliec titrus" + video fails | EHR stila titri, gatavs `<nosaukums>-titri.mp4` blakus video |
| "uzraksti aprakstu" + video vai teksts | apraksti Instagram, TikTok, Facebook, YouTube zīmola balsī |
| "uzstādi" | pārbauda un salabo sistēmu |

Zīmolu pasaki, ja tas nav tavs galvenais: "tas ir Super Hits video", "EHR+ saturs" (tad
titru krāsa, valoda un apraksta balss pārslēdzas). Darba mape `~/EHR-saturs`, katram video
sava apakšmape, gatavie faili paliek tur.

## Atjauninājumi

Reizi nedēļā ieraksti `/plugin marketplace update ehr-paka`, tad `/reload-plugins`, un dabūsi
jaunākos uzlabojumus (arī zīmolu balss labojumus). Tavi faili un iestatījumi paliek neaiztikti.

## Ja kaut kas neiet

Raksti edgars@creators.lv vai WhatsApp. Dashboards: http://10.0.0.33:8080 (biroja tīkls / VPN).
