#!/usr/bin/env python3
"""Video vai WAV -> transkripts (mlx-whisper) -> rediģējama titru tabula. EHR paka.

Lieto (parastais python3 der: skripts pats pārslēdzas uz ~/.ehr/venv-captions):
    python3 make_captions.py "/ceļš/uz/video.mp4" [--lang=lv] [--zimols=ehr|superhits|latviesuhiti|ehrplus|retrofm]

Valoda: --lang, citādi zīmola noklusējums (EHR+ = ru), citādi config.json `language`.
Zīmols: --zimols, citādi config.json `zimols`. Zīmols nosaka akcenta krāsu renderī un
tiek pierakstīts blakus video (<nosaukums>.captions-meta.json), lai caption_render.py to zina.

Rezultāts blakus video:
    <nosaukums>.captions.md            rediģējamā tabula (teksts + atzīmes)
    <nosaukums>.captions-timing.json   vārdu laiki (nerediģēt ar roku)
    <nosaukums>.captions-meta.json     zīmols + valoda šim video

Starpfaili (wav, transkripts) krājas ~/.ehr/work/; tos drīkst dzēst.
Ja captions.md jau ir, skripts APSTĀJAS (lai nepazustu rediģētais teksts); --force pārraksta.
"""
import hashlib, json, os, re, subprocess, sys

EHR_HOME = os.environ.get("EHR_HOME", os.path.expanduser("~/.ehr"))
WORK = f"{EHR_HOME}/work"
VENV_PY = f"{EHR_HOME}/venv-captions/bin/python"
PAKA = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ZIMOLI_PATH = f"{PAKA}/zimoli/zimoli.json"

# mlx_whisper dzīvo venv; ja skripts palaists ar citu python, pārstartē sevi ar venv python
if os.path.exists(VENV_PY) and os.path.realpath(sys.executable) != os.path.realpath(VENV_PY):
    try:
        import mlx_whisper  # noqa: F401
    except ImportError:
        os.execv(VENV_PY, [VENV_PY, *sys.argv])


def load_json(path, default):
    try:
        return json.load(open(path))
    except Exception:
        return default


CONFIG = load_json(f"{EHR_HOME}/config.json", {})
ZIMOLI = {k: v for k, v in load_json(ZIMOLI_PATH, {}).items() if not k.startswith("_")}
CAP = CONFIG.get("captions", {})
MODEL = CAP.get("whisperModel") or "mlx-community/whisper-large-v3-mlx"

MAX_SMALL = 3          # vārdi rindā (normāli)
MAX_SMALL_SHORT = 4    # atļauts 4. vārds, ja rinda kopumā īsa (saikļi u.tml.)
SHORT_TOTAL = 16       # burtu kopsumma, līdz kurai atļauts 4. vārds
GAP_BREAK = 0.55       # pauze (s), pēc kuras sākas jauna rinda
TAIL = 1.1             # cik ilgi rinda paliek ekrānā pēc pēdējā vārda, ja seko klusums

# Rindas platuma aplēse: konstantēm jāsakrīt ar remotion-src/src/WordCaptions.tsx
# (FS 56, left 120, width 840 1080x1920 telpā). EHR stilā visi vārdi vienā izmērā.
CAP_WIDTH = 840
FS = 56
CHAR_K = 0.66          # Montserrat vidējais burta platums kā daļa no fontSize
WORD_GAP = 15


def est_w(text: str) -> float:
    return len(text) * CHAR_K * FS


def src_key(path: str) -> str:
    """Stabils darba failu vārds: nosaukums + ceļa hash (vienādi faili dažādās mapēs nesajūk)."""
    stem = re.sub(r"[^A-Za-z0-9_-]+", "-", os.path.splitext(os.path.basename(path))[0]).strip("-")[:40] or "video"
    return f"{stem}-{hashlib.md5(os.path.abspath(path).encode()).hexdigest()[:8]}"


def transcribe(src: str, lang: str) -> dict:
    """ffmpeg -> 16k mono WAV -> mlx-whisper ar vārdu laikiem. Transkriptu kešo work/ mapē."""
    os.makedirs(WORK, exist_ok=True)
    key = src_key(src)
    tr_path = f"{WORK}/{key}.{lang}.transcript.json"
    if os.path.exists(tr_path) and os.path.getmtime(tr_path) > os.path.getmtime(src):
        return json.load(open(tr_path))
    wav = f"{WORK}/{key}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ar", "16000", "-ac", "1", "-vn", wav, "-y"], check=True)
    try:
        import mlx_whisper
    except ImportError:
        sys.exit("✗ Trūkst mlx-whisper vides (~/.ehr/venv-captions). Saki Claude: uzstādi")
    print(f"Transkribē ({lang}) ... pirmajā reizē lejupielādējas modelis (~3 GB), tas ir normāli")
    r = mlx_whisper.transcribe(wav, path_or_hf_repo=MODEL, language=lang, word_timestamps=True)
    json.dump(r, open(tr_path, "w"), ensure_ascii=False)
    return r


