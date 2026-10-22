FROM python:3.12-alpine

LABEL org.opencontainers.image.title="RackPulse Homelab IPAM & Ansible Studio"
LABEL org.opencontainers.image.description="Self-hosted homelab IPAM and dynamic Ansible inventory generator"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app
COPY index.html /app/index.html
COPY server.py /app/server.py

VOLUME ["/data"]
ENV PORT=8080
ENV DATA_DIR=/data

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD wget -qO- http://127.0.0.1:${PORT}/api/health || exit 1

CMD ["python3", "/app/server.py"]
