# IGMC Agents

This repository uses the IGMC agent stack installed under `.github/agents/`.

The repository contract at `.igmc/repository.yml` declares which agents are enabled for this repository. Command Deck treats that contract as the local source of intent and the workflow repository as the global source of standard agent definitions.

Standard roles include planner, reviewer, documentarian, issue planner, repository governor, implementation, polishing, and optimization agents.