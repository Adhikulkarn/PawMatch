"""
API Versioning Strategy

Scheme:
    URL path versioning (e.g. /api/v1/, /api/v2/).

Rules:
    - Breaking changes require a new version number.
    - Existing versions are never modified in a breaking way.
    - Multiple versions may coexist at the same time.

Deprecation:
    - A version is marked deprecated in release notes.
    - A deprecated version remains available for a minimum of 6 months.
    - After the deprecation window the version is removed in a major release.

Backward Compatibility:
    - Adding new fields/endpoints is NOT a breaking change.
    - Renaming/removing fields, changing response types, or altering
      endpoint semantics IS a breaking change.

Sunset Policy:
    - Announce deprecation at least 6 months before removal.
    - Emit a Sunset header on deprecated versions.
    - Redirect documentation to the current version.
"""
