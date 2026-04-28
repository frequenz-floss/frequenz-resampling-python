# Frequenz Resampling Release Notes

## Summary

This release introduces Rust-backed Python bindings for resampling and migrates
the Python package to the `frequenz.resampling` namespace.

The project now builds via `maturin`, includes a PyO3 extension module, and has
expanded tests and CI to validate the compiled package workflow.

## Upgrading

- Update imports from `resampling` to `frequenz.resampling`.
  - Old: `from resampling import Resampler`
  - New: `from frequenz.resampling import Resampler`
- The implementation is now provided by a Rust extension module
  (`frequenz.resampling._rust_backend`) built with `maturin`.
- If you maintain tooling around docs/linting/test discovery, note that Python
  source paths now target `frequenz/` and pytest collection targets `tests/`.

## New Features

- Add Rust crate wrapper for `frequenz-resampling` using PyO3.
- Expose Python API in `frequenz.resampling` with:
  - `Resampler`
  - `resample()`
  - `ResamplingFunction`
  - `Closed`
  - `Label`
- Add type stubs for the extension module (`_rust_backend.pyi`).
- Add comprehensive Python binding tests.
- Update CI packaging flow to better support compiled distribution builds across
  environments.
- Expand repository docs (`README.md`, `AGENTS.md`) for the new architecture.

## Build Changes

- Switch from a single abi3-compatible wheel to per-Python-version wheels
  (`cp311`, `cp312`, `cp313`, `cp314`). This removes the `abi3-py311` PyO3
  feature so each supported Python version gets its own compiled wheel.

## Bug Fixes

- Fix docs and tooling source path assumptions from `src/` to `frequenz/` for
  mkdocs/mkdocstrings and related generation scripts.
- Apply formatting and cleanup updates around the new bindings and tests.