def main(src: str, lang: str, zimols: str, force: bool):
    stem = os.path.splitext(src)[0]
    md_path = f"{stem}.captions.md"
    if os.path.exists(md_path) and not force:
        sys.exit(f"Jau ir {os.path.basename(md_path)} (rediģētais teksts). Renderē: caption_render.py, "
                 f"vai pārraksti no jauna ar --force.")

    tr = transcribe(src, lang)
    words = []
    for seg in tr["segments"]:
        for w in seg.get("words", []):
            text = w["word"].strip()
            if text:
                words.append({"t": round(w["start"], 3), "end": round(w["end"], 3), "text": text})
    if not words:
        sys.exit("Transkripts tukšs: failā nav sadzirdamas runas (mūzika bez vārdiem?).")

    # Grupēšana īsās rindās (renderis pats tās kārto pāros: ievada rinda + treknā rinda)
    groups, cur = [], []

    def flush():
        if cur:
            groups.append(list(cur))
            cur.clear()

    i = 0
    while i < len(words):
        w = words[i]
        cur_w = sum(est_w(words[j]["text"]) for j in cur) + WORD_GAP * len(cur)
        if cur and cur_w + est_w(w["text"]) > CAP_WIDTH:
            flush()
        cur.append(i)
        nxt = words[i + 1] if i + 1 < len(words) else None
        total = sum(len(words[j]["text"]) for j in cur)
        limit = MAX_SMALL_SHORT if total <= SHORT_TOTAL else MAX_SMALL
        brk = (
            len(cur) >= limit
            or w["text"][-1] in ".!?…"
            or (nxt and nxt["t"] - w["end"] > GAP_BREAK)
            or nxt is None
        )
        if brk:
            flush()
        i += 1
    flush()

    out = []
    for gi, grp in enumerate(groups):
        ph = [words[j] for j in grp]
        start = ph[0]["t"]
        nxt_start = words[groups[gi + 1][0]]["t"] if gi + 1 < len(groups) else None
        end = min(ph[-1]["end"] + TAIL, nxt_start) if nxt_start else ph[-1]["end"] + TAIL
        out.append({
            "start": round(start, 3),
            "end": round(end, 3),
            "words": [{"t": w["t"], "text": w["text"]} for w in ph],
        })

    json.dump(out, open(f"{stem}.captions-timing.json", "w"), ensure_ascii=False, indent=1)
    json.dump({"zimols": zimols, "language": lang, "model": MODEL},
              open(f"{stem}.captions-meta.json", "w"), ensure_ascii=False, indent=1)

    zname = ZIMOLI.get(zimols, {}).get("name", zimols)
    lines = [
        f"# Titri: {os.path.basename(src)}",
        "",
        f"> Zīmols: {zname} ({zimols}), valoda: {lang}. Rindas ekrānā rādās pāros: pirmā ievada",
        "> svarā, otrā treknā (to renderis kārto pats pēc paužu vietām). Atzīmes: ==vārds== = akcents",
        "> zīmola krāsā, ~~vārds~~ = IG gradients. Izdzēsta rinda = frāzi nerāda.",
        "> Frāzi var sadalīt vairākās rindās ar to pašu # (sākums ↳), katra parādās no sava",
        "> pirmā vārda laika. Vārdu skaitu frāzē drīkst mainīt (laiki izlīdzinās).",
        f'> Kad gatavs: python3 caption_render.py "{src}"',
        "",
        "| # | Sākums | Frāze |",
        "|---|---|---|",
    ]
    for i, p in enumerate(out, 1):
        mm, ss = divmod(int(p["start"]), 60)
        frac = int((p["start"] % 1) * 10)
        lines.append(f"| {i} | {mm}:{ss:02d}.{frac} | " + " ".join(w["text"] for w in p["words"]) + " |")

    open(md_path, "w").write("\n".join(lines) + "\n")
    print(f"OK: {len(out)} frāzes -> {md_path}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    argval = lambda k: next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith(k + "=")), None)
    zimols = argval("--zimols") or CONFIG.get("zimols") or "ehr"
    if zimols not in ZIMOLI and ZIMOLI:
        sys.exit(f"✗ Nav tāda zīmola: {zimols}. Ir: {', '.join(ZIMOLI)}")
    lang = argval("--lang") or ZIMOLI.get(zimols, {}).get("language") or CONFIG.get("language") or "lv"
    main(os.path.abspath(args[0]), lang, zimols, "--force" in sys.argv)
