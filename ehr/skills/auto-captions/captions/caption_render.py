#!/usr/bin/env python3
"""Titru tabula (captions.md) + laiki -> video ar titriem (Remotion WordCaptions renderis). EHR paka.

Lieto (parastais python3, venv nevajag):
    python3 caption_render.py "/ceļš/uz/video.mp4"
        noklusējums: burn-in <nosaukums>-titri.mp4 (1440x2560, gatavs publicēšanai)
    python3 caption_render.py "/ceļš/uz/video.mp4" --preview
        ātrs 1080x1920 melnraksts <nosaukums>-preview.mp4
    python3 caption_render.py "/ceļš/uz/fails.mp4|.wav|.mp3" --alpha [--dur=SEC] [--out=/ceļš]
        caurspīdīgs titru overlay bez fona video; audio ievadei (wav/mp3/m4a ...) ieslēdzas
        automātiski. Noklusējums: WebM VP9 + alpha (1080x1920), ko saprot CapCut; ar --prores
        dabū ProRes 4444 .mov (2160x3840) FCP/Premiere montāžai (CapCut ProRes caurspīdīgumu neatbalsta)

Papildus: --zimols=KEY  akcenta krāsa no zīmolu tabulas (citādi no <nosaukums>.captions-meta.json,
                        citādi config.json `zimols`)
          --y=NNNN      titru centra augstums 1080x1920 telpā (noklusēti config captions.captionY)
          --bg=/ceļš/kadrs.jpg  fona kadrs preview pozicionēšanai (kad nav fona video)

Priekšnosacījums: blakus failam ir <nosaukums>.captions.md un .captions-timing.json (no make_captions.py).
Ja mapē ir arī <nosaukums>.captions-title.json, tā title/titleBehind props aiziet uz komponenti.
"""
import hashlib, json, os, re, shutil, subprocess, sys

EHR_HOME = os.environ.get("EHR_HOME", os.path.expanduser("~/.ehr"))
WORK = f"{EHR_HOME}/work"
REMOTION = os.environ.get("REMOTION_DIR", f"{EHR_HOME}/remotion-captions")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PAKA = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ZIMOLI_PATH = f"{PAKA}/zimoli/zimoli.json"


def load_json(path, default):
    try:
        return json.load(open(path))
    except Exception:
        return default


CONFIG = load_json(f"{EHR_HOME}/config.json", {})
ZIMOLI = {k: v for k, v in load_json(ZIMOLI_PATH, {}).items() if not k.startswith("_")}
CAP = CONFIG.get("captions", {})


def src_key(path: str) -> str:
    """Tas pats darba failu vārds kā make_captions.py."""
    stem = re.sub(r"[^A-Za-z0-9_-]+", "-", os.path.splitext(os.path.basename(path))[0]).strip("-")[:40] or "video"
    return f"{stem}-{hashlib.md5(os.path.abspath(path).encode()).hexdigest()[:8]}"


def has_video(path: str) -> bool:
    try:
        out = subprocess.check_output(
            ["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries",
             "stream=codec_type", "-of", "csv=p=0", path])
        return b"video" in out
    except Exception:
        return not path.lower().endswith((".wav", ".mp3", ".m4a", ".aac", ".flac"))


def parse_md(md_path: str):
    """No captions.md tabulas: rindas -> [(idx, [(vārds, big, accent, ig)])]."""
    rows = []
    for ln in open(md_path):
        m = re.match(r"\|\s*(\d+)\s*\|[^|]*\|(.*)\|", ln)
        if not m:
            continue
        idx = int(m.group(1))
        words = []
        for tok in m.group(2).strip().split():
            big = tok.startswith("**") and tok.endswith("**") and len(tok) > 4
            accent = tok.startswith("==") and tok.endswith("==") and len(tok) > 4
            ig = tok.startswith("~~") and tok.endswith("~~") and len(tok) > 4
            words.append((tok.strip("*=~"), big, accent, ig))
        rows.append((idx, words))
    return rows


