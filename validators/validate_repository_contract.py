#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_TOP_LEVEL = [
    "schema_version",
    "repository",
    "standard",
    "paths",
    "commands",
    "issues",
    "agents",
    "alignment",
    "exemptions",
]

REQUIRED_SECTIONS = {
    "repository": ["id", "name", "archetype", "lifecycle", "visibility"],
    "standard": ["profile", "version", "automatic_checks"],
    "issues": ["provider", "schema", "sync_on_open", "stale_after_minutes"],
    "agents": ["enabled"],
    "alignment": ["target_score", "blocking_score"],
}


def fail(message: str) -> None:
    print(f"REPOSITORY CONTRACT VALIDATION FAIL: {message}")
    raise SystemExit(1)


def load_contract_text(root: Path) -> str:
    path = root / ".igmc" / "repository.yml"
    if not path.exists():
        fail(f"Missing required file: {path}")
    return path.read_text(encoding="utf-8")


def section_body(text: str, section: str) -> str:
    pattern = re.compile(rf"^{re.escape(section)}:\s*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return ""
    start = match.end()
    next_section = re.search(r"^[A-Za-z_][A-Za-z0-9_-]*:\s*", text[start:], re.MULTILINE)
    end = start + next_section.start() if next_section else len(text)
    return text[start:end]


def has_key(text: str, key: str, *, indented: bool = False) -> bool:
    prefix = r"\s+" if indented else ""
    return re.search(rf"^{prefix}{re.escape(key)}:\s*", text, re.MULTILINE) is not None


def validate_contract(root: Path) -> None:
    text = load_contract_text(root)
    for key in REQUIRED_TOP_LEVEL:
        if not has_key(text, key):
            fail(f"repository.yml missing top-level key: {key}")

    for section, keys in REQUIRED_SECTIONS.items():
        body = section_body(text, section)
        if not body:
            fail(f"repository.yml missing section body: {section}")
        for key in keys:
            if not has_key(body, key, indented=True):
                fail(f"repository.yml section '{section}' missing key: {key}")

    if re.search(r"token|secret|password|api[_-]?key", text, re.IGNORECASE):
        fail("repository.yml appears to contain a secret-like key")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an IGMC repository contract.")
    parser.add_argument("--root", default=".", help="Repository root to validate")
    args = parser.parse_args()

    validate_contract(Path(args.root).resolve())
    print("Repository contract validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())