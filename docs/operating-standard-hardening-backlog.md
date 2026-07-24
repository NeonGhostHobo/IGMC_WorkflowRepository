# Operating Standard Hardening Backlog

This backlog follows the six-block MVP implementation and realigns the next work with the IGMC Repository Operating Standard. It is intentionally review-first: do not treat these items as approved implementation until Ari validates the priorities and tradeoffs.

## Current Position

The MVP now has the basic spine:

- Workflow repository source-of-truth seed assets exist.
- Command Deck can read `.igmc/repository.yml`.
- Command Deck can run a deterministic quick alignment scan.
- Command Deck can write/read `.igmc/cache/repository-status.json`.
- The initial `/repo ...` command surface exists.
- Migration manifests and managed-asset drift exist as typed previews.
- The Governance tab and provider-neutral events exist as a UX surface.

The next phase should harden these features instead of adding broad new concepts.

## Important Existing Patterns To Preserve

These pre-standard patterns are useful and should be refined rather than replaced:

- Existing `.github/agents/*.agent.md` roles are already aligned with planner/reviewer/documentation/polishing/intake concepts. Keep them as first managed assets and tune naming/metadata later.
- Existing docs/tickets/reports workflow is valuable. Keep it, then map it into the documentation, issue, and reporting standards.
- Existing PR gate and CI failure loop are usable governance mechanisms. Extend them with contract/alignment checks instead of replacing them.
- Existing Command Deck catalog, issue tracker, and Copilot CLI adapter are good deterministic boundaries. Keep the CLI adapter as fallback even after SDK work begins.
- Existing TUI style helpers and wrapped panels are good enough for the Governance tab MVP. Improve usability incrementally rather than redesigning the shell.

## Deviations And Gaps Observed

These are not failures; they are explicit places where the MVP is still thinner than the standard.

1. Alignment scoring is currently flat rule-weight scoring.
   - Standard expects category-weighted scoring.
   - Needed: category scores, category weights, applicable-weight calculation, and category breakdown output.

2. Alignment rules are currently built into Rust.
   - Standard expects canonical rule registries in the workflow repository.
   - Needed: load rule registry or generate Rust-side rules from the workflow repo source.

3. Exemptions are loaded but not applied to rule results.
   - Standard requires exemptions remain visible and not silently convert failures to passes.
   - Needed: explicit `EXEMPT` handling and maximum-score/policy behavior.

4. Managed asset checksums are currently `null`.
   - Command Deck correctly reports present assets as `UNKNOWN SOURCE`.
   - Needed: checksum generation in workflow repo and checksum comparison in Command Deck.

5. Migration manifests are preview-only.
   - Standard requires deterministic, base-commit-bound, recorded manifests.
   - Needed: base commit capture, manifest serialization, `.igmc/migrations/` records, and rejection when repo changed incompatibly.

6. Manifest apply is blocked.
   - This is correct for safety, but incomplete.
   - Needed: safe operation executor for safe remediations only.

7. Repository-open lifecycle is partial.
   - We load cached snapshots and refresh issue data in some context changes.
   - Needed: consistent lifecycle on active repo changes: resolve root, contract, snapshot, Git, issues, workflow version, stale checks, summary.

8. Snapshot freshness is minimal.
   - Snapshot has timestamps, but no stale calculation yet.
   - Needed: compare timestamps to `issues.stale_after_minutes`, `alignment.quick_scan_interval_minutes`, and `alignment.full_scan_interval_hours`.

9. `/repo status` and Governance tab show useful data but need stronger cached/current distinction.
   - Standard explicitly requires cached data be visibly cached.
   - Needed: sharper labels, stale markers, and maybe separate Current vs Cached sections.

10. Governance events are MVP-level.
    - They have source/type/phase/timestamp/summary.
    - Needed: richer event data, task IDs, validation/tool/file event variants, and later Copilot SDK mapping.

11. The workflow repository still has two install paths.
    - Root `apply.py` is canonical, `workflow_scaffold/apply.py` delegates.
    - Needed: fully retire/regenerate partial `workflow_scaffold/template/` or remove it once dependent automation is updated.

12. Repository rename is still conceptual.
    - Standard says IGMC Workflow Repository.
    - Needed: decide official repo name and update GitHub/workflows/README references.

13. Issue schema is seeded but not enforced.
    - Existing GitHub forms are useful but not yet generated from canonical issue schema.
    - Needed: validate forms against schema and add issue object candidate pipeline later.

14. Security policy is not yet enforced.
    - Contract validator checks only simple secret-like keys.
    - Needed: stronger secret-key policy, instruction precedence checks, unknown-agent/tool restrictions, destructive-command blocks.

15. Full scan and semantic analysis are not implemented.
    - Correct to defer for now.
    - Needed after deterministic hardening: docs classification, stale-claim detection, design-to-issue extraction, duplicate detection.

## Hardening Backlog

### H1. Alignment Scoring Hardening - complete

Goal: Make quick alignment scoring match the Operating Standard more closely.

