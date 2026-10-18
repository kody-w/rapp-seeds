#!/usr/bin/env bash
# Brainstem, offline edition: the unchanged Brainstem plus the local-model add-on, in one line.
#   curl -fsSL https://kody-w.github.io/rapp-seeds/rar/offline-edition/install.sh | bash
# It installs into its own folder (~/.brainstem-offline) and runs on port 7081, so a normal Brainstem keeps working.
set -euo pipefail

HOME_DIR="${OFFLINE_HOME:-$HOME/.brainstem-offline}"
PORT="${PORT:-7081}"
MODEL="${LOCAL_MODEL:-qwen2.5:14b}"
OLLAMA_URL="${OLLAMA_URL:-http://127.0.0.1:11434}"
SEEDS="${SEEDS_URL:-https://kody-w.github.io/rapp-seeds}"
REPO="https://github.com/kody-w/rapp-installer.git"
COMMIT="0e43ee580e78c150b1c59002456822d2e779388e"
BLOB="3f7102ff508c813bb6494511fc32a421a633e418"

say() { printf '  %s\n' "$*"; }
need() { command -v "$1" >/dev/null 2>&1 || { say "This needs $1. Install it, then run this line again."; exit 1; }; }

echo ""
say "Brainstem, offline edition. Your AI, as files you own, thinking on this computer."
echo ""
need git; need curl
PY="$(command -v python3.12 || command -v python3.11 || command -v python3 || true)"
[ -n "$PY" ] || { say "This needs Python 3.9 or newer. Install it, then run this line again."; exit 1; }
"$PY" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' || { say "This needs Python 3.9 or newer."; exit 1; }

# 1. The unchanged Brainstem, pinned by commit, checked by fingerprint.
mkdir -p "$HOME_DIR"
if [ ! -d "$HOME_DIR/src/.git" ]; then
    say "Getting the Brainstem..."
    git init -q "$HOME_DIR/src"
    git -C "$HOME_DIR/src" remote add origin "$REPO"
fi
git -C "$HOME_DIR/src" fetch -q --depth 1 origin "$COMMIT"
git -C "$HOME_DIR/src" checkout -q --force FETCH_HEAD
GOT="$(git -C "$HOME_DIR/src" hash-object rapp_brainstem/brainstem.py)"
[ "$GOT" = "$BLOB" ] || { say "The Brainstem file does not match its fingerprint ($GOT). Stopping."; exit 1; }
say "Brainstem 0.6.16, unchanged (fingerprint ${BLOB:0:7})."

# 2. Its Python packages, in its own folder.
if [ ! -x "$HOME_DIR/venv/bin/python" ]; then "$PY" -m venv "$HOME_DIR/venv"; fi
"$HOME_DIR/venv/bin/python" -m pip install -q --upgrade pip >/dev/null 2>&1 || true
"$HOME_DIR/venv/bin/python" -m pip install -q -r "$HOME_DIR/src/rapp_brainstem/requirements.txt"

# 3. The add-ons.
mkdir -p "$HOME_DIR/addons"
curl -fsSL "$SEEDS/rar/local-model/local_model.py" -o "$HOME_DIR/addons/local_model.py"
say "Add-on: local model."

# 4. A model on this computer, through Ollama.
if ! curl -fsS -m 3 "$OLLAMA_URL/api/tags" >/dev/null 2>&1; then
    if command -v ollama >/dev/null 2>&1; then
        say "Starting Ollama..."
        (ollama serve >/dev/null 2>&1 &) ; sleep 3
    elif [ "$(uname)" = "Darwin" ] && command -v brew >/dev/null 2>&1; then
        say "Installing Ollama with Homebrew..."
        brew install -q ollama && (ollama serve >/dev/null 2>&1 &) ; sleep 3
    elif [ "$(uname)" = "Linux" ]; then
        say "Installing Ollama with its official installer..."
        curl -fsSL https://ollama.com/install.sh | sh
        (ollama serve >/dev/null 2>&1 &) ; sleep 3
    else
        say "Install Ollama from https://ollama.com, open it, then run this line again."; exit 1
    fi
fi
curl -fsS -m 5 "$OLLAMA_URL/api/tags" >/dev/null || { say "Ollama is not answering at $OLLAMA_URL. Open Ollama, then run this line again."; exit 1; }
if ! curl -fsS "$OLLAMA_URL/api/tags" | grep -q "\"$MODEL\""; then
    say "Downloading the model $MODEL once (several GB)..."
    curl -fsS "$OLLAMA_URL/api/pull" -d "{\"name\": \"$MODEL\"}" | tail -1
fi

# 5. One command to start it again later: brainstem-offline
mkdir -p "$HOME/.local/bin"
cat > "$HOME/.local/bin/brainstem-offline" <<LAUNCH
#!/usr/bin/env bash
exec "$HOME_DIR/venv/bin/python" "$HOME_DIR/addons/local_model.py" --brainstem "$HOME_DIR/src/rapp_brainstem" \\
    --model "\${LOCAL_MODEL:-$MODEL}" --port "\${PORT:-$PORT}" --offline "\$@"
LAUNCH
chmod +x "$HOME/.local/bin/brainstem-offline"

echo ""
say "Ready. Open http://127.0.0.1:$PORT  (start it again any time with: brainstem-offline)"
say "Its memory and agents are files in $HOME_DIR/src/rapp_brainstem. Nothing you say leaves this computer."
echo ""
[ "${NO_LAUNCH:-}" = "1" ] && exit 0
exec "$HOME/.local/bin/brainstem-offline"
