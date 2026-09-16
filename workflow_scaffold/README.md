# Workflow Scaffold Compatibility Wrapper

The canonical IGMC workflow installer is `../apply.py`. This directory remains only for older automation that invokes `workflow_scaffold/apply.py`; the wrapper delegates to the root installer and there is no second template tree here.

From the workflow repository root, install into another checkout with:

```sh
python apply.py --dest /path/to/repo --repo-id my-repo --repo-name "My Repo" --archetype rust-terminal-application
```

The installer copies `template/` paths into the destination. It includes the repository contract, baseline `docs/` artifacts, GitHub workflows and agents, and the `.agents/skills/igmc-issues` skill with `scripts/igmc_issue.py`.

## Codex issue generation

Open the destination repository in Codex for VS Code, the OpenAI desktop app, or CLI. Ask Codex to turn a request or a `docs/design/` section into GitHub issues. It writes reviewable `tickets/*.md` drafts, checks for duplicates, and uses the authenticated GitHub CLI to publish when asked. See the installed `AGENTS.md` and `.agents/skills/igmc-issues/SKILL.md` for the workflow.

GitHub Copilot remains available through `.github/copilot-instructions.md` and the optional GitHub agent files. Connecting the repository to Codex cloud or enabling Codex PR review is configured separately in Codex.
