# IGMC Repository Operating Standard

**Document ID:** IGMC-ROS
**Status:** Draft Standard
**Schema version:** 1.0.0
**Applies to:** All repositories managed through Intergalactic Megacorporation Command Deck
**Primary implementation repository:** IGMC Workflow Repository
**Enforcement authority:** Command Deck Repository Governance Engine

---

## 1. Purpose

The IGMC Repository Operating Standard defines a common operational shape for all software, game, art, research, prototype, and consultancy repositories managed through Command Deck.

The standard exists to ensure that repositories remain:

* understandable by humans and AI agents;
* structurally predictable;
* recoverable after periods of inactivity;
* measurable instead of vaguely “organized”;
* compatible with shared agents and workflows;
* capable of producing uniformly structured issues, plans, reviews, and documentation;
* migratable as the global workflow evolves.

A repository does not need to begin in a clean state.

Repositories MAY originate as experiments, game-jam wreckage, client prototypes, copied directories, abandoned branches, or late-night creative detonations. The governance system MUST be capable of examining such a repository, describing its current state, and proposing a safe migration toward alignment.

The operating principle is:

> Chaos is permitted at creation time. Unmeasured chaos is not permitted indefinitely.

---

## 2. Architectural model

The system SHALL consist of three primary layers.

### 2.1 Global operating layer

The global operating layer contains rules and capabilities that apply across all managed repositories.

It includes:

* global agents;
* global skills;
* workflow definitions;
* repository archetypes;
* canonical schemas;
* documentation conventions;
* issue taxonomy;
* review policies;
* security policies;
* migration logic;
* alignment rules;
* telemetry definitions;
* Command Deck tool implementations.

The global operating layer MUST remain outside individual project repositories except where a generated or pinned copy is required for compatibility.

The global operating layer is the source of truth.

### 2.2 Repository contract layer

Each repository contains a repository-specific contract describing how the global standard applies to that repository.

It includes:

* repository identity;
* repository archetype;
* enabled workflow modules;
* repository-specific commands;
* important paths;
* documentation locations;
* issue configuration;
* agent overrides;
* validation commands;
* ignored or exempted rules;
* current standard version;
* migration history.

The repository contract MUST be machine-readable.

### 2.3 Runtime and telemetry layer

Command Deck owns runtime orchestration, workflow state, repository inspection, alignment evaluation, event normalization, and user-facing progress information.

GitHub Copilot SDK SHALL be the primary Copilot integration for agent sessions requiring:

* streaming events;
* tool-call visibility;
* subagent visibility;
* token and model usage;
* structured session lifecycle information;
* custom tool integration;
* session state.

The standalone Copilot CLI MAY remain available for:

* direct interactive sessions;
* debugging;
* compatibility;
* one-off commands;
* workflows not exposed through the SDK;
* emergency fallback.

The SDK emits session events representing agent activity, including writing and tool execution, and exposes a reliable idle event when the agent loop has stopped processing. Command Deck SHOULD normalize those events rather than scraping formatted terminal output.

---

## 3. Separation of authority

The system MUST distinguish between advisory AI behavior and enforceable deterministic behavior.

### 3.1 AI responsibilities

AI agents MAY:

* interpret design documents;
* classify repository contents;
* propose architecture;
* identify missing documentation;
* decompose plans into issues;
* draft migration recommendations;
* propose file moves;
* summarize code;
* review implementation quality;
* identify likely duplication;
* generate structured candidate data.

### 3.2 Deterministic system responsibilities

Command Deck, scripts, validators, hooks, and CI MUST control:

* schema validation;
* required fields;
* permitted file locations;
* issue creation;
* duplicate-operation prevention;
* migration application;
* file modification boundaries;
* branch and repository safety rules;
* alignment scoring;
* standard-version comparison;
* validation execution;
* generated-file integrity;
* final pass/fail decisions.

The governing rule is:

> AI interprets intent. Deterministic systems enforce contracts.

Prompts and custom instructions guide Copilot behavior, while hooks can guarantee that configured operations occur at specific stages or prevent tool operations. GitHub repository rulesets and required status checks MAY provide additional enforcement at the GitHub platform level.

---

## 4. Canonical repository shape

A fully aligned repository SHOULD support the following conceptual structure.

Not every repository requires every directory, but deviations MUST be declared by the repository contract.

```text
repository/
├── .igmc/
│   ├── repository.yml
│   ├── alignment-baseline.yml
│   ├── migrations/
│   ├── generated/
│   └── cache/
│
├── .github/
│   ├── copilot-instructions.md
│   ├── instructions/
│   ├── agents/
│   ├── prompts/
│   ├── hooks/
│   ├── ISSUE_TEMPLATE/
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│
├── docs/
│   ├── README.md
│   ├── design/
│   ├── architecture/
│   ├── decisions/
│   ├── plans/
│   ├── reviews/
│   ├── reference/
│   └── archive/
│
├── scripts/
│   ├── validate/
│   ├── development/
│   └── migration/
│
├── AGENTS.md
├── README.md
├── CONTRIBUTING.md
└── CHANGELOG.md
```