def build_phrases(rows, timing):
    """Rindas + laiku json -> Remotion frāzes. Vairākas rindas ar to pašu # (↳) sadala
    frāzes laika logu: katra apakšrinda rādās no sava pirmā vārda laika."""
    grouped = {}
    for i, w in rows:
        grouped.setdefault(i, []).append(w)

    phrases = []
    for i, ph in enumerate(timing, 1):
        parts = [p for p in grouped.get(i, []) if p]
        if not parts:
            continue  # rinda izdzēsta -> frāzi nerāda
        edited = [w for part in parts for w in part]
        orig = ph["words"]
        if len(edited) == len(orig):
            times = [ow["t"] for ow in orig]
        else:  # vārdu skaits mainīts -> laikus izlīdzina frāzes logā
            t0, t1 = orig[0]["t"], orig[-1]["t"]
            n = max(1, len(edited) - 1)
            times = [round(t0 + (t1 - t0) * j / n, 3) for j in range(len(edited))]
        pos = 0
        for k, part in enumerate(parts):
            words = [{"t": times[pos + j], "text": text, "big": big, "accent": accent, "ig": ig}
                     for j, (text, big, accent, ig) in enumerate(part)]
            start = ph["start"] if k == 0 else times[pos]
            pos += len(part)
            end = ph["end"] if k == len(parts) - 1 else times[pos]
            phrases.append({"start": start, "end": end, "words": words})
    return phrases


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    argval = lambda k: next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith(k + "=")), None)

    if not os.path.isdir(f"{REMOTION}/node_modules"):
        sys.exit(f"✗ Trūkst renderēšanas vides ({REMOTION}). Saki Claude: uzstādi")

    src = os.path.abspath(args[0])
    stem = os.path.splitext(src)[0]
    md, tj = f"{stem}.captions.md", f"{stem}.captions-timing.json"
    if not (os.path.exists(md) and os.path.exists(tj)):
        sys.exit(f'Nav {os.path.basename(md)}. Vispirms: python3 make_captions.py "{src}"')
    phrases = build_phrases(parse_md(md), json.load(open(tj)))
    if not phrases:
        sys.exit("captions.md tabulā nav nevienas rindas, nav ko renderēt.")

    meta = load_json(f"{stem}.captions-meta.json", {})
    zimols = argval("--zimols") or meta.get("zimols") or CONFIG.get("zimols") or "ehr"
    accent = ZIMOLI.get(zimols, {}).get("color") or CAP.get("accentColor") or "#E4002B"

    alpha = "--alpha" in sys.argv or not has_video(src)
    preview = "--preview" in sys.argv

    key = src_key(src)
    os.makedirs(WORK, exist_ok=True)

    link = None
    if alpha:
        dur = float(argval("--dur") or (max(p["end"] for p in phrases) + 0.5))
        video_prop = ""
    else:
        dur = float(subprocess.check_output(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", src]).strip())
        # Smagi avoti (4K, ProRes) Remotion kadru ekstrakcijā mēdz noildzināties ->
        # pārkodē uz 1440x2560 H264 proxy (VideoToolbox); pēc rendera proxy izdzēš.
        os.makedirs(f"{REMOTION}/public/captions", exist_ok=True)
        link = f"{REMOTION}/public/captions/{key}-src.mp4"
        if not os.path.exists(link) or os.path.getmtime(link) < os.path.getmtime(src):
            subprocess.run(["ffmpeg", "-v", "error", "-i", src,
                            "-vf", "scale=1440:2560", "-c:v", "h264_videotoolbox", "-b:v", "16M",
                            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
                            link, "-y"], check=True)
        video_prop = f"captions/{key}-src.mp4"

    y = int(argval("--y") or CAP.get("captionY") or 1120)
    props = {"video": video_prop, "phrases": phrases, "captionY": y, "durationSec": dur, "accentColor": accent}
    tpath = f"{stem}.captions-title.json"
    if os.path.exists(tpath):
        props.update(json.load(open(tpath)))
    if argval("--bg"):
        bg = os.path.abspath(argval("--bg"))
        os.makedirs(f"{REMOTION}/public/captions", exist_ok=True)
        bg_dst = f"{REMOTION}/public/captions/{key}-bg{os.path.splitext(bg)[1]}"
        shutil.copyfile(bg, bg_dst)
        props["bgStill"] = f"captions/{os.path.basename(bg_dst)}"
    props_path = f"{WORK}/{key}-props.json"
    json.dump(props, open(props_path, "w"), ensure_ascii=False)

    if preview:
        out = argval("--out") or f"{stem}-preview.mp4"
        codec = ["--codec=h264", "--crf=23", "--scale=1"]
    elif alpha and "--prores" in sys.argv:
        out = argval("--out") or f"{stem}-titri-alpha.mov"
        codec = ["--codec=prores", "--prores-profile=4444", "--pixel-format=yuva444p10le", "--scale=2"]
    elif alpha:
        out = argval("--out") or f"{stem}-titri-alpha.webm"
        codec = ["--codec=vp9", "--pixel-format=yuva420p", "--image-format=png", "--scale=1"]
    else:
        out = argval("--out") or f"{stem}-titri.mp4"
        codec = ["--codec=h264", "--crf=18", "--scale=1.33334"]

    port = 4000 + int(hashlib.md5(key.encode()).hexdigest(), 16) % 800
    cmd = ["npx", "remotion", "render", "WordCaptions", out,
           f"--props={props_path}", *codec,
           "--concurrency=1", "--timeout=120000", f"--port={port}"]
    if os.path.exists(CHROME):
        cmd.append(f"--browser-executable={CHROME}")
    print(f"▶ zīmols {zimols} ({accent}), y={y}")
    print("▶", " ".join(cmd))
    r = subprocess.run(cmd, cwd=REMOTION)
    if link and os.path.exists(link):
        os.remove(link)
    if r.returncode == 0:
        print("✅", out)
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
