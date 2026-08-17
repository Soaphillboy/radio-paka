#!/usr/bin/env python3
"""EHR pakas config lasītājs: vienīgā vieta, kas zina config un zīmolu tabulas formātu.

Lieto:  python3 read_config.py                    # izdrukā visu configu
        python3 read_config.py --get zimols        # viena vērtība (punktu ceļš: captions.captionY)
        python3 read_config.py --check             # validācija; exit 0 = ok, 1 = problēmas
        python3 read_config.py --zimols superhits  # zīmola ieraksts (name, color, language, profils)
        python3 read_config.py --zimoli            # visu zīmolu saraksts (key: name)
        python3 read_config.py --set vards "Anete" # ieraksta lauku (punktu ceļš, JSON vērtība vai teksts)

Config dzīvo ~/.ehr/config.json (raksta uzstadi skills). Mājas mapi maina env EHR_HOME.
Zīmolu tabula: <paka>/zimoli/zimoli.json (šī faila kaimiņš ../zimoli/).
"""
import json, os, sys

EHR_HOME = os.environ.get("EHR_HOME", os.path.expanduser("~/.ehr"))
CONFIG_PATH = os.path.join(EHR_HOME, "config.json")
PAKA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIMOLI_PATH = os.path.join(PAKA, "zimoli", "zimoli.json")

REQUIRED = ["vards", "dashboard", "zimols", "language", "darbaMape"]


def load():
    if not os.path.exists(CONFIG_PATH):
        sys.exit(f"✗ Nav config faila: {CONFIG_PATH}\n  Saki Claude: uzstādi")
    try:
        return json.load(open(CONFIG_PATH))
    except json.JSONDecodeError as e:
        sys.exit(f"✗ config.json nav derīgs JSON: {e}")


def zimoli():
    z = json.load(open(ZIMOLI_PATH))
    return {k: v for k, v in z.items() if not k.startswith("_")}


def get(cfg, dotted):
    cur = cfg
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            sys.exit(f"✗ Nav tāda lauka: {dotted}")
        cur = cur[part]
    return cur


def set_value(cfg, dotted, raw):
    try:
        val = json.loads(raw)
    except Exception:
        val = raw
    parts = dotted.split(".")
    cur = cfg
    for p in parts[:-1]:
        cur = cur.setdefault(p, {})
    cur[parts[-1]] = val
    os.makedirs(EHR_HOME, exist_ok=True)
    json.dump(cfg, open(CONFIG_PATH, "w"), ensure_ascii=False, indent=2)
    print(f"✓ {dotted} = {json.dumps(val, ensure_ascii=False)}")


def check(cfg):
    problems = []
    for k in REQUIRED:
        if not cfg.get(k):
            problems.append(f"trūkst lauka '{k}'")
    z = zimoli()
    if cfg.get("zimols") and cfg["zimols"] not in z:
        problems.append(f"zimols '{cfg.get('zimols')}' nav viens no: {', '.join(z)}")
    dm = os.path.expanduser(cfg.get("darbaMape", ""))
    if dm and not os.path.isdir(dm):
        problems.append(f"darba mape neeksistē: {dm}")
    if dm and "/Documents/" in dm + "/":
        problems.append("darba mape ir iCloud Documents iekšpusē: iCloud izlādē failus un lauž renderus")
    d = cfg.get("dashboard", "")
    if d and not d.startswith(("http://", "https://")):
        problems.append(f"dashboard adrese '{d}' nesākas ar http:// vai https://")
    if problems:
        print("✗ config problēmas:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("✓ config derīgs:", CONFIG_PATH)


def main():
    if "--zimoli" in sys.argv:
        for k, v in zimoli().items():
            print(f"{k}: {v['name']} ({v['color']}, {v['language']})")
        return
    if "--zimols" in sys.argv:
        key = sys.argv[sys.argv.index("--zimols") + 1]
        z = zimoli()
        if key not in z:
            sys.exit(f"✗ Nav tāda zīmola: {key}. Ir: {', '.join(z)}")
        print(json.dumps({"key": key, **z[key]}, ensure_ascii=False, indent=2))
        return
    cfg = load()
    if "--check" in sys.argv:
        check(cfg)
    elif "--get" in sys.argv:
        i = sys.argv.index("--get")
        val = get(cfg, sys.argv[i + 1])
        print(json.dumps(val, ensure_ascii=False) if isinstance(val, (dict, list)) else val)
    elif "--set" in sys.argv:
        i = sys.argv.index("--set")
        set_value(cfg, sys.argv[i + 1], sys.argv[i + 2])
    else:
        print(json.dumps(cfg, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