Repository-specific source directories remain outside the scope of this canonical structure unless an archetype defines them.

Examples include:

```text
src/
Assets/
Packages/
crates/
app/
server/
client/
tests/
tools/
```

---

## 5. Repository contract

Every managed repository MUST contain:

```text
.igmc/repository.yml
```

This file is the local machine-readable declaration of repository intent.

### 5.1 Minimum contract

```yaml
schema_version: "1.0"

repository:
  id: "command-deck"
  name: "Intergalactic Megacorporation Command Deck"
  archetype: "rust-terminal-application"
  lifecycle: "active"
  visibility: "private"

standard:
  profile: "igmc-default"
  version: "1.0.0"
  last_alignment_check: null
  automatic_checks: true

paths:
  source:
    - "src"
  tests:
    - "tests"
  documentation: "docs"
  design: "docs/design"
  architecture: "docs/architecture"
  decisions: "docs/decisions"
  plans: "docs/plans"
  reviews: "docs/reviews"

commands:
  setup: "cargo build"
  validate: "cargo check"
  test: "cargo test"
  format_check: "cargo fmt --check"
  lint: "cargo clippy --all-targets --all-features -- -D warnings"

issues:
  provider: "github"
  schema: "igmc-issue-v1"
  sync_on_open: true
  stale_after_minutes: 15

agents:
  enabled:
    - "planner"
    - "reviewer"
    - "documentarian"
    - "issue-planner"
    - "repository-governor"

alignment:
  target_score: 90
  blocking_score: 70
  scan_on_open: true
  full_scan_interval_hours: 24

exemptions: []
```

### 5.2 Contract rules

The repository contract:

* MUST be committed to version control;
* MUST declare a schema version;
* MUST declare the applied workflow-standard version;
* MUST declare the repository archetype;
* MUST define validation commands where applicable;
* MUST declare all exemptions;
* MUST NOT contain secrets;
* SHOULD use paths relative to the repository root;
* SHOULD be readable without invoking an AI model.

---

## 6. Global workflow repository

The IGMC Workflow Repository is the canonical distribution source for the operating standard.

It SHOULD contain:

```text
igmc-workflow/
├── standard/
│   ├── repository-standard.md
│   ├── schemas/
│   ├── policies/
│   ├── archetypes/
│   └── scoring/
│
├── agents/
├── skills/
├── prompts/
├── hooks/
├── templates/
│   ├── repository/
│   ├── documentation/
│   ├── issues/
│   └── pull-requests/
│
├── migrations/
├── validators/
├── commands/
└── VERSION
```

### 6.1 Versioning

The workflow standard MUST use semantic versioning.

* **Patch:** clarification or backward-compatible validator improvement.
* **Minor:** new optional capabilities or automatically migratable rules.
* **Major:** breaking repository-contract or structural change.

Each managed repository MUST record the version it conforms to.

Command Deck MUST be able to compare:

```text
Installed repository version: 1.2.0
Current global version:        1.5.0
Migration path available:      yes
```

### 6.2 Distribution model

The global repository SHOULD distribute components through generated installation manifests rather than blind directory copying.

Each distributed asset SHOULD contain metadata resembling:

```yaml
asset:
  id: "agent.repository-reviewer"
  version: "2.1.0"
  source: "agents/repository-reviewer.agent.md"
  destination: ".github/agents/repository-reviewer.agent.md"
  strategy: "managed-copy"
  checksum: "sha256:..."
```

Supported distribution strategies MAY include:

* `managed-copy`
* `generated`
* `merge`
* `repository-owned`
* `global-only`
* `symlink`, where the platform and repository policy permit it

Files managed by the global workflow MUST be identifiable as managed assets.

Repository-owned files MUST NOT be overwritten without an explicit migration operation.

---

## 7. Repository archetypes

Every repository MUST select one archetype.

Example archetypes:

* `rust-terminal-application`
* `unity-project`
* `web-application`
* `javascript-library`
* `python-tool`
* `research-repository`
* `creative-prototype`
* `documentation-only`
* `client-delivery`
* `generic-software`

An archetype defines:

* expected source paths;
* expected commands;
* documentation requirements;
* standard agents;
* standard ignores;
* CI expectations;
* testing expectations;
* generated-file rules;
* archetype-specific alignment checks.

Archetypes SHOULD inherit from a shared base profile.

Example:

```yaml
id: "unity-project"
extends: "igmc-default"

expected:
  paths:
    - "Assets"
    - "Packages"
    - "ProjectSettings"

documentation:
  required:
    - "docs/design"
    - "docs/architecture"
    - "docs/decisions"

checks:
  - "unity.project-version-present"
  - "unity.meta-files-consistent"
  - "unity.library-not-versioned"
  - "unity.generated-folders-ignored"
```

---

## 8. Repository adoption workflow

Command Deck SHALL expose:

```text
/repo adopt
```

The command transforms an unmanaged or partially managed repository into a repository governed by this standard.

### 8.1 Default safety behavior

`/repo adopt` MUST operate as a dry run unless explicitly instructed to apply changes.

Default behavior:

```text
/repo adopt
→ inspect
→ classify
→ compare
→ generate manifest
→ present proposal
→ make no repository changes
```

Application requires:

```text
/repo adopt --apply
```

Potentially destructive operations MUST require an additional explicit policy or confirmation mechanism.

### 8.2 Adoption stages

#### Stage 1: Discover

Inspect:

* repository metadata;
* current branch and dirty state;
* languages and frameworks;
* build systems;
* source directories;
* documentation;
* existing GitHub configuration;
* existing Copilot customization;
* existing agents and prompts;
* issue templates;
* pull request templates;
* CI workflows;
* testing commands;
* stale or contradictory instructions.

#### Stage 2: Classify

Determine:

* likely repository archetype;
* lifecycle state;
* current workflow version, if any;
* existing conventions worth preserving;
* managed and unmanaged assets;
* confidence level for each classification.

#### Stage 3: Compare

Compare the repository against:

* the selected archetype;
* the global standard;
* enabled modules;
* repository-specific exemptions;
* the previous alignment baseline.

#### Stage 4: Propose

Generate a migration manifest.

#### Stage 5: Review

Present:

* proposed additions;
* proposed modifications;
* proposed moves;
* proposed archive operations;
* conflicts;
* uncertain classifications;
* expected alignment-score improvement;
* commands that will be executed.

#### Stage 6: Apply

Apply only approved manifest operations.

#### Stage 7: Validate

Run:

* structural validation;
* schema validation;
* documentation validation;
* repository-specific validation commands;
* tests, where requested or required;
* final alignment scan.

#### Stage 8: Record

Create:

* a migration record;
* an updated alignment baseline;
* a human-readable summary;
* optionally a commit or pull request.

---

## 9. Migration manifest

Every adoption or alignment-repair operation MUST generate a migration manifest before applying changes.

### 9.1 Example manifest

```yaml
manifest_version: "1.0"

operation:
  id: "mig-2026-07-24-command-deck-001"
  type: "repository-adoption"
  created_at: "2026-07-24T19:00:00+03:00"
  repository: "command-deck"
  base_commit: "abc1234"
  workflow_version_from: null
  workflow_version_to: "1.0.0"

classification:
  archetype: "rust-terminal-application"
  confidence: 0.97

summary:
  alignment_before: 46
  alignment_expected_after: 89
  files_added: 8
  files_modified: 3
  files_moved: 1
  files_deleted: 0
  issues_proposed: 7

operations:
  - id: "op-001"
    action: "create"
    destination: ".igmc/repository.yml"
    source_template: "templates/repository/repository.yml"
    ownership: "repository"

  - id: "op-002"
    action: "install-managed"
    destination: ".github/agents/reviewer.agent.md"
    source: "agents/reviewer.agent.md"
    ownership: "workflow"
    expected_checksum: "sha256:..."

  - id: "op-003"
    action: "move"
    source: "DESIGN_NOTES.md"
    destination: "docs/design/command-deck.md"
    preserve_history: true

  - id: "op-004"
    action: "generate"
    destination: ".github/ISSUE_TEMPLATE/feature.yml"
    generator: "issue-template-generator"
    schema: "igmc-issue-v1"

validations:
  - "repository.contract.valid"
  - "documentation.frontmatter.valid"
  - "cargo.check"
  - "cargo.test"

conflicts: []
warnings:
  - "README.md contains setup instructions inconsistent with Cargo.toml"

rollback:
  strategy: "git"
  requires_clean_worktree: true
```

### 9.2 Manifest properties

A manifest MUST be:

* deterministic where practical;
* reviewable;
* serializable;
* replayable where safe;
* bound to a base commit;
* rejected if the repository has changed incompatibly;
* recorded after successful application.

A manifest MUST distinguish:

* generated proposals;
* approved operations;
* completed operations;
* failed operations;
* skipped operations.

---

## 10. Managed files and drift

The system MUST detect drift between globally managed files and installed repository copies.

For each managed file, Command Deck SHOULD retain:

* source asset ID;
* source version;
* installed version;
* source checksum;
* installed checksum;
* installation strategy;
* local-modification policy.

Drift states:

```text
CURRENT
OUTDATED
LOCALLY MODIFIED
MISSING
UNKNOWN SOURCE
CONFLICT
```

Command Deck MUST NOT overwrite `LOCALLY MODIFIED` files automatically unless the asset policy explicitly permits regeneration.

A three-way merge MAY be proposed when:

* the previous global version is known;
* the current global version is known;
* the local modified version is available.

---

## 11. Documentation standard

### 11.1 Documentation categories

Documentation SHOULD be classified into:

* **Design:** what should be built and why.
* **Architecture:** how the system is structured.
* **Decision records:** why a significant choice was made.
* **Plans:** bounded intended work.
* **Reviews:** findings without direct implementation authority.
* **Reference:** stable factual or operational information.
* **Archive:** superseded material retained for history.

### 11.2 Required document metadata

Managed Markdown documents SHOULD use frontmatter.

```yaml
---
id: "design-command-deck-repository-governance"
type: "design"
title: "Command Deck Repository Governance"
status: "active"
owners:
  - "Ari"
created: "2026-07-24"
updated: "2026-07-24"
version: "1.0"
related_issues: []
supersedes: []
---
```

### 11.3 Document statuses

Permitted statuses SHOULD include:

* `draft`
* `active`
* `accepted`
* `implemented`
* `superseded`
* `archived`

### 11.4 Documentation checks

Alignment checks MAY validate:

* correct location;
* valid frontmatter;
* recognized document type;
* stable document ID;
* valid status;
* no broken internal links;
* no duplicate active design documents;
* no references to deleted paths;
* update age;
* implementation-status consistency;
* explicit supersession relationships.

Age alone MUST NOT automatically make a document invalid.

A stale document is one whose claims conflict with the repository, not simply one whose timestamp is old.

---

## 12. Issue standard

Every issue created through Command Deck MUST conform to an issue schema.

GitHub Issue Forms support required structured fields that are converted to a normal Markdown issue body. They SHOULD be generated from the same canonical schema used by Command Deck rather than maintained as an unrelated second definition.

### 12.1 Canonical issue object

```yaml
schema_version: "1.0"

title: "Add repository alignment status panel"
type: "feature"
area: "repository-governance"
status: "proposed"

summary: >
  Display repository alignment score, detected drift,
  and outstanding remediation actions.

motivation: >
  The operator needs immediate awareness of whether the active
  repository conforms to the current IGMC workflow standard.

scope:
  included:
    - "Display total alignment score"
    - "Display category scores"
    - "List blocking violations"
    - "Show last scan time"
  excluded:
    - "Automatic remediation"

acceptance_criteria:
  - id: "AC-1"
    text: "The panel displays the current total alignment score."
  - id: "AC-2"
    text: "Blocking violations are visually distinguishable."
  - id: "AC-3"
    text: "The user can open the full alignment report."

validation:
  - "cargo test"
  - "manual TUI inspection"

source_references:
  - "docs/design/repository-governance.md#alignment"

dependencies: []
risks: []
implementation_notes: []
```

### 12.2 AI-generated issues

AI-generated issue candidates MUST pass through the following pipeline:

```text
source documents
→ semantic interpretation
→ structured candidate object
→ schema validation
→ duplicate detection
→ human or policy approval
→ GitHub issue creation
→ source linkage
```

The agent MUST NOT directly create issues when operating in proposal-only mode.
### 12.2.1 Codex issue generation

Codex MAY generate issue drafts from repository requests or `docs/` sources in the local checkout. The shared `.agents/skills/igmc-issues/SKILL.md` workflow is available to Codex in VS Code, the OpenAI desktop app, and CLI. It records each candidate in `tickets/*.md`, validates the draft, checks existing GitHub issues for duplicates, and publishes only when issue creation is requested. GitHub Copilot remains an optional agent for implementation; its assignment is not a precondition for issue generation.

### 12.3 Source traceability

Every issue extracted from documentation SHOULD record:

* source document;
* source section;
* extraction timestamp;
* originating workflow session;
* design-version identifier.

This allows Command Deck to identify:

* issues whose source design changed;
* design sections with no implementation tracking;
* closed issues linked to still-unresolved requirements;
* duplicated issue extraction.

---

## 13. Alignment engine

Command Deck SHALL include a deterministic repository alignment engine.

Its output is not a judgment of code quality.

It measures conformance to the declared repository contract and selected workflow standard.

### 13.1 Alignment categories

The initial alignment model SHALL use the following categories:

