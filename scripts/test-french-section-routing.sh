#!/usr/bin/env bash
# Ensure localization keeps persona/rules in OpenClaw's SOUL.md.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$SCRIPT_DIR/lib.sh"

for heading in \
  '## 🧠 votre identité et votre mémoire' \
  '## 🚨 règles impératives à respecter' \
  '## 📚 apprentissage et mémoire' \
  '## 💬 votre style de communication' \
  '## langue de travail' \
  '## critical rules you must follow' \
  '## your identity & memory'; do
  is_persona_header "$heading" || {
    printf 'FAIL: persona heading routed to operations: %s\n' "$heading"; exit 1;
  }
done
for heading in \
  '## 🎯 votre mission principale' \
  '## 📋 vos livrables techniques' \
  '## vos indicateurs de réussite' \
  '## your core mission'; do
  if is_persona_header "$heading"; then
    printf 'FAIL: operational heading routed to persona: %s\n' "$heading"; exit 1;
  fi
done
echo 'PASS: French and English section routing'
