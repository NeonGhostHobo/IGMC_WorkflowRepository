#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


REQUIRED_STANDARD_FILES = [
    "standard/VERSION",
    "standard/repository-operating-standard.md",
    "standard/schemas/repository.schema.json",
    "standard/schemas/migration-manifest.schema.json",
    "standard/schemas/alignment-rule.schema.json",
    "standard/schemas/issue.schema.json",
    "standard/schemas/managed-asset.schema.json",
    "standard/rules/quick.yml",
    "standard/policies/default-weights.yml",
    "standard/policies/critical-rules.yml",
    "standard/assets/managed-assets.yml",
]

FORBIDDEN_PATHS = [
    "workflow_scaffold/template",
]

REQUIRED_ARCHETYPES = [
    "generic-software",
    "rust-terminal-application",
    "unity-project",
    "web-application",
    "python-tool",
    "documentation-only",
    "javascript-library",
    "research-repository",
    "creative-prototype",
    "client-delivery",
]


def fail(message: str) -> None:
    print(f"STANDARD ASSET VALIDATION FAIL: {message}")
    raise SystemExit(1)


def require_file(root: Path, relative: str) -> Path:
    path = root / relative
    if not path.exists():
        fail(f"Missing required file: {relative}")
    return path


def validate_json_schemas(root: Path) -> None:
    for path in (root / "standard" / "schemas").glob("*.json"):
        with path.open(encoding="utf-8") as handle:
            json.load(handle)


def yamlish_value(text: str, key: str) -> str | None:
    match = re.search(rf"^\s*{re.escape(key)}:\s*\"?([^\"\n]+)\"?\s*$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def validate_archetypes(root: Path) -> None:
    archetype_dir = root / "standard" / "archetypes"
    for archetype in REQUIRED_ARCHETYPES:
        path = archetype_dir / f"{archetype}.yml"
        require_file(root, str(path.relative_to(root)))
        text = path.read_text(encoding="utf-8")
        declared = yamlish_value(text, "id")
        if declared != archetype:
            fail(f"Archetype {path} declares id {declared!r}, expected {archetype!r}")


def validate_managed_assets(root: Path) -> None:
    text = require_file(root, "standard/assets/managed-assets.yml").read_text(encoding="utf-8")
    assets = re.findall(
        r"^\s+source:\s*\"?([^\"\n]+)\"?\s*\n(?:^\s+[^\n]*\n)*?^\s+checksum:\s*\"?([^\"\n]+)\"?\s*$",
        text,
        re.MULTILINE,
    )
    if not assets:
        fail("Managed asset registry has no asset sources")
    for source, checksum in assets:
        source_path = root / source
        if not source_path.exists():
            fail(f"Managed asset source does not exist: {source}")
        if not checksum.startswith("sha256:"):
            fail(f"Managed asset source {source} has missing or non-sha256 checksum")
        actual = sha256_path(source_path)
        if actual != checksum:
            fail(f"Managed asset source {source} checksum mismatch: expected {checksum}, got {actual}")


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    if path.is_file():
        digest.update(path.read_bytes())
        return "sha256:" + digest.hexdigest()

    for child in sorted(p for p in path.rglob("*") if p.is_file()):
        relative = child.relative_to(path).as_posix().encode("utf-8")
        digest.update(relative)
        digest.update(b"\0")
        digest.update(child.read_bytes())
        digest.update(b"\0")
    return "sha256:" + digest.hexdigest()


def validate(root: Path) -> None:
    for relative in REQUIRED_STANDARD_FILES:
        require_file(root, relative)
    for relative in FORBIDDEN_PATHS:
        if (root / relative).exists():
            fail(f"Forbidden stale workflow path exists: {relative}")
    validate_json_schemas(root)
    validate_archetypes(root)
    validate_managed_assets(root)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate IGMC workflow-standard source assets.")
    parser.add_argument("--root", default=".", help="Workflow repository root")
    args = parser.parse_args()

    validate(Path(args.root).resolve())
    print("Standard asset validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())