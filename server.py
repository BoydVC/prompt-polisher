#!/usr/bin/env python3
"""Stdlib server for Fleet Prompt Polisher on port 4270. Read-only."""
import http.server, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); PORT = int(os.environ.get("PORT", 4270))
class H(http.server.BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        b = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code); self.send_header("Content-Type", ctype); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        p = self.path.split("?")[0]
        if p in ("/", "/index.html"): return self._send(200, open(os.path.join(HERE, "web/index.html"), "rb").read(), "text/html; charset=utf-8")
        if p == "/api/data": return self._send(200, open(os.path.join(HERE, "data/polish.json"), "rb").read(), "application/json")
        if p == "/health": return self._send(200, json.dumps({"ok": True, "app": "prompt-polisher"}), "application/json")
        if p == "/summary.pdf" and os.path.exists(os.path.join(HERE, "dist/prompt-polisher-summary.pdf")):
            return self._send(200, open(os.path.join(HERE, "dist/prompt-polisher-summary.pdf"), "rb").read(), "application/pdf")
        self._send(404, "not found", "text/plain")
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(("0.0.0.0", PORT), H).serve_forever()
