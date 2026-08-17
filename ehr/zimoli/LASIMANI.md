# Zīmolu mape

- `zimoli.json`: tabula ar 5 zīmoliem (nosaukums, akcenta krāsa, gradients, valoda, IG/TikTok handles,
  profila ceļš). To lasa `lib/read_config.py --zimoli|--zimols`, `auto-captions` (krāsa, valoda)
  un `auto-apraksts` (nosaukums, valoda).
- `<key>.md`: zīmola RAKSTĪTĀ balss profils (apraksti IG/TikTok/FB/YT). Būvēts no publiskajiem
  aprakstiem 2026-08; katrs apgalvojums ar citātu. Sadaļas: balss īsumā, skaitļi (garums, emoji,
  hashtagi, valoda), formāti un formulas (āķi, CTA), ko nedarīt, paraugu korpuss, komandas labojumi.

Kā profils aug: darbinieku labojumi krājas viņu Mac `~/.ehr/labojumi.md` (auto-apraksts tos raksta
ar datumu un zīmolu). Edgars tos sapludina šeit "Komandas labojumi" sadaļā, ceļ pakas versiju un pusho;
`/plugin marketplace update ehr-paka` atnes visiem.
