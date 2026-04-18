#!/bin/bash
set -e

export PATH="/usr/local/bin:/usr/bin:/bin"

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_DIR"

/usr/bin/just sync
/usr/bin/just display-nasa
