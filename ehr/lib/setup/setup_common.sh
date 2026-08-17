#!/bin/bash
# EHR paka: kopīgās tehniskās pārbaudes (Mac ar Apple Silicon).
# Palaiž uzstadi skills vai ar roku: bash setup_common.sh
# Katrs solis vai nu izdodas, vai izdrukā cilvēkam saprotamu iemeslu un ko darīt.
set -e

echo "== EHR paka: kopīgā uzstādīšana =="
echo ""

# 1) Apple Silicon (mlx-whisper strādā tikai uz M-čipa)
if [ "$(uname -m)" != "arm64" ]; then
  echo "✗ Šim datoram nav Apple Silicon (M) čipa, titru transkripcija te nestrādās."
  echo "  Apraksti strādās arī bez tā. Uzraksti Edgaram (edgars@creators.lv), sarunāsim risinājumu."
  exit 1
fi
echo "✓ Apple Silicon"

# 2) Brīvā vieta (whisper modelis ~3 GB + Remotion ~0.5 GB)
FREE_GB=$(df -g "$HOME" | awk 'NR==2 {print $4}')
if [ "${FREE_GB:-0}" -lt 8 ]; then
  echo "✗ Par maz brīvās vietas diskā (${FREE_GB} GB). Vajag vismaz 8 GB."
  echo "  Atbrīvo vietu (piem., vecos video) un palaid vēlreiz."
  exit 1
fi
echo "✓ Brīvā vieta: ${FREE_GB} GB"

# 3) Homebrew (svaigā Macā pēc instalēšanas brew nav PATH, savelkam paši)
[ -x /opt/homebrew/bin/brew ] && eval "$(/opt/homebrew/bin/brew shellenv)"
if ! command -v brew >/dev/null 2>&1; then
  echo "✗ Trūkst Homebrew (Mac pakotņu pārvaldnieks). Uzinstalē ar šo komandu Terminālī"
  echo "  (prasīs Mac paroli, tas ir normāli), tad saki Claude 'uzstādi' vēlreiz:"
  echo ""
  echo '  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
  exit 1
fi
echo "✓ Homebrew"

# 4) ffmpeg
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "→ Instalē ffmpeg ..."
  brew install ffmpeg
fi
echo "✓ ffmpeg"

# 5) Node.js 18+ (vajag Remotion renderim)
NEED_NODE=1
if command -v node >/dev/null 2>&1; then
  MAJOR=$(node -v | sed 's/v\([0-9]*\).*/\1/')
  [ "${MAJOR:-0}" -ge 18 ] && NEED_NODE=0
fi
if [ "$NEED_NODE" = "1" ]; then
  echo "→ Instalē Node.js ..."
  brew install node
fi
echo "✓ Node.js $(node -v)"

# 6) Python 3.10+
PY=""
for c in python3.12 python3.11 python3.13 python3; do
  if command -v "$c" >/dev/null 2>&1; then
    if "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)' 2>/dev/null; then
      PY="$c"; break
    fi
  fi
done
if [ -z "$PY" ]; then
  echo "→ Instalē Python ..."
  brew install python@3.12
  PY=python3.12
fi
echo "✓ Python: $($PY --version)"

# 7) EHR mājas mape (venv, modelis, Remotion, config; pārdzīvo plugin update)
EHR_HOME="${EHR_HOME:-$HOME/.ehr}"
export EHR_HOME
mkdir -p "$EHR_HOME/work"
echo "$PY" > "$EHR_HOME/.python"
echo "✓ $EHR_HOME"

# 8) Claude Code iestatījums: ja fona atjauninājums kādreiz neizdodas (nav interneta), paturēt esošo kopiju
#    citādi klusi pārklonē paku. Sapludina ar esošo ~/.claude/settings.json.
"$PY" - <<'EOF' || echo "  (settings.json neizdevās papildināt; uzstadi skills to izdarīs pats)"
import json, os
p = os.path.expanduser("~/.claude/settings.json")
os.makedirs(os.path.dirname(p), exist_ok=True)
try:
    s = json.load(open(p))
except Exception:
    s = {}
env = s.setdefault("env", {})
if env.get("CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE") != "1":
    env["CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE"] = "1"
    json.dump(s, open(p, "w"), ensure_ascii=False, indent=2)
print("✓ Claude Code iestatījumi")
EOF

# 9) Chrome piezīme (renderim vajag pārlūku)
if [ ! -d "/Applications/Google Chrome.app" ]; then
  echo "! Nav Google Chrome. Renderis pirmajā reizē lejupielādēs savu pārlūku;"
  echo "  ja renderēšana neizdodas, uzinstalē Google Chrome un mēģini vēlreiz."
fi

echo ""
echo "== Kopīgā daļa gatava. Tālāk: setup_captions.sh =="