Scope:
- Add category scores.
- Load or mirror default category weights.
- Calculate total as `sum(category score * category weight)`.
- Show category breakdown in `/repo scan --quick`, `/repo status`, and Governance tab.
- Keep critical violations separate from numeric score.

Validation:
- Unit tests for category score math.
- Test that critical violation prevents `FULLY ALIGNED`.
- Smoke `/repo scan --quick` against Command Deck and an unmanaged repo.

Latest implementation:
- Quick scan now reports category scores.
- Total score is category-weighted across applicable quick-scan categories.
- Critical violations remain separate from numeric score.

### H2. Exemption Handling - complete

Goal: Implement visible, policy-correct exemptions.

Scope:
- Match contract exemptions to rule IDs.
- Mark exempted rules as `EXEMPT` instead of hiding them.
- Keep exemption reason visible in `/repo explain` and Governance tab.
- Add warning for expired or malformed exemptions.

Validation:
- Unit test: failed rule with exemption is visible as `EXEMPT`.
- Unit test: exemption without reason remains invalid or warned.

Latest implementation:
- Matching contract exemptions transform rule state to `EXEMPT` and keep the reason visible.
- Exempt rules are excluded from applicable category scoring instead of silently becoming passes.
- Malformed exemptions with empty reasons become `WARN` and remain visible.

### H3. Rule Registry Integration

Goal: Stop letting Command Deck and the workflow repo drift apart.

Scope:
- Decide whether Command Deck reads workflow repo YAML directly or uses generated Rust constants.
- Load quick rules from `standard/rules/quick.yml` where practical.
- Keep built-in fallback rules for bootstrap safety.
- Add version/source metadata to scan output.

Validation:
- Unit test registry loading.
- Smoke scan with missing workflow repo path falls back to built-ins.

### H4. Managed Asset Checksums - complete

Goal: Move from `UNKNOWN SOURCE` to meaningful drift states.

Scope:
- Generate checksums for workflow assets in the workflow repo.
- Store checksums in `standard/assets/managed-assets.yml` or generated sidecar manifest.
- Compare installed file checksums in Command Deck.
- Report `CURRENT`, `OUTDATED`, `LOCALLY MODIFIED`, `MISSING`, `UNKNOWN SOURCE`, and `CONFLICT` accurately.

Validation:
- Unit tests with temp files for current/outdated/missing.
- Workflow validator confirms asset source paths and checksums.

Latest implementation:
- Workflow repo can generate SHA-256 checksums for managed file and directory assets.
- Workflow validator verifies checksum presence and correctness.
- Command Deck compares installed managed assets against checksum constants.
- Present matching assets report `CURRENT`; present mismatching assets report `LOCALLY MODIFIED`; missing assets report `MISSING`; absent checksums still report `UNKNOWN SOURCE`.

### H5. Migration Manifest Persistence - complete for persistence MVP

Goal: Make manifests reviewable artifacts, not only terminal output.

Scope:
- Serialize manifest previews to `.igmc/generated/` or `.igmc/migrations/proposed/`.
- Include base commit from Git.
- Include operation states: generated/proposed/approved/completed/failed/skipped.
- Reject stale manifest when base commit differs.

Validation:
- Unit test manifest round-trip.
- Smoke `/repo adopt` writes proposal only when explicitly requested, or provide `/repo adopt --write-manifest` if we want a separate command.

Latest implementation:
- `/repo adopt --write-manifest`, `/repo repair --write-manifest`, `/repo migrate --write-manifest`, and `/repo diff-standard --write-manifest` can persist review JSON under `.igmc/generated/`.
- Manifests include the current Git HEAD as `base_commit` when available.
- Manifest previews remain dry-run by default; no command applies a manifest yet.
- Stale-manifest rejection is deferred to H6 because the safe executor is the first code path that will consume a stored manifest.

### H6. Safe Manifest Executor - complete for adoption MVP

Goal: Allow safe remediations without weakening safety policy.

Scope:
- Execute only safe operations at first:
  - create missing empty directory
  - regenerate ignored cache
  - create missing documentation index
  - update generated checksum records
- Keep review-required/destructive operations blocked.
- Require clean worktree or explicit policy for writes.
- Log every applied operation.

Validation:
- Tests for safe create-directory operation.
- Tests that destructive operations are rejected.
- Smoke `/repo repair --apply` on temp repo only.

Latest implementation:
- `/repo adopt --apply` runs the safe adoption executor.
- Adoption creates missing IGMC contract/cache/generated/migrations directories, validators, docs artifacts, PR template, agent/workflow/issue-template files, and review scaffolding without overwriting existing files.
- Adoption writes a migration record under `.igmc/migrations/` and can also write generated review JSON under `.igmc/generated/`.
- Repair apply remains blocked until rule-specific safe operations are implemented.

### H7. Repository-Open Lifecycle Hardening - complete for lifecycle MVP

Goal: Make repository context switches visibly reliable.

Scope:
- Centralize lifecycle into one method:
  1. resolve root
  2. read contract
  3. load snapshot
  4. inspect Git
  5. refresh/load issues
  6. compare workflow version
  7. determine stale scans
  8. render/update summary
