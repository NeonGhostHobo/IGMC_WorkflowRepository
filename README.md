# IGMC Workflow Repository

This repository is the **single source of truth** for the IGMC repository operating workflow. It is the workflow standard, installer, and template distribution source for all repositories managed by Command Deck.

It distributes the reusable pieces that make a repository compatible with:
- The IGMC Issue -> Copilot -> PR loop
- The PR + nightly **IGMC integrity gates**
- The CI failure -> PolishingAgent loop (with attempt cap)
- The agent spec stack under `.github/agents/`
- The IGMC Repository Operating Standard contract and alignment model

The repository was originally named for Unity development, but the workflow now applies to Unity and non-Unity repositories. Unity-specific expectations belong in the `unity-project` archetype rather than the generic scaffold. The intended repository name is `IGMC_WorkflowRepository`; until the remote is renamed, this working tree remains compatible with the old repository name.

## Apply to another repo

From this repo root:

- `python apply.py --dest /path/to/other-repo --repo-id my-repo --repo-name "My Repo" --archetype generic-software`

Options:
- Add `--force` to overwrite existing files.
- Use `--archetype rust-terminal-application`, `unity-project`, `web-application`, or `generic-software` to seed `.igmc/repository.yml`.

## What gets installed

Everything under `template/` is copied into the destination repo root, preserving paths:
- `.igmc/repository.yml`
- `.github/workflows/*`
- `.github/agents/*`
- `.github/copilot-instructions.md`
- `.github/ISSUE_TEMPLATE/igmc-intake.yml`
- `scripts/validate_artifacts.py`
- baseline `/docs/*` artifacts
- `tickets/` + `reports/` folders

The root `apply.py` is the canonical installer. `workflow_scaffold/apply.py` is only a compatibility wrapper for older automation and delegates to root `apply.py`. There must not be a second template tree under `workflow_scaffold/template/`.

## Source-of-truth layout

- `standard/` contains schemas, archetypes, rules, policies, managed assets, and the human-readable operating standard.
- `template/` contains installable repository files.
- `validators/` contains deterministic validators for this workflow repository and installed repositories.
- `apply.py` is the only installer implementation.

## Notes

- The PR gate enforces that any non-doc changes also update required `/docs/*`, add/update at least one `tickets/*.md`, and add/update `review.md`.
- Archetype-specific validation, such as Unity compilation, is declared by `.igmc/repository.yml` and archetype rules rather than hard-coded into the generic template.

## Validate the workflow standard

From this repo root:

- `python validators/validate_standard_assets.py`
- `python validators/validate_repository_contract.py --root /path/to/installed-repo`
