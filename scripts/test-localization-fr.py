#!/usr/bin/env python3
"""Check the French corpus against its pinned English Git revision.

Run from any directory: python3 scripts/test-localization-fr.py
Requires PyYAML, as does test-convert-outputs.sh. No network or model required.
"""
from collections import Counter
from pathlib import Path
import json
import re
import subprocess
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "scripts/i18n/fr-source.json").read_text(encoding="utf-8"))
NAMES = json.loads((ROOT / "scripts/i18n/agent-names-fr.json").read_text(encoding="utf-8"))
DIVISIONS = json.loads((ROOT / "divisions.json").read_text(encoding="utf-8"))["divisions"]


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args]).decode("utf-8")


def split_document(text):
    parts = text.split("\n---", 1)
    assert text.startswith("---\n") and len(parts) == 2, "missing frontmatter"
    return yaml.safe_load(parts[0][4:]), parts[1].lstrip("\n")


def fences(body):
    result = []
    current = None
    for line in body.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if match:
            if current is None:
                current = (match[1][0], match[2].strip(), [])
            elif match[1][0] == current[0]:
                result.append((current[1], "\n".join(current[2])))
                current = None
        elif current is not None:
            current[2].append(line)
    if current is not None:
        result.append((current[1], "\n".join(current[2])))
    return result


def structure(body):
    # All source rows must remain in order, including blank rows, tables and lists.
    result = []
    for line in body.splitlines():
        match = re.match(r"^(\s*)(#{1,6}\s+|[-*+]\s+|\d+[.)]\s+|>|`{3,}|~{3,}|\|)", line)
        result.append(match[0] if match else ("blank" if not line.strip() else "text"))
    return result


def check_agent(path):
    source = git("show", f"{CONFIG['source_commit']}:{path}")
    data = (ROOT / path).read_bytes()
    assert b"\r" not in data and not data.startswith(b"\xef\xbb\xbf"), "expected UTF-8 without BOM, with LF"
    translated = data.decode("utf-8")
    before, old_body = split_document(source)
    after, body = split_document(translated)
    assert before["name"] in NAMES, "missing French display name"
    for field in before.keys() | after.keys():
        if field not in ("description", "vibe"):
            assert before.get(field) == after.get(field), f"technical metadata changed: {field}"
    assert after["description"] != before["description"], "description still in English"
    assert body.startswith("## Langue de travail\n\nRépondez en français par défaut"), "missing French default"
    body = re.sub(r"^## Langue de travail\n\n[^\n]+\n+", "", body, count=1)
    assert structure(old_body) == structure(body), "Markdown row structure changed"
    old_blocks, new_blocks = fences(old_body), fences(body)
    assert len(old_blocks) == len(new_blocks), "fenced block count changed"
    for index, ((lang, old), (new_lang, new)) in enumerate(zip(old_blocks, new_blocks), 1):
        assert lang == new_lang, f"fence language changed in block {index}"
        if lang.lower() not in ("", "md", "markdown", "text", "plaintext"):
            assert old == new, f"executable code changed in block {index} ({lang})"
    assert re.findall(r"`[^`\n]+`", old_body) == re.findall(r"`[^`\n]+`", body), "inline code changed"
    links = r"https?://[^\s<>\])]+"
    assert re.findall(links, old_body) == re.findall(links, body), "URLs changed"
    assert Counter(re.findall(r"\d+", old_body)) == Counter(re.findall(r"\d+", body)), "numeric values changed"
    foreign = r"[\u0370-\u03ff\u3040-\u30ff\u4e00-\u9fff\uac00-\ud7af]+"
    assert Counter(re.findall(foreign, old_body)) == Counter(re.findall(foreign, body)), "foreign examples or mathematical symbols changed"
    assert "987650" not in body, "unresolved translation token"
    assert "\ufffd" not in body and "\u2047" not in body, "unresolved translation character"


def main():
    paths = [p for p in git("ls-tree", "-r", "--name-only", CONFIG["source_commit"]).splitlines()
             if p.split("/")[0] in DIVISIONS and p.endswith(".md")]
    current = {p.relative_to(ROOT).as_posix() for d in DIVISIONS for p in (ROOT / d).rglob("*.md")}
    assert set(paths) == current, "agent files were added, removed or renamed"
    assert len(paths) == CONFIG["agent_count"] == len(NAMES), "roster/glossary count mismatch"
    errors = []
    for path in paths:
        try:
            check_agent(path)
        except (AssertionError, ValueError, KeyError) as exc:
            errors.append(f"{path}: {exc}")
    for error in errors:
        print("FAIL:", error)
    print(f"French localization: {len(paths)} agents, {len(errors)} failures")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
