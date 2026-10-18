import json, sys, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
PORT = int(sys.argv[1])
class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def j(self, v):
        b = json.dumps(v).encode(); self.send_response(200)
        self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        if self.path.startswith("/token"):
            return self.j({"token": "fake", "expires_at": int(time.time()) + 3600, "endpoints": {"api": f"http://127.0.0.1:{PORT}"}})
        return self.j({"data": [{"id": "gpt-4o", "name": "gpt-4o", "capabilities": {"type": "chat", "supports": {"tool_calls": True}}, "model_picker_enabled": True}]})
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
        msgs = body.get("messages", []); last = msgs[-1] if msgs else {}
        user = next((m.get("content") or "" for m in reversed(msgs) if m.get("role") == "user"), "")
        tools = [t["function"]["name"] for t in body.get("tools") or []]
        if last.get("role") == "tool":
            msg = {"role": "assistant", "content": "SAVED: " + str(last.get("content"))}
        elif user.startswith("Remember") and "ManageMemory" in tools:
            args = json.dumps({"memory_type": "preference", "content": "favorite coffee is a flat white", "importance": 4})
            msg = {"role": "assistant", "content": None, "tool_calls": [{"id": "c1", "type": "function", "function": {"name": "ManageMemory", "arguments": args}}]}
        else:
            sysText = " ".join(str(m.get("content")) for m in msgs if m.get("role") == "system")
            msg = {"role": "assistant", "content": "SYSTEM PROMPT HAS FLAT WHITE: " + str("flat white" in sysText)}
        self.j({"model": "gpt-4o", "choices": [{"index": 0, "message": msg, "finish_reason": "tool_calls" if msg.get("tool_calls") else "stop"}]})
ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
