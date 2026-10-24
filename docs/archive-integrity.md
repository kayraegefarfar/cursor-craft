# Source archive integrity — V0.5

## Scope

Cursor Craft's archive is **source code and documentation**, not a signed executable or an installed plugin. Its offline build and verification tools are only maintainers' convenience checks; there is no automatic installation, upload or remote action.

### Builder

`python tools/build_release.py --output ../cursor-craft-v0.5.0-alpha.zip`

- Validates the repository before creating a ZIP.
- Refuses to overwrite an existing output or symlink; choose a fresh output path.
- Uses deterministic file order, compression settings and timestamps.
- Adds `cursor-craft/SOURCE-MANIFEST.sha256`, containing SHA-256 checksums for each source file.
- Includes no generated caches or external analysis executables.

### Read-only verifier

`python tools/verify_archive.py ../cursor-craft-v0.5.0-alpha.zip`

- Rejects ZIP slip (`..`), absolute or drive paths, backslashes, duplicate/case-insensitive colliding names, Windows device names and trailing dots/spaces.
- Rejects symlinks/nonregular ZIP entries, encrypted ZIPs and files exceeding size/count bounds.
- Reads bounded data to check CRC and compares each source file to the manifest.
- Never extracts the ZIP or executes its contents.

### Threat model and residual risk

- **Detects accidental corruption and certain unsafe package layouts.** Doesn't establish publisher authenticity or trustworthiness: an attacker can tamper with both source and embedded hash manifest.
- Compare the *whole-archive* SHA-256 with a trusted release announcement, and verify the source/release origin using GitHub or another authenticated distribution channel.
- An archive can still contain harmful plain-text instructions or syntactically valid malicious source: review the source and apply runtime permission controls.
- Static checks, including CI on Windows, **do not prove Cursor itself works on Windows**. Real runtime tests remain `NOT_RUN` until independently observed.
- `morluto/rea` is an optional third-party candidate, not bundled; licenses and analyzer safety are separate concerns.
