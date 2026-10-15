# AI Assistance Log — GR05 (Living Document)

Review permitted AI use and the declaration/citation format with the lecturer, as advised by HFU. For project traceability, retain whole AI conversations, document tools/purposes/sections, verify statements and references, and identify incorporated AI-generated text or reasoning with attribution. Conversation retention is a project practice; the lecturer should confirm submission requirements.

| Date | Tool/version | Purpose | Files/sections affected | Human review and changes | Prompt or archived chat link |
|---|---|---|---|---|---|
| 2026-10-15 | ChatGPT (GPT-6) | Suggested structure and drafted initial Task 2 business case/data inventory using course instructions and paper | `docs/02-business-case.md`, `docs/03-data-inventory-access.md` (originally `docs/04-data-inventory-access.md`) | Pending team fact-check and rewriting | Add exported conversation/share link |
| 2026-10-15 | Codex (GPT-6) | Reviewed README, all existing docs, working tree, and commit history; reorganized documentation; updated README, approval status, and historical proposal context; added Git ignore rules; checked HFU AI guidance and GitHub contributor documentation; diagnosed Copilot co-author attribution | `README.md`, `.gitignore`, `docs/01-project-definition.md`, `docs/03-data-inventory-access.md` (renamed), `docs/04-dataset-evaluation.md`, `docs/ai-use-log.md` | Automated local link, ignore-rule, and whitespace checks; team review pending. No dataset downloaded, experiments run, or scientific results claimed. | This conversation; team to retain an export or add a share link |
| 2026-10-15 | Codex (GPT-6) | At the user's explicit request, removed the Copilot co-author trailer from the latest local commit and prepared a separate commit for the documentation cleanup | Local Git history and `docs/ai-use-log.md`; cleanup files listed above | Verified replacement commit `854d158` has the same file tree, parent, human author, and author date as `3738ca8`, with no Copilot trailer. No remote changes; user will review and push. | This conversation; team to retain an export or add a share link |
| 2026-10-15 | Codex (GPT-6) | Added the proposed repository layout to the README as a roadmap, adapted to current document names and local data exclusions; committed this documentation update at the user's request | `README.md` (Planned structure), `docs/ai-use-log.md` | Checked the diff and whitespace; no placeholder folders or implementation files created. Team review pending; no push performed. | This conversation; team to retain an export or add a share link |

## Attribution follow-up

Original commit `3738ca869c7dd1eccbee636dbf933d1c12f2c5fd` (`Update predictive maintenance project proposal`) contained a Copilot `Co-authored-by` trailer. The exact extent of that earlier assistance is not established by the trailer; the team should document it from the original conversation. Removing a Git co-author credit does not remove the need to disclose AI assistance academically.

With explicit user authorization, the local commit was amended to `854d158`, preserving its file tree, parent, human author, author date, and subject while removing the Copilot trailer. The documentation cleanup is committed separately after this correction. Nothing was pushed: the user will review and publish the changes. Updating remote `main` will require a force-with-lease push because the original commit was already published.

**Guideline:** https://www.hs-furtwangen.de/en/hfu-insights/studying-at-hfu/academic-work-including-with-ai-tools
