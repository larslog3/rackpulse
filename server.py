#!/usr/bin/env python3
"""
RackPulse Homelab IPAM & Ansible Inventory Studio — Lightweight Server
Serves the web UI and provides optional server-side JSON persistence at /api/hosts.
Zero external dependencies required (uses Python 3 standard library).
"""
import argparse
import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

DEFAULT_PORT = int(os.environ.get("RACKPULSE_PORT", "8080"))
DEFAULT_BIND = os.environ.get("RACKPULSE_BIND", "0.0.0.0")
DATA_FILE = Path(os.environ.get("RACKPULSE_DATA_FILE", "/var/lib/rackpulse/hosts.json"))
WEB_ROOT = Path(__file__).resolve().parent


class RackPulseHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_ROOT), **kwargs)

    def do_GET(self):
        if self.path == "/api/health":
            self._send_json(200, {"status": "ok", "service": "rackpulse"})
            return
        if self.path == "/api/hosts":
            if DATA_FILE.exists():
                try:
                    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
                    self._send_json(200, data)
                    return
                except Exception as exc:
                    self._send_json(500, {"error": str(exc)})
                    return
            self._send_json(200, [])
            return
        return super().do_GET()

    def do_POST(self):
        if self.path == "/api/hosts":
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8")
            try:
                payload = json.loads(raw)
                DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
                DATA_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")
                self._send_json(200, {"saved": True, "count": len(payload) if isinstance(payload, list) else 1})
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


def main():
    parser = argparse.ArgumentParser(description="RackPulse Homelab IPAM Server")
    parser.add_argument("--bind", default=DEFAULT_BIND, help="Bind address (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Listen port (default: 8080)")
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.bind, args.port), RackPulseHandler)
    print(f"RackPulse listening on http://{args.bind}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
