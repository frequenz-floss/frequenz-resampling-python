# Frequenz Resampling Release Notes

## Summary

<!-- Here goes a general summary of what this release is about -->

## Upgrading

<!-- Here goes notes on how to upgrade from previous versions, including deprecations and what they should be replaced with -->

## New Features

<!-- Here goes the main new features and examples or instructions on how to use them -->

## Bug Fixes

<!-- Here goes notable bug fixes that are worth a special mention or explanation -->

## Tooling

* Restored security hardening to GitHub Actions workflows: hash-pinned all
  actions, re-added workflow-level `permissions: contents: read`, restored
  `python -I` isolated mode on Python invocations, re-added `permissions: {}`
  on gate jobs, and fixed shell injection risks in `mike` and release steps.