| Category               | Default weight |
| ---------------------- | -------------: |
| Repository contract    |             15 |
| Structural conformity  |             10 |
| AI configuration       |             15 |
| Documentation          |             15 |
| Issue governance       |             10 |
| Validation and testing |             15 |
| Git and CI governance  |             10 |
| Workflow currency      |             10 |
| **Total**              |        **100** |

Archetypes MAY adjust weights.

### 13.2 Rule result states

Each rule returns one of:

```text
PASS
WARN
FAIL
BLOCKED
NOT_APPLICABLE
EXEMPT
UNKNOWN
```

### 13.3 Rule model

```yaml
id: "documentation.design-directory-present"
category: "documentation"
severity: "required"
weight: 2
applies_to:
  - "*"
check:
  type: "path-exists"
  path: "docs/design"
remediation:
  type: "create-directory"
  safe: true
```

### 13.4 Score calculation

For applicable, non-exempt rules:

```text
category score =
earned rule weight / applicable rule weight × 100
```

Total score:

```text
sum(category score × category weight)
```

`WARN` SHOULD receive partial credit only when the rule explicitly defines it.

Example:

```text
PASS:    100%
WARN:     50%
FAIL:      0%
BLOCKED:   0%
UNKNOWN:   0%
```

### 13.5 Critical violations

Some rules MUST be designated critical.

Examples:

* invalid repository contract;
* secrets committed in managed configuration;
* no recognized source or project root;
* workflow asset conflict;
* required validation command cannot be resolved;
* migration manifest base commit mismatch;
* generated issue schema invalid;
* repository-level instructions contradict mandatory safety policy.

A repository with a critical violation MUST NOT report `FULLY ALIGNED`, regardless of numerical score.

### 13.6 Alignment grades

```text
95–100  FULLY ALIGNED
85–94   ALIGNED
70–84   PARTIALLY ALIGNED
50–69   DRIFTING
0–49    UNGOVERNED
```

The displayed grade MUST also show whether critical violations exist.

Example:

```text
Alignment: 91 / 100 — ALIGNED
Critical violations: 1
```

### 13.7 Score transparency

Every score MUST be explainable.

The user MUST be able to inspect:

* each rule;
* its result;
* its weight;
* evidence;
* recommended remediation;
* whether remediation is automatic;
* whether the rule is exempted.

Command Deck MUST NOT produce an AI-invented alignment percentage.

---

## 14. Repository-open lifecycle

When the active repository changes, Command Deck SHALL execute a repository-open lifecycle.

### 14.1 Immediate operations

These operations SHOULD be fast and deterministic:

```text
1. Resolve repository root
2. Read repository contract
3. Read cached alignment state
4. Inspect Git status
5. Refresh or load issue cache
6. Compare installed workflow version
7. Determine whether scans are stale
8. Render repository summary
```

### 14.2 Cached initial state

Command Deck SHOULD immediately display the most recent known state:

```text
Repository: Command Deck
Branch: main
Working tree: 3 modified files

Issues:
  Open: 18
  In progress: 4
  Blocked: 1

Alignment:
  Cached score: 86
  Last full scan: 21 hours ago
  Workflow update available: 1.4.0 → 1.5.0
```

The UI MUST clearly distinguish cached data from freshly validated data.

### 14.3 Refresh policy

The repository contract SHALL define scan intervals.

Example:

```yaml
issues:
  stale_after_minutes: 15

alignment:
  quick_scan_interval_minutes: 30
  full_scan_interval_hours: 24
```

### 14.4 Quick scan

A quick scan MAY include:

* required-path existence;
* contract validity;
* workflow-version comparison;
* managed-file checksums;
* issue-template presence;
* documentation-index presence;
* GitHub workflow presence;
* Git state.

Quick scans SHOULD avoid expensive AI calls.

### 14.5 Full scan

A full scan MAY include:

* all quick checks;
* documentation validation;
* source/document link checks;
* issue-schema analysis;
* open-issue synchronization;
* build-command verification;
* test discovery;
* agent configuration validation;
* managed-asset drift analysis;
* semantic document consistency checks;
* repository summary regeneration.

Deterministic checks MUST run before semantic AI checks.

### 14.6 Background semantics

The TUI MAY keep operating while scans execute concurrently, but Command Deck MUST display that state explicitly.

Example:

```text
Repository loaded
Alignment scan: running
Current stage: validating documentation
```

No result may be labeled current until the relevant scan completes.

---

## 15. Repository status snapshot

Command Deck SHOULD maintain a local derived snapshot:

```text
.igmc/cache/repository-status.json
```

This file SHOULD normally be ignored by Git.

Example:

