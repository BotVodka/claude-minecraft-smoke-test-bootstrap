# Smoke-Test Integration

## Purpose

This document explains how `claude-minecraft-smoke-test-bootstrap` integrates with `minecraft-smoke-test-kit`.

## Integration Contract

The integration contract is intentionally small:

- user has a local clone of `minecraft-smoke-test-kit`
- Claude settings define `MC_SMOKE_TEST_KIT_ROOT`
- global commands call the central script from that root

Central script path:

```text
MC_SMOKE_TEST_KIT_ROOT/scripts/mc_smoke_test.py
```

## Execution Model

### Global command layer

Repository B distributes the Claude-facing command entrypoints:

- `commands/botvodka/mc-smoke-test.md`
- `commands/botvodka/doctor.md`
- `commands/botvodka/bootstrap-project.md`

This layer should remain thin.

### Central orchestration layer

Repository A owns the actual smoke-test logic:

- environment inspection
- helper detection
- verified Forge 1.20.1 bootstrap path
- marker watching
- controlled shutdown
- structured result summaries

## Target Project Model

A target project should keep only the minimum local code that must compile inside that project.

For the current verified path, that mainly means helper Java files.

The global layer should not require each project to keep its own copied orchestration script when central execution is available.

## Verified Path

Current verified path:

- Forge
- Minecraft 1.20.1
- helper bootstrap via `install_forge_smoke_test.py --global-mode`

## Unsupported Path

For unsupported environments:

- do not blindly reuse the verified Forge helper templates
- follow the helper-generation guidance maintained in Repository A
- keep the marker contract stable while adapting loader-specific code locally

## Design Rule

Repository B helps users reach Repository A safely.

It should not become a second source of truth for smoke-test behavior.
