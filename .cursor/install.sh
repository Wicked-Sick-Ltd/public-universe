#!/usr/bin/env bash
# Idempotent, non-interactive bootstrap for Cursor Cloud Agents.
# This repository is Python 3.11+ and the standard library only: no lockfile,
# no third-party packages, and no secrets. Safe to run more than once.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! command -v python3 >/dev/null 2>&1; then
  echo "error: python3 is not installed" >&2
  exit 1
fi

if ! python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)'; then
  echo "error: python3 must be 3.11 or newer (found $(python3 --version 2>&1))" >&2
  exit 1
fi

# `import venv` can succeed while ensurepip is missing (Debian/Ubuntu split
# that into python3-venv). Creating a virtualenv needs both.
if ! python3 -c 'import ensurepip' >/dev/null 2>&1; then
  if ! command -v sudo >/dev/null 2>&1 || ! command -v apt-get >/dev/null 2>&1; then
    echo "error: python3 venv support (ensurepip) is missing and apt-get is unavailable" >&2
    exit 1
  fi
  py_minor="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
  sudo DEBIAN_FRONTEND=noninteractive apt-get update
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y "python${py_minor}-venv" python3-venv
fi

if [[ ! -x .venv/bin/python ]] || ! .venv/bin/python -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)'; then
  rm -rf .venv
  python3 -m venv .venv
fi

# No requirements file and no dev-tool manifest. Do not pip-install anything.
.venv/bin/python -c 'import sys; print("python", sys.version.split()[0], "venv", sys.prefix)'
