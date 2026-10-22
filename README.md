# RackPulse — Homelab IPAM & Ansible Inventory Studio

Track homelab static IPv4 addresses, hostnames, FQDNs, VLANs, distros, and service tags — and dynamically generate Ansible `inventory.ini`, `hosts.yml`, or `inventory.json` files based on your active filters.

## 1. Quick Start with Docker / Podman

```bash
# Run directly from GitHub Container Registry (once pushed)
docker run -d --name rackpulse -p 8080:80 --restart unless-stopped ghcr.io/<YOUR_GITHUB_USER>/rackpulse-ipam:latest

# Or build and run locally with Docker Compose
docker compose up -d --build
```

Then open `http://localhost:8080`.

## 2. Install as a Native Linux Package (Any Distro)

Every tagged release (`v1.0.0`, etc.) automatically builds `.deb`, `.rpm`, `.apk`, and Arch `.pkg.tar.zst` packages via GitHub Actions + nFPM:

- **Debian / Ubuntu / Proxmox VE (`.deb`)**:
  ```bash
  sudo apt install ./rackpulse-ipam_1.0.0_all.deb
  ```
- **Rocky / RHEL / Fedora / AlmaLinux (`.rpm`)**:
  ```bash
  sudo dnf install ./rackpulse-ipam-1.0.0.noarch.rpm
  ```
- **Alpine Linux (`.apk`)**:
  ```bash
  sudo apk add --allow-untrusted ./rackpulse-ipam_1.0.0_all.apk
  ```
- **Arch Linux (`.pkg.tar.zst`)**:
  ```bash
  sudo pacman -U ./rackpulse-ipam-1.0.0-1-any.pkg.tar.zst
  ```

The package installs `/usr/share/rackpulse/` and enables the `rackpulse.service` systemd unit on port `8080`.
