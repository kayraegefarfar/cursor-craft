# User-facing task examples

These prompts are demonstrations of expected **policy**, not evidence of working automation.

### Routine fix (should not call specialists)

> In this settings panel, align the icon with the label. Keep other styles unchanged and verify the result if UI tools are available.

### Design Studio (should seek approval for major direction)

> Redesign our main navigation with two meaningfully different, original concepts. Explain usability, keyboard and performance trade-offs. Do not change the existing visual identity or implement the full redesign until I select a direction.

### Authorized REA

> Analyze this open-source library's public tab-grouping implementation, check its license and the current architecture, and propose integration options. Start with directly related files; distinguish verified code facts from inferences. Do not install external analyzers.

### Risk-based review

> Review the session recovery diff for data loss, private browsing leakage, and regression risk. Report reproducible findings and the tests actually run; avoid speculative comments.

### Long task checkpoint

> Summarize our approved scope, exact changed files, verified passing/failing tests, pending work and safe next action. Do not include secrets or rewrite unrelated project files.