```json
{
  "repositoryId": "command-deck",
  "headCommit": "abc1234",
  "scannedAt": "2026-07-24T19:10:00+03:00",
  "alignment": {
    "score": 86,
    "grade": "aligned",
    "criticalViolations": 0
  },
  "issues": {
    "open": 18,
    "inProgress": 4,
    "blocked": 1,
    "refreshedAt": "2026-07-24T19:09:45+03:00"
  },
  "workflow": {
    "installed": "1.4.0",
    "available": "1.5.0"
  }
}
```

The cache is an optimization, not a source of truth.

---

## 16. Command Deck governance commands

The initial command surface SHOULD include:

```text
/repo status
/repo scan
/repo align
/repo adopt
/repo migrate
/repo diff-standard
/repo explain
/repo exemptions
/repo repair
```

### 16.1 `/repo status`

Displays:

* repository identity;
* branch;
* dirty state;
* issue summary;
* alignment score;
* workflow version;
* stale scans;
* critical violations.

### 16.2 `/repo scan`

Runs alignment checks.

Options:

```text
/repo scan --quick
/repo scan --full
/repo scan --category documentation
/repo scan --rule issue.schema-valid
```

### 16.3 `/repo align`

Generates remediation proposals for current violations.

It MUST NOT apply changes by default.

### 16.4 `/repo adopt`

Creates the initial repository contract and migration manifest.

### 16.5 `/repo migrate`

Migrates from one workflow-standard version to another.

### 16.6 `/repo diff-standard`

Displays repository drift against the active standard.

### 16.7 `/repo explain`

Explains a rule, score, violation, or proposed operation.

Example:

```text
/repo explain documentation.frontmatter-valid
```

### 16.8 `/repo exemptions`

Lists, creates, reviews, and removes declared exemptions.

### 16.9 `/repo repair`

Applies safe, deterministic remediations.

It SHOULD require a generated manifest.

---

## 17. Exemptions

Repositories MAY intentionally diverge from the standard.

Every exemption MUST be explicit.

```yaml
exemptions:
  - rule: "documentation.architecture-directory-present"
    reason: "Single-file experimental prototype with no architecture layer."
    approved_by: "Ari"
    approved_at: "2026-07-24"
    review_after: "2026-10-24"
```

Exemptions:

* MUST include a reason;
* SHOULD include a review date;
* MUST NOT silently convert failed rules into passes;
* MUST remain visible in alignment reports;
* MAY reduce the maximum achievable score if policy defines the rule as non-exemptible.

A permanent exemption is allowed, but “I got tired of looking at the warning” is not architecture.

---

## 18. Copilot customization model

The repository governance system SHALL recognize four distinct Copilot customization mechanisms.

### 18.1 Instructions

Instructions define persistent project facts, coding conventions, validation expectations, and behavioral constraints.

GitHub Copilot CLI discovers repository instructions such as `AGENTS.md` and repository-specific custom instruction files.

### 18.2 Agents

Agents define specialized roles.

Standard IGMC agents SHOULD include:

* planner;
* repository governor;
* reviewer;
* documentarian;
* issue planner;
* implementation agent;
* test agent;
* research agent.

GitHub custom agents are specialized configurations intended to follow particular workflows, conventions, and tool policies.

### 18.3 Skills

Skills provide reusable task-specific instructions, scripts, and resources that agents load when relevant.

Examples:

* repository classification;
* Unity project inspection;
* Rust validation;
* issue extraction;
* architecture-decision generation;
* documentation-link validation.

### 18.4 Hooks

Hooks perform deterministic operations at defined agent lifecycle points.

They SHOULD be used for:

* policy checks;
* operation logging;
* telemetry enrichment;
* blocking forbidden commands;
* validating generated output;
* recording session metadata.

They SHOULD NOT contain large semantic workflows better represented as Command Deck tasks.

---

## 19. SDK runtime event model

Command Deck SHALL normalize provider-specific events into its own internal event schema.

### 19.1 Internal event envelope

```json
{
  "eventId": "evt-001",
  "sessionId": "session-123",
  "taskId": "task-456",
  "timestamp": "2026-07-24T19:20:00.000+03:00",
  "source": "github-copilot-sdk",
  "type": "tool.started",
  "phase": "repository-analysis",
  "data": {}
}
```

### 19.2 Required normalized event types

```text
session.started
session.idle
session.completed
session.failed

phase.started
phase.completed
phase.failed

agent.selected
agent.started
agent.completed
agent.failed

message.delta
message.completed

tool.requested
tool.started
tool.progress
tool.completed
tool.failed

file.read
file.created
file.modified
file.deleted

validation.started
validation.completed
validation.failed

usage.updated
warning
error
```

### 19.3 Provider isolation

The TUI MUST consume normalized Command Deck events, not raw SDK objects.

This enables future support for:

* Copilot SDK;
* Copilot CLI;
* local OpenAI-compatible models;
* OpenAI API;
* Anthropic;
* deterministic scripts;
* MCP tools;
* custom local agents.

