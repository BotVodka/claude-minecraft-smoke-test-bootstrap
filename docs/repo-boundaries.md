# Repository Boundaries

## Purpose

This document defines what belongs in each repository of the dual-repo setup.

It exists to prevent duplication, scope creep, and long-term drift between the Claude bootstrap layer and the Minecraft smoke-test implementation layer.

## Boundary Summary

| Repository | Owns | Does Not Own |
|---|---|---|
| `minecraft-smoke-test-kit` | smoke-test domain logic, orchestration, helper templates | Claude machine bootstrap, public-safe Claude settings distribution |
| `claude-minecraft-smoke-test-bootstrap` | Claude installation, command distribution, settings templates, doctor flow | Minecraft smoke-test source-of-truth logic, loader-specific helper implementations |

## What belongs in `minecraft-smoke-test-kit`

This repository should contain anything that defines or implements Minecraft smoke-test behavior itself.

Examples:

- `scripts/mc_smoke_test.py`
- `scripts/install_forge_smoke_test.py`
- Forge helper templates
- future NeoForge / Fabric helper templates
- marker protocol definitions
- helper-generation prompt templates
- Minecraft-facing integration documentation

### Why

These assets are domain logic. They must stay centralized so that all projects and all bootstrap layers reuse the same behavior.

## What belongs in `claude-minecraft-smoke-test-bootstrap`

This repository should contain anything that helps a Windows Claude Code user install and integrate the smoke-test kit.

Examples:

- `scripts/install.ps1`
- `scripts/bootstrap_claude_windows.py`
- `scripts/doctor.py`
- `commands/botvodka/mc-smoke-test.md`
- `commands/botvodka/doctor.md`
- `templates/claude/settings.json.template`
- Windows installation docs
- Claude integration docs

### Why

These assets are distribution and integration concerns. They are about getting the user environment ready to consume Repository A safely.

## What must not be duplicated

The following should not be independently reimplemented in both repositories:

- central orchestration logic
- marker protocol behavior
- loader detection rules
- helper installation domain logic
- project-environment support rules

If one of these changes, the source of truth should remain Repository A.

## Soft Dependency Rule

Repository B must reference Repository A instead of embedding it.

Preferred model:

- user clones both repositories
- Repository B configures `MC_SMOKE_TEST_KIT_ROOT`
- commands in Repository B call scripts in Repository A

Avoid in v1:

- git submodules
- vendored copies
- copying the full smoke-test kit into the bootstrap repository

## Public-Safe vs Local-Only Data

### Public-safe

Safe to ship in Repository B:

- command templates
- settings templates
- example paths and path conventions
- doctor checks
- installation guidance
- environment variable names such as `MC_SMOKE_TEST_KIT_ROOT`

### Local-only

Must not be committed as public defaults:

- personal API tokens
- private base URLs
- private MCP endpoints
- machine-local secret locations
- private memory data
- project-private workflow artifacts

## Decision Rule for New Files

When adding a new file, use this rule:

### Put it in Repository A if...

- it changes smoke-test execution behavior
- it changes helper generation behavior
- it changes loader-specific implementation details
- it changes the domain contract of the smoke-test system

### Put it in Repository B if...

- it helps install or configure Claude Code
- it distributes commands or templates
- it validates the user machine setup
- it explains how to connect Claude Code to Repository A

## Good / Bad Examples

### Good

- Repository A updates `mc_smoke_test.py`; Repository B keeps calling it through `MC_SMOKE_TEST_KIT_ROOT`
- Repository B adds a better Windows installer without touching smoke-test domain logic
- Repository A adds new helper-generation guidance for unsupported environments

### Bad

- Repository B copies `mc_smoke_test.py` and starts drifting from Repository A
- Repository B embeds Forge helper logic directly
- Repository A starts shipping machine-level Claude settings installation logic
- both repositories document conflicting integration contracts

## Maintenance Principle

If there is ever ambiguity, prefer the thinner Repository B and the stronger Repository A source of truth.

That keeps the architecture easier to maintain, easier to publish, and easier for outside users to understand.
