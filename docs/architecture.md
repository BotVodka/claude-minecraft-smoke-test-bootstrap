# Architecture

## Overview

`claude-minecraft-smoke-test-bootstrap` uses a **dual-repo architecture**.

The design goal is to keep Minecraft smoke-test domain logic and Claude-side bootstrap logic separate, so each layer can evolve without duplicating responsibilities.

## Repository Roles

### Repository A: `minecraft-smoke-test-kit`

Role: **domain capability repository**

This repository is the single source of truth for Minecraft smoke-test behavior.

It owns:

- central orchestration script: `scripts/mc_smoke_test.py`
- Forge helper installer: `scripts/install_forge_smoke_test.py`
- helper templates
- marker protocol
- environment detection logic
- unsupported-environment helper-generation guidance

It does not own:

- Claude global settings distribution
- Windows-wide Claude bootstrap flow
- machine-level install steps
- public-safe Claude configuration templates

### Repository B: `claude-minecraft-smoke-test-bootstrap`

Role: **Claude-facing bootstrap / integration / distribution repository**

This repository is the public installation layer for Windows Claude Code users.

It owns:

- global command distribution
- Windows-first install flow
- public-safe settings templates
- local environment doctor flow
- integration docs for connecting Claude Code to `minecraft-smoke-test-kit`

It does not own:

- Minecraft helper source-of-truth logic
- loader-specific smoke-test implementations
- copies of the orchestration logic that should remain centralized

## Why dual-repo

A single repository would blur two very different responsibilities:

1. Minecraft smoke-test implementation
2. Claude-side installation and reuse

Keeping them separate has several benefits:

- the smoke-test kit stays domain-focused
- the bootstrap layer stays lightweight and easier to explain
- updates to orchestration logic happen in one place
- users can understand which repository they should modify
- Repository B can stay thin instead of becoming a second implementation source

## Integration Model

Repository B references Repository A through a soft dependency model.

Expected flow:

1. User clones `minecraft-smoke-test-kit`
2. User configures `MC_SMOKE_TEST_KIT_ROOT`
3. Global Claude command calls Repository A scripts through that root
4. Target project keeps only the minimum local helper files required for compilation

## Central Contract

The key cross-repo contract is:

- `MC_SMOKE_TEST_KIT_ROOT`

This environment variable points to the local clone of `minecraft-smoke-test-kit` and allows the global command layer to call:

- `MC_SMOKE_TEST_KIT_ROOT/scripts/mc_smoke_test.py`

This keeps the orchestration implementation centralized and prevents script copies from drifting across projects.

## Command Strategy

Repository B distributes thin commands.

Example:

- `commands/botvodka/mc-smoke-test.md`

These commands should:

- parse high-level user intent
- validate required environment assumptions
- call central scripts from Repository A
- fail clearly when configuration is missing

These commands should not:

- reimplement smoke-test domain logic
- guess private machine paths silently
- fork their own incompatible orchestration behavior

## Installer Strategy

The bootstrap installer is responsible for machine-level integration, not project-level domain implementation.

Installer responsibilities:

- find the Claude config directory on Windows
- ensure global command folders exist
- install public-safe commands
- guide or merge public-safe settings
- validate the existence of Repository A
- print actionable next steps

Installer non-responsibilities:

- write secrets
- overwrite unrelated user settings blindly
- embed vendored copies of Repository A

## Validation Strategy

Repository B should include a `doctor` flow to validate the local setup.

The doctor flow should check:

- Claude config directory exists
- command files exist in expected locations
- `MC_SMOKE_TEST_KIT_ROOT` is configured
- the referenced Repository A path exists
- the central script exists

## Versioning Principle

Repository A and Repository B are related but independently versioned.

That means:

- Repository A can evolve smoke-test behavior
- Repository B can evolve installation flow and docs
- integration should rely on documented contracts, not internal assumptions

## MVP Boundary

MVP intentionally targets:

- Windows
- Claude Code
- `minecraft-smoke-test-kit` integration
- verified Forge 1.20.1 helper bootstrap path

MVP intentionally avoids:

- submodules
- vendored smoke-test-kit copies
- generic workflow-framework positioning
- full multi-loader compatibility inside Repository B
