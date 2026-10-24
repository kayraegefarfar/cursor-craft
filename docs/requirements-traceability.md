# Requirements to artifacts (V0.5 source preview)

This is a **planning trace**, not evidence that the AI behaviors work in Cursor. A requirement is listed only where the package actually provides a relevant instruction, test fixture or source tool.

| Requirement | Source artifact | Planned real verification |
| --- | --- | --- |
| High craftsmanship across every discipline | `rules/professional-core.mdc`, `docs/professional-quality-rubric.md` | T02 implementation and independent review |
| Controlled autonomy and approval gates | `rules/professional-core.mdc`, `docs/architecture.md` | T12 scope expansion/approval test |
| Selective specialist activation | `skills/*/SKILL.md`, `examples/routing-cases.json` | T01, T03, T04 agent traces |
| Original, accessible design and real UI validation | `skills/design-studio/SKILL.md`, `docs/design-standard.md` | T03 interaction and screenshot checks |
| Evidence-first authorized source/app analysis | `skills/rea-workflow/SKILL.md` | T04, T11 with approved sources and tools |
| Security trust boundary, no auto secret disclosure | `rules/professional-core.mdc`, `docs/security-model.md` | T05 harmless injection fixture and tool logs |
| Deep risk-based quality | `skills/deep-quality-review/SKILL.md` | T08 known blocker detection |
| Long task checkpoint and memory hints | `skills/task-handoff/SKILL.md` | T07 real restart/handoff test |
| No conflicting parallel file edits | `docs/architecture.md` | T06 shared-workspace test |
| Safe removal/coexistence | `docs/installation.md`, `docs/migration.md` | T10 preview removal, restore tests |
| No exaggerated savings claims | `docs/benchmarks.md`, `tools/compare_runs.py` | T09 measured paired tasks |
| Open-source source quality | `tools/validate_package.py`, `tests/` | Offline preflight, tests, publication review |
| Honest runtime evidence and stable-release gating | `tools/release_readiness.py`, `examples/runtime-acceptance-template.json`, `docs/runtime-evidence.md` | T01–T12 independently reviewed, owner approval |

## Known gaps

- Instructions cannot force Agent or model selection, OS authorization, perfect prompt-injection resistance, automatic token caps, cross-chat memory, or real tool availability.
- Existing user-installed packs are not bundled. Name-only ZIP overlap reports are **hypotheses**.
- Runtime acceptance results are **NOT_RUN** until collected from a real Cursor test environment.
- GitHub publication ownership and security reporting channels require explicit final owner decisions.