- Call it on catalog load, `/use`, `/primary`, `/focus`, and clone/register flows where appropriate.
- Record governance events for each stage.

Validation:
- AppState tests around context switch.
- Governance tab shows cached state immediately.

Latest implementation:
- Context changes now run through one repository-open lifecycle method.
- Lifecycle loads cached snapshot, reads contract, inspects Git, refreshes issues, runs quick alignment, refreshes snapshot, and records governance events.
- The old primary-only issue refresh path has been replaced by the lifecycle path.

### H8. Governance UX Hardening - complete for panelized MVP

Goal: Make the Governance tab a reliable operator surface.

Scope:
- Separate Current State, Cached Snapshot, Alignment, Drift, and Events into clearer panels.
- Add explicit stale/current labels.
- Use severity colors for critical/fail/warn/pass/exempt.
- Ensure wrapped text and scrolling remain usable.
- Add concise empty states for unmanaged repositories.

Validation:
- TUI tests for helper formatting.
- Manual screenshot inspection later if/when we add visual testing.

Latest implementation:
- Governance tab now separates Current State, Cached Snapshot, Alignment + Drift, and Governance Events.
- Current/cached labels are explicit.
- Severity coloring highlights missing, failed, locally modified, warning, current, aligned, and completed states.
- Empty cached/alignment states have concise operator text.

### H9. Event Model Hardening - complete for event envelope MVP

Goal: Prepare for Copilot SDK without overbuilding now.

Scope:
- Add optional task/session IDs.
- Add typed event kinds or constants for required standard events.
- Add event data field for small structured payloads.
- Keep rendering human-readable summaries.
- Do not invent progress for unbounded agent work.

Validation:
- Unit tests for event construction and render lines.
- Governance tab shows recent events after repo commands.

Latest implementation:
- Governance events now include optional `session_id`, optional `task_id`, and structured string `data`.
- Event kind constants cover the current repository governance event types.
- Existing Governance tab lines keep human-readable summaries while showing context and compact data payloads.
- Repository scans, issue refreshes, manifests, persisted manifests, drift checks, and repository-open lifecycle events now attach useful structured payloads.

### H10. Workflow Repository Cleanup - complete for source-of-truth cleanup

Goal: Make the workflow repo unambiguously the source of truth.

Scope:
- Rename documentation to IGMC Workflow Repository everywhere.
- Decide repository rename timing.
- Remove or regenerate partial `workflow_scaffold/template/` after compatibility window.
- Move reusable assets into standard layout where needed.
- Keep existing agents/workflows as managed assets.

Validation:
- `python validators/validate_standard_assets.py`.
- Scaffold smoke install into temp repo.

Latest implementation:
- Root `template/` is the only installable template tree.
- Stale partial `workflow_scaffold/template/` files were removed.
- `workflow_scaffold/apply.py` remains only as a compatibility wrapper.
- `.github/workflows/apply_scaffold.yml` now calls root `apply.py` directly.
- Workflow docs consistently describe the repo as the IGMC Workflow Repository.
- `validators/validate_standard_assets.py` rejects reintroduced `workflow_scaffold/template` content.

### H11. CI And Validator Hardening

Goal: Make local and CI validation converge.

Scope:
- Add repository contract validation to installed PR/nightly workflows.
- Add advisory alignment validation first.
- Later fail on critical violations once baselines are stable.
- Validate issue templates and PR template presence.

Validation:
- Temp repo scaffold check.
- CI dry-run if available.

### H12. Security And Authority Hardening

Goal: Enforce the separation of authority from the standard.

Scope:
- Strengthen secret detection in repository contracts/manifests.
- Prevent repository instructions from overriding global security policy.
- Mark unknown agents restricted by default.
- Display or policy-approve shell commands before execution.
- Keep force-push, delete, visibility changes, destructive migration blocked.

Validation:
- Unit tests for forbidden operation classification.
- Contract validator tests for secret-like fields.

## Suggested Next Sequence

1. H11 CI And Validator Hardening.
2. H12 Security And Authority Hardening.

## Decisions Needed Before Continuing

1. Should the workflow repository be officially renamed to `IGMC_WorkflowRepository` now, or after the hardening pass?
2. Should Command Deck read workflow standard YAML directly from a configured path, or should the workflow repo generate Rust-compatible rule/asset registries?
3. Should manifest proposals be written by default, or only with an explicit flag like `/repo adopt --write-manifest`?
4. Should safe remediation ever run automatically, or only through `/repo repair --apply`?
5. Should CI start advisory-only for alignment scores, or fail immediately on critical violations?
6. Should existing IGMC agents stay as-is for now and only receive metadata, or should we rename them to standard roles immediately?

## Current Recommendation

Proceed with H1 and H2 first. They tighten the core promise of the Operating Standard: every score must be deterministic, explainable, category-aware, and honest about exemptions and critical violations. After that, managed asset checksums and manifest persistence become much safer to implement.
