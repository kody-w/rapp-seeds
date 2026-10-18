"""Remember, restart, recall: the hour page's step 2 against the unchanged pinned grail."""
import json, shutil, subprocess, sys, time, urllib.request, os
from pathlib import Path
S = Path(sys.argv[1]); G = S / "grail/src/rapp_brainstem"; R = S / "rapp-1/conformance/grail"; W = S / "memproof/run"
shutil.rmtree(W, ignore_errors=True); W.mkdir(parents=True)
k = W / "kernel"
shutil.copytree(G, k, ignore=shutil.ignore_patterns("agents", ".brainstem_data", ".brainstem_model", ".copilot_*", ".env", ".git", ".venv", "__pycache__", "tests"))
(k / "agents").mkdir()
for a in ("basic_agent.py", "manage_memory_agent.py", "context_memory_agent.py"): shutil.copy2(G / "agents" / a, k / "agents" / a)
fake = subprocess.Popen([sys.executable, str(S / "memproof/memory_fake.py"), "18931"])
env = dict(os.environ, HOME=str(W / "home"), GITHUB_TOKEN="ghu_fake", GITHUB_MODEL="gpt-4o", GRAIL_MODEL="gpt-4o", VOICE_MODE="false")
(W / "home").mkdir()
def up():
    p = subprocess.Popen([sys.executable, str(R / "run_grail.py"), str(k), "18930", "18931"], env=env, stdout=open(W / "log.txt", "a"), stderr=subprocess.STDOUT)
    for _ in range(100):
        try: urllib.request.urlopen("http://127.0.0.1:18930/health", timeout=1); return p
        except Exception: time.sleep(0.2)
    sys.exit("kernel did not start: " + (W / "log.txt").read_text()[-2000:])
def chat(text):
    req = urllib.request.Request("http://127.0.0.1:18930/chat", json.dumps({"user_input": text, "conversation_history": []}).encode(), {"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=30)).get("response")
try:
    p = up(); print("before remember:", chat("What do you remember about me?"))
    print("day 1:", chat("Remember that my favorite coffee is a flat white."))
    p.terminate(); p.wait(5); print("kernel stopped (Terminal closed)")
    p = up(); print("day 2, fresh process, empty history:", chat("What do you remember about me?"))
    store = list((k / ".brainstem_data").rglob("*.json")); print("memory files in the folder:", [str(x.relative_to(k)) for x in store])
    p.terminate()
finally:
    fake.terminate()
