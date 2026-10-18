"""Local model: run your Brainstem with a model on your own computer, no internet needed for the thinking.

    python3 local_model.py                      uses qwen2.5:14b through Ollama
    python3 local_model.py --model qwen2.5:32b  any Ollama model that can call tools
    python3 local_model.py --offline            also blocks every outside connection, to prove nothing leaves

It starts a small bridge that speaks the same chat language as Copilot, then starts your unchanged Brainstem
pointed at that bridge instead of Copilot. Your Brainstem's files are not edited. Close this window to stop it;
run your normal install line to go back to Copilot.

Needs: Ollama (https://ollama.com) running, with the model pulled (ollama pull qwen2.5:14b).
"""
import argparse
import hashlib
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

OLLAMA = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")


def bridge(port, model):
    """Answers the three things the Brainstem asks Copilot for: a token, the model list, and chat."""

    class Bridge(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def send_json(self, value, code=200):
            body = json.dumps(value).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path.startswith("/token"):
                return self.send_json({"token": "local", "expires_at": int(time.time()) + 86400,
                                       "endpoints": {"api": f"http://127.0.0.1:{port}"}})
            if self.path.startswith("/models"):
                return self.send_json({"data": [{"id": model, "name": model, "model_picker_enabled": True,
                                                 "capabilities": {"type": "chat", "supports": {"tool_calls": True}}}]})
            self.send_json({"error": "not found"}, 404)

        def do_POST(self):
            if not self.path.startswith("/chat/completions"):
                return self.send_json({"error": "not found"}, 404)
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
            body["model"] = model
            body.pop("tool_choice", None)
            req = urllib.request.Request(f"{OLLAMA}/v1/chat/completions", json.dumps(body).encode(),
                                         {"Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=600) as r:
                    self.send_response(r.status)
                    self.send_header("Content-Type", r.headers.get("Content-Type", "application/json"))
                    self.end_headers()
                    while True:
                        chunk = r.read1(65536) if hasattr(r, "read1") else r.read(65536)
                        if not chunk:
                            break
                        self.wfile.write(chunk)
                        self.wfile.flush()
            except urllib.error.HTTPError as e:
                self.send_json({"error": e.read().decode(errors="replace")[:500]}, e.code)
            except OSError as e:
                self.send_json({"error": f"Ollama is not answering at {OLLAMA}: {e}"}, 502)

    server = ThreadingHTTPServer(("127.0.0.1", port), Bridge)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def main():
    ap = argparse.ArgumentParser(description="Run your Brainstem on a local model.")
    ap.add_argument("--model", default=os.environ.get("LOCAL_MODEL", "qwen2.5:14b"))
    ap.add_argument("--brainstem", default=os.path.expanduser("~/.brainstem/src/rapp_brainstem"),
                    help="your Brainstem's folder (the install line puts it here)")
    ap.add_argument("--port", type=int, default=int(os.environ.get("PORT", "7071")))
    ap.add_argument("--bridge-port", type=int, default=7099)
    ap.add_argument("--offline", action="store_true",
                    help="block every connection that is not to this computer, so nothing can leave")
    a = ap.parse_args()

    if a.offline:
        # Set before the first web request: Python keeps the proxy settings it sees first.
        # Every web request then goes through a proxy that does not exist, except to this computer and to Ollama.
        dead = "http://127.0.0.1:9"
        here = ",".join(["127.0.0.1", "localhost", urllib.parse.urlparse(OLLAMA).hostname or "127.0.0.1"])
        os.environ.update(HTTP_PROXY=dead, HTTPS_PROXY=dead, http_proxy=dead, https_proxy=dead,
                          NO_PROXY=here, no_proxy=here)
    kernel = os.path.abspath(a.brainstem)
    if not os.path.exists(os.path.join(kernel, "brainstem.py")):
        sys.exit(f"No Brainstem found in {kernel}. Run the install line first, or pass --brainstem <folder>.")
    try:
        names = [m["name"] for m in json.load(urllib.request.urlopen(f"{OLLAMA}/api/tags", timeout=5))["models"]]
    except OSError:
        sys.exit(f"Ollama is not running at {OLLAMA}. Start Ollama, then run this again.")
    if a.model not in names and a.model + ":latest" not in names:
        sys.exit(f"Ollama does not have {a.model} yet. Run: ollama pull {a.model}")

    bridge(a.bridge_port, a.model)
    source = open(os.path.join(kernel, "brainstem.py"), "rb").read()
    blob = hashlib.sha1(b"blob %d\0" % len(source) + source).hexdigest()[:7]
    os.environ.update(PORT=str(a.port), GITHUB_TOKEN="local")
    os.environ.setdefault("AGENTS_PATH", os.path.join(kernel, "agents"))
    sys.path.insert(0, kernel)
    os.chdir(kernel)
    import brainstem  # the unchanged Brainstem; only where it looks for a model changes, from outside

    brainstem.COPILOT_TOKEN_URL = f"http://127.0.0.1:{a.bridge_port}/token"
    brainstem.MODEL = a.model
    print(f"Brainstem (blob {blob}) thinking with {a.model} on this computer"
          f"{', outside connections blocked' if a.offline else ''}: http://127.0.0.1:{a.port}")
    brainstem.app.run(host="127.0.0.1", port=a.port, debug=False, threaded=True, use_reloader=False)


if __name__ == "__main__":
    main()
