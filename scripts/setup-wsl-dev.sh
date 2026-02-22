#!/usr/bin/env bash

set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "Run as root: sudo bash scripts/setup-wsl-dev.sh"
  exit 1
fi

if ! command -v apt-get >/dev/null 2>&1; then
  echo "This script currently supports Debian/Ubuntu (apt-get)."
  exit 1
fi

echo "[1/6] Updating apt package index..."
apt-get update

echo "[2/6] Installing base development tooling..."
apt-get install -y \
  ca-certificates \
  curl \
  wget \
  git \
  unzip \
  xdg-utils \
  software-properties-common \
  build-essential

echo "[3/6] Installing Python + pip..."
apt-get install -y \
  python3 \
  python3-pip \
  python3-venv

echo "[4/6] Installing R..."
apt-get install -y \
  r-base \
  r-base-dev

echo "[5/6] Installing Node.js + npm..."
apt-get install -y \
  nodejs \
  npm

echo "[6/6] Installing Quarto..."
QUARTO_VERSION="${QUARTO_VERSION:-}"
if [[ -z "${QUARTO_VERSION}" ]]; then
  QUARTO_VERSION="$(curl -fsSL https://api.github.com/repos/quarto-dev/quarto-cli/releases/latest \
    | grep -oP '"tag_name":\s*"v\K[^"]+')"
fi

if [[ -z "${QUARTO_VERSION}" ]]; then
  echo "Could not resolve latest Quarto version."
  exit 1
fi

QUARTO_DEB="/tmp/quarto-${QUARTO_VERSION}-linux-amd64.deb"
wget -q -O "${QUARTO_DEB}" \
  "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.deb"

dpkg -i "${QUARTO_DEB}" || apt-get install -f -y

echo
echo "Tool versions:"
python3 --version || true
pip3 --version || true
R --version | head -n 1 || true
node --version || true
npm --version || true
quarto --version || true

echo
echo "WSL development environment setup is complete."
