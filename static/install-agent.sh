#!/usr/bin/env bash
#
# ebshield agent install script
# ------------------------------------
# Safe for `curl | bash` usage: exits on error, no globbing, no word-splitting
# Run as root (or with sudo) because we need to create system files.
#
set -euo pipefail
IFS=$'\n\t'

### ---- 0. CONFIGURABLES ----------------------------------------------------
AGENT_VERSION=${AGENT_VERSION:-"v1.4.2"}          # override with env if you pin
DOWNLOAD_BASE="https://download.ebshield.io/agent"
BINARY_NAME="ebshield-agent"                       # matches systemd unit
INSTALL_DIR="/usr/local/bin"
DATA_DIR="/var/lib/ebshield"
CONF_DIR="/etc/ebshield"
TOKEN_FILE="${CONF_DIR}/enroll_token"              # 0600 root:root
UNIT_FILE="/etc/systemd/system/${BINARY_NAME}.service"

### ---- 1. PRE-FLIGHT -------------------------------------------------------
if [[ $EUID -ne 0 ]]; then
  echo "❌  Must run as root (use sudo)" >&2; exit 1; fi

if [[ -z "${ESHIELD_ENROLL_TOKEN:-}" ]]; then
  echo "❌  Set ESHIELD_ENROLL_TOKEN env var before running." >&2; exit 1; fi

arch=$(uname -m)
case "$arch" in
  x86_64)      arch="amd64"  ;;
  aarch64|arm64) arch="arm64" ;;
  *) echo "❌  Unsupported architecture: $arch" >&2; exit 1 ;;
esac

### ---- 2. DOWNLOAD & VERIFY ------------------------------------------------
tmp=$(mktemp -d)
tgz="${BINARY_NAME}_${AGENT_VERSION}_linux_${arch}.tar.gz"
url="${DOWNLOAD_BASE}/${AGENT_VERSION}/${tgz}"
sha_url="${url}.sha256"

echo "⬇️  Downloading $tgz …"
curl -fsSL "$url"     -o "${tmp}/${tgz}"
curl -fsSL "$sha_url" -o "${tmp}/${tgz}.sha256"

pushd "$tmp" >/dev/null
sha256sum -c "${tgz}.sha256"
popd >/dev/null
echo "✅  SHA-256 verified"

### ---- 3. INSTALL BINARY ---------------------------------------------------
tar -xzf "${tmp}/${tgz}" -C "$tmp"                  # expects ./ebshield-agent
install -Dm755 "${tmp}/${BINARY_NAME}" "${INSTALL_DIR}/${BINARY_NAME}"
echo "📦  Installed to ${INSTALL_DIR}/${BINARY_NAME}"

### ---- 4. CONFIG & DATA DIRS ----------------------------------------------
install -d -m 0755 "$DATA_DIR"
install -d -m 0700 "$CONF_DIR"
printf '%s\n' "$ESHIELD_ENROLL_TOKEN" > "$TOKEN_FILE"
chmod 600 "$TOKEN_FILE"
echo "🔑  Enrollment token stored at ${TOKEN_FILE}"

### ---- 5. SYSTEMD UNIT -----------------------------------------------------
cat >"$UNIT_FILE" <<EOF
[Unit]
Description=eB-Shield Firewall Agent
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=${INSTALL_DIR}/${BINARY_NAME} --token-file ${TOKEN_FILE} --data-dir ${DATA_DIR}
Restart=on-failure
RestartSec=5
User=root
AmbientCapabilities=CAP_NET_ADMIN

[Install]
WantedBy=multi-user.target
EOF

echo "📝  systemd unit placed at ${UNIT_FILE}"

### ---- 6. START & ENABLE ---------------------------------------------------
systemctl daemon-reload
systemctl enable --now "${BINARY_NAME}.service"

echo "🚀  Agent started:"
systemctl --no-pager status "${BINARY_NAME}.service" | head -n 15

echo "🎉  eB-Shield agent ${AGENT_VERSION} is active."