The visual interface must not care which creature is behind the curtain.

---

## 20. Progress presentation

Progress MUST be based on observable state.

### 20.1 Bounded progress

Percentages MAY be shown for bounded tasks:

```text
Documents validated: 14 / 22
Issues synchronized: 18 / 18
Migration operations: 7 / 11
Test suites completed: 3 / 5
```

### 20.2 Unbounded agent work

For open-ended agent work, Command Deck MUST show:

* current phase;
* current operation;
* elapsed time;
* tool calls;
* files inspected;
* files changed;
* model turns;
* validation status.

It MUST NOT invent a percentage.

Example:

```text
REPOSITORY ALIGNMENT

Phase: Documentation analysis
Current: Comparing active design documents with open issues
Elapsed: 00:18

Files inspected: 41
Documents classified: 12
Tool calls: 9
Agent turns: 4
Warnings found: 3
```

### 20.3 Hierarchical task model

Progress SHOULD be hierarchical:

```text
Repository alignment
├── Contract validation                 complete
├── Managed asset comparison            complete
├── Documentation analysis              running
│   ├── Classify documents              complete
│   ├── Validate metadata               complete
│   └── Compare designs to issues       running
├── Validation commands                 pending
└── Final score                         pending
```

### 20.4 Activity log

The user SHOULD be able to switch between:

* concise current status;
* task hierarchy;
* chronological event log;
* tool details;
* file changes;
* usage metrics.

---

## 21. Alignment history

Command Deck SHOULD retain alignment history outside the Git repository or in a committed summary, depending on repository policy.

Useful historical metrics include:

* score over time;
* category scores;
* number of critical violations;
* workflow version;
* average remediation age;
* stale-document count;
* unmanaged-file count;
* issue-schema conformance;
* validation success rate.

Example:

```text
Jul 01   58  DRIFTING
Jul 08   72  PARTIALLY ALIGNED
Jul 15   84  PARTIALLY ALIGNED
Jul 24   91  ALIGNED
```

Alignment history SHOULD help expose repository decay.

It MUST NOT become a vanity KPI optimized by adding meaningless files.

---

## 22. Automatic remediation policy

Remediations SHALL be classified by risk.

### 22.1 Safe

May be applied automatically when enabled:

* create missing empty directory;
* regenerate ignored cache;
* update generated managed file with no local modifications;
* create missing documentation index;
* refresh derived metadata;
* update workflow checksum records.

### 22.2 Review required

Requires an approved manifest:

* create repository contract;
* install agents;
* install hooks;
* add issue templates;
* modify CI;
* move documents;
* rewrite frontmatter;
* add validation scripts;
* update repository instructions.

### 22.3 Destructive

Requires explicit approval and MUST NOT be bundled into ordinary automatic alignment:

* delete files;
* overwrite locally modified managed files;
* archive active documents;
* close issues;
* change branch protection;
* alter repository visibility;
* force-push;
* rewrite Git history.

---

## 23. CI enforcement

Local Command Deck checks provide visibility and early remediation.

CI provides repository-level enforcement.

The workflow repository SHOULD provide reusable validation workflows that check:

* repository contract validity;
* managed-file integrity;
* documentation schemas;
* issue-template validity;
* prohibited paths;
* generated-file freshness;
* repository-specific commands;
* alignment threshold.

Example policy:

```yaml
ci:
  alignment:
    minimum_score: 80
    fail_on_critical: true
    fail_on_score_regression: false
```

A repository MAY initially run alignment CI in advisory mode.

A mature repository SHOULD require the alignment check before merge.

GitHub rulesets can require status checks and control how protected branches are updated.

---

## 24. Security requirements

The governance system MUST assume that repository content may contain malicious or outdated instructions.

Therefore:

* repository instructions MUST NOT override global security policy;
* hooks MUST be inspected before execution;
* migration scripts MUST be treated as executable code;
* unknown agents MUST NOT receive unrestricted tools automatically;
* shell commands MUST be displayed or policy-approved;
* secrets MUST NOT be written to repository contracts or manifests;
* external URLs MUST follow provider permission policies;
* destructive commands MUST be blocked by default;
* repositories obtained from third parties MUST begin in restricted mode.

The repository governor agent is not the security authority.

Command Deck is.

---

## 25. Initial implementation phases

### Phase 1: Deterministic repository awareness

Implement:

* repository contract;
* archetype registry;
* repository-open lifecycle;
* issue refresh;
* quick alignment scan;
* cached repository snapshot;
* alignment status panel;
* rule explanation.

No AI is required for most of this phase.

### Phase 2: Workflow installation

Implement:

