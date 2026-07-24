# Operating Standard Implementation Tracker

This document tracks implementation of the IGMC Repository Operating Standard across the workflow repository and Command Deck.

## Blocks

1. **Workflow repository source of truth** — complete for MVP seed
   - Canonical standard copy: done
   - Schemas: done for repository, migration manifest, alignment rule, issue, and managed asset
   - Archetypes: done for first supported repository families
   - Rule and policy registries: seeded
   - Managed asset registry: seeded from existing agents, workflows, issue templates, validators, and contracts
   - Template/install layout

2. **Command Deck alignment engine** — complete for quick-scan MVP
   - Deterministic rule evaluation: done for quick scan
   - Score and grade calculation: done
   - Critical violation handling: done
   - Explainable evidence and remediation: done for quick scan

3. **Repository snapshot and open lifecycle** — complete for cache MVP
   - `.igmc/cache/repository-status.json`: done
   - Cached/fresh state distinction: surfaced in `/repo status`
   - issue freshness and scan freshness: recorded for issue refresh and quick scan snapshots

4. **Full `/repo ...` command surface** — complete for deterministic dry-run MVP
   - status, scan, align, adopt, migrate, diff-standard, explain, exemptions, repair
   - apply modes are blocked until manifest-backed operations land in Block 5

5. **Migration manifests and managed-file drift** — complete for manifest/drift MVP
   - deterministic manifests: done for adoption, repair, migration, and drift previews
   - base commit binding: seeded as `unknown` until Git commit capture is added to governance commands
   - managed asset checksums: registry supports checksum, current seed uses `null` and reports `UNKNOWN SOURCE`
   - drift states and safe remediation: drift states implemented; apply execution remains blocked pending safe executor

6. **Governance UI and later SDK/runtime events** — complete for governance/event MVP
   - repository/governance tab: done
   - alignment panels: surfaced through Governance tab summary
   - task/event views: governance event log MVP done
   - Copilot SDK event normalization after deterministic governance exists: event model is provider-neutral and ready for SDK provider integration later

## Block 1 Acceptance

- The workflow repository has a canonical copy of the Operating Standard.
- The standard directory contains schemas for repository contracts, migration manifests, alignment rules, issue objects, and managed assets.
- The standard directory contains archetypes for the first supported repository families.
- Existing prototype agents and workflows are retained and registered as managed assets.
- Validators can validate the repository contract seed without third-party dependencies.
- The root installer remains canonical, while legacy `workflow_scaffold/apply.py` remains compatible.

## Block 1 Validation

- `python validators/validate_standard_assets.py`
- `python validators/validate_repository_contract.py --root <installed-repo>`
- `python apply.py --dest <temp> --repo-id smoke --repo-name "Smoke" --archetype generic-software`

Latest evidence:

- Python compile check passed for root installer, compatibility installer, standard validators, and installed validators.
- `python validators/validate_standard_assets.py` passed.
- Temp install using `--archetype unity-project` passed.
- Installed `scripts/validate_repository_contract.py` passed.
- Installed `scripts/validate_artifacts.py` passed.

## Block 2 Validation

- `cargo test alignment`
- `cargo test repo_commands_parse_governance_routes`
- `cargo run -- --exec "/repo scan --quick"`
- `python scripts/check.py`

## Block 3 Validation

- `cargo test snapshot`
- `cargo run -- --exec "/repo scan --quick"`
- `cargo run -- --exec "/repo status"`
- `python scripts/check.py`

## Block 4 Validation

- `cargo test repo_commands_parse_governance_routes`
- `cargo run -- --exec "/repo align"`
- `cargo run -- --exec "/repo explain repository.contract.present"`
- `cargo run -- --exec "/repo adopt"`
- `cargo run -- --exec "/repo repair"`
- `cargo run -- --exec "/repo diff-standard"`
- `cargo run -- --exec "/repo exemptions"`
- `python scripts/check.py`

## Block 5 Validation

- `cargo test managed_assets`
- `cargo test migrations`
- `cargo run -- --exec "/repo diff-standard"`
- `cargo run -- --exec "/repo migrate"`
- `cargo run -- --exec "/repo adopt"`
- `cargo run -- --exec "/repo repair"`
- `python scripts/check.py`

## Block 6 Validation

- `cargo test events`
- `cargo test governance_events_record_manifest_previews`
- `cargo test tui::tests`
- `cargo run -- --exec "/repo adopt"`
- `cargo run -- --exec "/repo diff-standard"`
- `python scripts/check.py`

## Hardening Validation

- H1/H2: `cargo test alignment`
- H4: `cargo test managed_assets`; `python validators/validate_standard_assets.py`
- H5: `cargo test migrations`; `/repo adopt --write-manifest`; `/repo diff-standard --write-manifest`
- H6: `cargo test adoption`; `/repo adopt --apply` smoke on a temp repository; generated contract/artifacts validation
- H8: `cargo test tui::tests`
- H9: `cargo test events`; `cargo test governance_events_record_manifest_previews`
- H10: `python validators/validate_standard_assets.py`; scaffold smoke install through root `apply.py`
- H7: context-changing command smoke; `python scripts/check.py`
