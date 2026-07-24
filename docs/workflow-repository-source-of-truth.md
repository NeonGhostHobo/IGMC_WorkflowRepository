# Workflow Repository Source Of Truth

This repository is the IGMC Workflow Repository: the canonical source for the repository operating standard, installable workflow template, validators, agents, workflows, and managed asset registry.

## Canonical Paths

- `standard/` contains the operating standard and machine-readable schemas, archetypes, rules, policies, and managed asset metadata.
- `template/` contains the installable repository scaffold.
- `validators/` contains deterministic validation tools for the workflow repository and installed repositories.
- `apply.py` is the canonical installer.

## Compatibility

`workflow_scaffold/apply.py` remains only as a compatibility wrapper. It delegates to root `apply.py`.

There must not be a second template under `workflow_scaffold/template/`. A second template tree creates drift and violates the source-of-truth model.

## Existing Assets

The existing IGMC agents, issue templates, and workflows are retained as managed assets. They should be tuned and versioned through `standard/assets/managed-assets.yml` rather than replaced wholesale.
