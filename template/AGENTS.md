# IGMC Agents

This repository uses the IGMC agent stack installed under `.github/agents/`.

The repository contract at `.igmc/repository.yml` declares which agents are enabled for this repository. Command Deck treats that contract as the local source of intent and the workflow repository as the global source of standard agent definitions.

Standard roles include planner, reviewer, documentarian, issue planner, repository governor, implementation, polishing, and optimization agents.

## Issue generation

When asked to generate GitHub issues from a request, design document, or plan, use `.agents/skills/igmc-issues/SKILL.md`. Drafts live in `tickets/`; `scripts/igmc_issue.py check` validates them, and `publish` creates GitHub issues when requested. Check existing issues first. Codex works from VS Code, the OpenAI desktop app, or CLI. Copilot remains an optional implementation route and must not be assigned by default.
