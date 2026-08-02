# Changelog

All notable changes to this project are documented in this file.

## [0.6.0] - 2026-08-02

### Changed

- **Dropped support for Python 3.8 and 3.9.** The minimum supported version is now Python 3.10.
- Added Python 3.13 and 3.14 to the supported versions (3.10 - 3.14).
- Migrated packaging and dependency management from Poetry to [uv](https://docs.astral.sh/uv/),
  using the `uv_build` backend. Nothing changes for consumers installing from PyPI.
- Replaced `black` and `pylama` with [ruff](https://docs.astral.sh/ruff/) for formatting and
  linting. Source files were reformatted accordingly (no behaviour change).

### Added

- `py.typed` marker, so type checkers now pick up the inline type annotations shipped with the
  package ([#85](https://github.com/nornir-automation/nornir_napalm/pull/85)).

### Fixed

- Refreshed the CI workflows, `Makefile` and `Dockerfile` to build and test against the current
  Python versions.
- Numerous transitive development dependency bumps.

[0.6.0]: https://github.com/nornir-automation/nornir_napalm/compare/v0.5.0...v0.6.0