* global workflow asset registry;
* `/repo adopt`;
* migration manifest;
* managed-file checksums;
* safe remediation;
* workflow-version comparison;
* migration history.

### Phase 3: Copilot SDK core

Implement:

* SDK session host;
* event normalization;
* task hierarchy;
* tool-call timeline;
* usage metrics;
* agent selection;
* Command Deck custom tools;
* reliable completion through session lifecycle events.

### Phase 4: Semantic repository analysis

Implement:

* documentation classification;
* design-to-issue extraction;
* duplicate issue analysis;
* stale-claim detection;
* repository summary generation;
* AI-assisted remediation proposals.

### Phase 5: Enforcement

Implement:

* CI validator;
* reusable GitHub workflow;
* alignment thresholds;
* branch-rule integration;
* formal exemptions;
* score history;
* policy modules.

---

## 26. Minimum viable release

The first useful version MUST support:

1. Opening a repository.
2. Reading or detecting the absence of `.igmc/repository.yml`.
3. Refreshing GitHub issues.
4. Displaying cached repository state immediately.
5. Running a deterministic quick alignment scan.
6. Showing a transparent alignment score.
7. Listing failed rules and evidence.
8. Generating a dry-run adoption manifest.
9. Applying safe selected operations.
10. Recording the installed workflow version.
11. Running a Copilot SDK task with visible streamed activity.
12. Distinguishing bounded progress from unbounded agent activity.

It does not need to automatically solve every violation.

Seeing the repository clearly is the first victory.

---

## 27. Acceptance criteria

This design is considered initially implemented when:

* every managed repository can declare its archetype and workflow version;
* Command Deck can inspect any local Git repository without modifying it;
* `/repo adopt` produces a reviewable migration manifest;
* no adoption changes occur in default dry-run mode;
* managed workflow files can be distinguished from repository-owned files;
* repository alignment is calculated deterministically;
* every alignment deduction can be explained;
* issue state refreshes when the active repository changes;
* scan freshness is visible;
* stale repositories can be detected against the current workflow version;
* Copilot SDK events appear through a provider-neutral event model;
* agent activity can be followed without fake percentages;
* issue candidates generated from design documents are validated before creation;
* critical violations prevent a repository from appearing fully aligned;
* the same workflow repository can install or update the standard across multiple repositories.

---

## 28. Foundational principles

1. **Command Deck owns orchestration.**
2. **The workflow repository owns the standard.**
3. **The repository contract owns local intent.**
4. **AI proposes meaning; code enforces structure.**
5. **Every mutation begins as a manifest.**
6. **Every score must be explainable.**
7. **Cached data must be visibly cached.**
8. **Repository exceptions must be explicit.**
9. **Global upgrades must not silently erase local knowledge.**
10. **The system should make neglected repositories recoverable, not shameful.**
11. **An agent is a worker, not the foreman.**
12. **No progress bar shall lie merely to comfort the operator.**

---

## 29. Recommended first files

The initial implementation SHOULD begin with:

```text
workflow-repository/
├── standard/
│   ├── repository-operating-standard.md
│   ├── schemas/
│   │   ├── repository.schema.json
│   │   ├── migration-manifest.schema.json
│   │   ├── alignment-rule.schema.json
│   │   └── issue.schema.json
│   ├── archetypes/
│   │   ├── base.yml
│   │   ├── rust-terminal-application.yml
│   │   └── unity-project.yml
│   └── scoring/
│       └── default.yml
│
├── agents/
│   └── repository-governor.agent.md
│
├── migrations/
│   └── registry.yml
│
├── templates/
│   └── repository/
│       └── repository.yml
│
└── validators/
    ├── repository-contract
    ├── migration-manifest
    └── alignment
```

The first Command Deck implementation SHOULD then add:

```text
src/
├── repository/
│   ├── discovery
│   ├── contract
│   ├── archetype
│   ├── snapshot
│   └── issue_sync
│
├── governance/
│   ├── rules
│   ├── scanner
│   ├── scoring
│   ├── remediation
│   └── migrations
│
├── agents/
│   ├── copilot_sdk
│   ├── events
│   └── tools
│
└── ui/
    ├── repository_status
    ├── alignment
    ├── task_tree
    └── event_log
```

---

## 30. Closing definition

A repository governed by Command Deck is not merely a folder containing source code.

It is a versioned operational object with:

* a declared identity;
* a known lifecycle;
* an observable shape;
* an explicit relationship to the global workflow;
* measurable alignment;
* traceable documentation;
* structured work;
* controlled automation;
* recoverable history.

The goal is not to turn every repository into a sterile corporate mausoleum.

The goal is to preserve the speed and creative violence of prototyping while leaving enough lights on that a human—or an agent—can return six months later and understand what happened there.
