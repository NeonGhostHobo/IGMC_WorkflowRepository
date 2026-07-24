#!/usr/bin/env python3

import argparse
from pathlib import Path


TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".yml",
    ".yaml",
    ".json",
    ".py",
}


def render_tokens(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def copy_tree(template_dir: Path, dest: Path, *, force: bool, values: dict[str, str]) -> None:
    for src in sorted(template_dir.rglob("*")):
        if src.is_dir():
            continue

        rel = src.relative_to(template_dir)
        dst = dest / rel
        dst.parent.mkdir(parents=True, exist_ok=True)

        if dst.exists() and not force:
            raise SystemExit(f"Refusing to overwrite existing file: {dst} (use --force)")

        if src.suffix.lower() in TEXT_SUFFIXES:
            dst.write_text(render_tokens(src.read_text(encoding="utf-8"), values), encoding="utf-8")
        else:
            dst.write_bytes(src.read_bytes())


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply the IGMC workflow repository template into a repository."
    )
    parser.add_argument(
        "--dest",
        default=".",
        help="Destination repo root (default: current directory)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files",
    )
    parser.add_argument(
        "--repo-id",
        default=None,
        help="Repository contract id (default: destination folder name)",
    )
    parser.add_argument(
        "--repo-name",
        default=None,
        help="Human-readable repository name (default: destination folder name)",
    )
    parser.add_argument(
        "--archetype",
        default="generic-software",
        help="Repository archetype for .igmc/repository.yml",
    )
    parser.add_argument(
        "--lifecycle",
        default="active",
        help="Repository lifecycle for .igmc/repository.yml",
    )
    parser.add_argument(
        "--visibility",
        default="private",
        help="Repository visibility for .igmc/repository.yml",
    )

    args = parser.parse_args()
    dest = Path(args.dest).resolve()
    template_dir = Path(__file__).resolve().parent / "template"
    if not template_dir.exists():
        raise SystemExit(f"Missing template dir: {template_dir}")

    values = {
        "REPOSITORY_ID": args.repo_id or dest.name,
        "REPOSITORY_NAME": args.repo_name or dest.name,
        "REPOSITORY_ARCHETYPE": args.archetype,
        "REPOSITORY_LIFECYCLE": args.lifecycle,
        "REPOSITORY_VISIBILITY": args.visibility,
        "IGMC_STANDARD_VERSION": "1.0.0",
    }

    copy_tree(template_dir, dest, force=args.force, values=values)

    print("IGMC workflow repository template applied")
    print(f"- Template: {template_dir}")
    print(f"- Dest: {dest}")
    print(f"- Contract: {values['REPOSITORY_ID']} ({values['REPOSITORY_ARCHETYPE']})")
    print("Next: push changes, then create an Issue titled 'IGMC: ...' and assign to Copilot.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
