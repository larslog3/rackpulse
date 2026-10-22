FROM nginx:1.27-alpine

LABEL org.opencontainers.image.title="RackPulse — Homelab IPAM & Ansible Studio"
LABEL org.opencontainers.image.description="Track homelab IPs, hostnames, VLANs, distros & services and export Ansible inventories"
LABEL org.opencontainers.image.licenses="MIT"

COPY index.html /usr/share/nginx/html/index.html

RUN printf 'server {\n    listen 80;\n    server_name _;\n    root /usr/share/nginx/html;\n    index index.html;\n    gzip on;\n    gzip_types text/plain text/css application/json application/javascript;\n    location / {\n        try_files $uri $uri/ /index.html;\n    }\n}\n' > /etc/nginx/conf.d/default.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1:80/ > /dev/null || exit 1
