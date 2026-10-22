#!/bin/sh
set -e
mkdir -p /var/lib/rackpulse
if command -v systemctl >/dev/null 2>&1; then
  systemctl daemon-reload || true
  systemctl enable --now rackpulse.service || true
fi
echo "RackPulse installed! Open http://localhost:8080 in your browser."
