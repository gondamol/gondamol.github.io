#!/usr/bin/env bash
set -euo pipefail

html_file="${1:-_site/index.html}"

if [[ ! -f "$html_file" ]]; then
  echo "Missing file: $html_file" >&2
  exit 1
fi

require() {
  local pattern="$1"
  if ! grep -q "$pattern" "$html_file"; then
    echo "Missing pattern: $pattern" >&2
    exit 1
  fi
}

require "editorial-hero"
require "editorial-hero__domains"
require "editorial-hero__stats"
require "new profile pic.jpeg"
require "chapter-band"
require "featured-ledger"
require "collab-channel"
