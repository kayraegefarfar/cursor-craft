# Release gates — alpha to public V1

## Current state: v0.5.0-alpha

The source structure, policy content and offline checker are available in the public repository. Current local checks are recorded in [static checks](static-checks.md); practical-use feedback and case-level coverage are recorded in [runtime evidence](runtime-evidence.md). Historical CI and installation observations do not establish the status of a newer working tree. No release was created by this development review.

See the [runtime evidence guidance](runtime-evidence.md) and [maintainer review](maintainer-review.md). Automated release-readiness checks do not replace reviewer signoff.

## Required before labeling a public stable V1

The owner has since reported several days of successful use in normal projects.
This practical feedback is recorded in [runtime evidence](runtime-evidence.md);
it does not supply per-case evidence or a tested build/revision for these gates.

1. **License and provenance:** original package files reviewed; no user's existing global packs bundled; all borrowed content vetted.
2. **Manifest and compatibility:** plugin successfully installed/discovered on supported Cursor builds; no undocumented component paths.
3. **Coexistence:** tested beside representative global Rules/Skills/Plugins, not overwriting user settings or causing surprising conflicts.
4. **Functional:** T01–T12 executed in real controlled environment; critical gates passed, failures reported and tracked.
5. **Security:** authority boundaries, prompt-injection tests, permissions and secret redaction verified. No “prompt-only guaranteed protection” claims.
6. **Professional quality:** demonstrable code and UI results with actual independent evaluation; defects and unsupported features disclosed.
7. **Performance:** at least a measured comparison; no unsupported percentage savings claim.
8. **Rollback:** user-scoped and project-scoped removal tested without loss of unrelated work.
9. **Documentation:** clear install/uninstall, requirements, examples, supported platforms, known limitations, contribution and security channels.
10. **Public consent:** repository owner explicitly approves GitHub publishing and licensing; no remote push or Marketplace submission as an automatic side effect.

A project can publish an **honestly labeled experimental alpha** only after appropriate source/license checks and explicit publisher approval. A stable release should not claim completion while any relevant critical gate remains open.

## Distribution status labels

`DRAFT` → `STATIC_CHECKED` → `CURSOR_RUNTIME_TESTED` → `RELEASE_CANDIDATE` → `PUBLIC_STABLE`

Current status is **STATIC_CHECKED** only if bundled validators pass. Release status is not inferred from a document's title.
