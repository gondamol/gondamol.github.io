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

reject() {
  local pattern="$1"
  if grep -q "$pattern" "$html_file"; then
    echo "Unexpected pattern: $pattern" >&2
    exit 1
  fi
}

require "editorial-hero"
require "editorial-hero__nameplate"
require "editorial-hero__stats"
require "editorial-hero__ticker-track"
require "new profile pic.jpeg"
require "expertise-story__grid"
require "lifecycle-atlas__grid"
require "lifecycle-atlas__hover"
require "portfolio-memory__grid"
require "portfolio-memory__media"
require "tools-trust__grid"
require "tools-trust__meter"
require "background-ledger__layout"
require "background-ledger__chips"
require "life-glimpse__grid"
require "collab-channel"
reject "editorial-hero__domains"
reject "domain-flow"
reject "service-suite"
