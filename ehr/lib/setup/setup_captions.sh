#!/bin/bash
# EHR paka: auto-captions vide (mlx-whisper venv + Whisper modelis + Remotion projekts).
# Viss dzīvo ~/.ehr/, lai plugin update to neaiztiek. Palaid pēc setup_common.sh.
# Atkārtota palaišana ir droša: pārsinhronizē Remotion avotus, node_modules neaiztiek.
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$SCRIPT_DIR/../../skills/auto-captions"
EHR_HOME="${EHR_HOME:-$HOME/.ehr}"
export EHR_HOME
[ -x /opt/homebrew/bin/brew ] && eval "$(/opt/homebrew/bin/brew shellenv)"
PY="$(cat "$EHR_HOME/.python" 2>/dev/null || echo python3)"

echo "== EHR paka: titru vides uzstādīšana =="

# 1) Python vide + mlx-whisper
VENV="$EHR_HOME/venv-captions"
if [ ! -x "$VENV/bin/python" ]; then
  echo "→ Veido Python vidi (venv) ..."
  "$PY" -m venv "$VENV"
fi
"$VENV/bin/pip" -q install --upgrade pip
echo "→ Instalē mlx-whisper ..."
"$VENV/bin/pip" -q install mlx-whisper
echo "✓ mlx-whisper"

# 2) Whisper modelis (~3 GB, lejupielādējas vienreiz)
MODEL="$("$VENV/bin/python" - <<'EOF' 2>/dev/null || echo mlx-community/whisper-large-v3-mlx
import json, os
p = os.path.join(os.environ.get("EHR_HOME", os.path.expanduser("~/.ehr")), "config.json")
try:
    print(json.load(open(p)).get("captions", {}).get("whisperModel") or "mlx-community/whisper-large-v3-mlx")
except Exception:
    print("mlx-community/whisper-large-v3-mlx")
EOF
)"
echo "→ Lejupielādē transkripcijas modeli $MODEL (~3 GB; ja jau ir, izlaidīs) ..."
"$VENV/bin/python" -c "from huggingface_hub import snapshot_download; snapshot_download('$MODEL'); print('✓ modelis vietā')" \
  || echo "  (modeli nesanāca lejupielādēt tagad; tas automātiski notiks pirmajā titrēšanas reizē)"

# 3) Remotion projekts: kopija no pakas uz mājas mapi + npm install.
RDEST="$EHR_HOME/remotion-captions"
mkdir -p "$RDEST"
rsync -a --exclude node_modules --exclude public "$SKILL_DIR/remotion-src/" "$RDEST/"
mkdir -p "$RDEST/public/captions"
echo "→ Instalē Remotion (npm, var aizņemt pāris minūtes) ..."
(cd "$RDEST" && npm install --no-fund --no-audit)
echo "✓ Remotion: $RDEST"

echo ""
echo "== Titru vide gatava. Pārbaude: Claude sarunā 'uzliec titrus' + video fails =="
