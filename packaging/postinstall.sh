#!/bin/sh
set -e
mkdir -p /var/lib/rackpulse
if command -v systemctl >/dev/null 2>&1; then
  systemctl daemon-reload || true
  systemctl enable rackpulse.service || true
  systemctl restart rackpulse.service || true
fi
