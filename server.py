#!/usr/bin/env python3
"""
RackPulse Homelab IPAM & Ansible Studio — Lightweight Self-Hosted HTTP Server
Provides static serving of index.html + optional REST persistence at /api/state
"""
import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PORT = int(os.environ.get("PORT", "8080"))
DATA_DIR = Path(os.environ.get("DATA_DIR", "./data"))
APP_DIR = Path(__file__).resolve().parent
STATE_FILE = DATA_DIR / "rackpulse_state.json"


class RackPulseHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(APP_DIR), **kwargs)

    def do_GET(self):
        if self.path == "/api/health":
            self._send_json(200, {"status": "ok", "service": "rackpulse-ipam"})
            return
        if self.path == "/api/state":
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            if STATE_FILE.exists():
                try:
                    data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
                    self._send_json(200, data)
                    return
                except Exception as exc:
                    self._send_json(500, {"error": str(exc)})
                    return
            self._send_json(200, {"hosts": None, "presets": None})
            return
        return super().do_GET()

    def do_POST(self):
        if self.path == "/api/state":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                raw = self.rfile.read(length).decode("utf-8")
                payload = json.loads(raw)
                DATA_DIR.mkdir(parents=True, exist_ok=True)
                STATE_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")
                self._send_json(200, {"saved": True, "path": str(STATE_FILE)})
            except Exception as exc:
                self._send_json(400, {"error": str(exc)})
            return
        self._send_json(404, {"error": "Not found"})

    def _send_json(self, status_code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(("0.0.0.0", PORT), RackPulseHandler)
    print(f"RackPulse IPAM listening on http://0.0.0.0:{PORT} (data dir: {DATA_DIR.resolve()})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
