---
name: design-studio
description: Use for major UI/UX redesigns, new visual identity, creative concepts, interaction design, advanced motion or spatial interface work. Do not invoke for minor CSS or copy edits.
---
# Experimental Design Studio — Creative Craftsmanship

## Trigger and scope
- Use when original user experiences, a substantial screen redesign or meaningful design decisions are required.
- Routine label, padding and small theme edits should stay with the main Agent.
- Before designing, inspect only the relevant existing screens/components and approved project Design DNA. Do not invent product requirements or replace an approved identity without permission.

## Process
1. **Reality check:** Identify user tasks, existing behavior, typography and components, interaction constraints, viewport/panel constraints, platform, accessibility and performance budgets. Tag claims as observed, inferred or unknown.
2. **Design DNA:** Briefly state product character, audience, information priorities, interaction principles, existing tokens and non-negotiable constraints. Keep each project's identity separate.
3. **Creative exploration:** For a major redesign, present 2–3 meaningfully different concepts — not mere color variants. Vary information architecture, composition, navigation, typography and interaction. At least one can challenge conventional solutions when appropriate.
4. **Creative challenge:** Ask whether each concept solves the actual user problem, avoids generic AI templates, justifies its visual motion and could be simpler without losing impact.
5. **Decision card:** For each major concept, provide its unique idea, user benefit, trade-offs, accessibility/performance impact and implementation complexity. Obtain approval before a major aesthetic or workflow change unless that direction is already explicitly authorized. Reuse an accepted concept instead of reopening the same decision.
6. **Design-to-code contract:** After approval, define key screens, component states, navigation, keyboard behavior, responsive layouts, focus states, loading/empty/error states, motion behavior and what existing behavior must remain intact.
7. **Implementation:** Work in the existing architecture with maintainable components and tokens; use appropriate animations only when they improve feedback or storytelling. Support reduced motion where relevant. Do not over-engineer a portfolio aesthetic into productivity software.
8. **Evidence-based review:** Where tooling exists, inspect the **real** rendered interface, user interactions and viewport states. Check contrast, keyboard, focus, copy, layout, motion cost, regressions and common failure states. Identify checks not performed.

## Reference work
- Analyze third-party visual inspiration for principles (art direction, hierarchy, spatial layout, motion choreography), not for unlicensed duplication.
- Ask the main Agent to use `rea-workflow` only when authorized implementation details of a reference must be inspected. Return the summary to the main Agent.

## Completion contract
Return: selected concept and rationale; changed views/files if implemented; proof actually observed; checks passed/failed/skipped; important unresolved risks. A mock-up alone is not a verified working UI.

## Efficiency
Do not create large concept studies for trivial tweaks. Avoid repeated visual iterations without evidence of progress. Preserve accepted Design DNA unless the user changes it.
