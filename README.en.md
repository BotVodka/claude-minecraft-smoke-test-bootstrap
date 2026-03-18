# Claude Minecraft Smoke-Test Bootstrap

This project was written by BotVodka using Claude Code and GPT-5.4.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![README: 中文](https://img.shields.io/badge/README-%E4%B8%AD%E6%96%87-blue.svg)](./README.md)
[![README: English](https://img.shields.io/badge/README-English-blue.svg)](./README.en.md)

A bootstrap repository for Windows Claude Code users who want reusable Minecraft smoke-test integration.

Its purpose is not to reimplement `minecraft-smoke-test-kit`, but to package the **global Claude command distribution, Windows installation flow, public-safe settings templates, and environment doctor flow** into a reusable public entrypoint.

## What problem this repository solves

`minecraft-smoke-test-kit` already provides the central orchestration script, Forge helper installer, templates, and integration docs. But a new Windows Claude Code user still faces repeated setup work:

- where global Claude commands should live
- how `MC_SMOKE_TEST_KIT_ROOT` should be configured
- which configuration is safe to publish and which is not
- how to install public repository assets into a local Claude environment
- how to verify that the local integration is working

This repository solves those **bootstrap / integration / distribution** problems.

## Dual-repo structure

### Repository A: `minecraft-smoke-test-kit`

Owns the Minecraft smoke-test domain capabilities:

- `scripts/mc_smoke_test.py`
- `scripts/install_forge_smoke_test.py`
- Forge helper templates
- future NeoForge / Fabric templates or helper-generation rules
- Minecraft smoke-test domain docs

### Repository B: `claude-minecraft-smoke-test-bootstrap`

Owns the Claude-side installation and integration layer:

- Windows-first bootstrap
- global Claude command distribution
- public-safe settings templates
- installation and integration docs
- local doctor / validation flow

> Boundary: this repository is not a generic workflow framework and not a replacement for `minecraft-smoke-test-kit`.

## Implemented MVP capabilities

This repository currently provides:

- `scripts/install.ps1`
  - Windows installer entrypoint
  - auto-detects Python 3 and forwards arguments to the Python bootstrap script
- `scripts/bootstrap_claude_windows.py`
  - detects the Claude config directory
  - installs or updates `commands/botvodka/*.md`
  - merges the public-safe settings template
  - sets `MC_SMOKE_TEST_KIT_ROOT`
  - supports `--dry-run`
- `scripts/doctor.py`
  - checks the Claude config directory
  - checks `settings.json`
  - checks `MC_SMOKE_TEST_KIT_ROOT`
  - checks botvodka command installation
  - checks the central smoke-test script and Forge helper installer

## Quick start

### 1. Clone both repositories

```bash
git clone https://github.com/BotVodka/claude-minecraft-smoke-test-bootstrap.git
git clone https://github.com/BotVodka/minecraft-smoke-test-kit.git
```

### 2. Run the bootstrap installer

Default install:

```powershell
./scripts/install.ps1
```

Explicit smoke-test kit path:

```powershell
./scripts/install.ps1 --kit-root "D:/projects/code/minecraft-smoke-test-kit"
```

Preview only, no file writes:

```powershell
./scripts/install.ps1 --dry-run
```

### 3. Run doctor

```bash
python3 ./scripts/doctor.py
```

Optional override:

```bash
python3 ./scripts/doctor.py --kit-root "D:/projects/code/minecraft-smoke-test-kit"
```

## Installation behavior

The bootstrap script resolves `MC_SMOKE_TEST_KIT_ROOT` in this order:

1. `--kit-root`
2. existing `env.MC_SMOKE_TEST_KIT_ROOT` in `settings.json`
3. sibling repository at `../minecraft-smoke-test-kit`

The installer will:

- detect and create the Claude config directory
- install or update `commands/botvodka/*.md`
- merge `templates/claude/settings.json.template`
- write `env.MC_SMOKE_TEST_KIT_ROOT`
- create `settings.json.bak` before overwriting an existing `settings.json`

The installer will not:

- write private tokens
- write private MCP endpoints
- silently guess a non-existent kit path
- duplicate smoke-test domain logic from `minecraft-smoke-test-kit`

## Installed commands

After installation, the user should have:

```text
/botvodka:mc-smoke-test
/botvodka:doctor
/botvodka:bootstrap-project
```

Responsibilities:

- `/botvodka:mc-smoke-test`
  - runs `server` / `client` / `both` smoke tests through the central script
- `/botvodka:doctor`
  - checks Claude config, command install state, and `MC_SMOKE_TEST_KIT_ROOT`
- `/botvodka:bootstrap-project`
  - guides helper integration for a target Minecraft project

## Intended usage

In a supported Minecraft project, the user should be able to run:

```text
/botvodka:mc-smoke-test server
/botvodka:mc-smoke-test client
/botvodka:mc-smoke-test both
```

The command calls:

- `MC_SMOKE_TEST_KIT_ROOT/scripts/mc_smoke_test.py`

and can bootstrap helpers on demand for the verified Forge 1.20.1 path.

## Configuration boundaries

### Safe to distribute publicly

- command templates
- `settings.json.template`
- path-style env contracts such as `MC_SMOKE_TEST_KIT_ROOT`
- Windows-first installation scripts
- doctor / validation scripts

### Must not be published as defaults

- API tokens
- private MCP endpoints
- private base URLs
- machine-local secret paths
- private memory content
- project-private automation data

## Documentation index

- `docs/architecture.md`
- `docs/repo-boundaries.md`
- `docs/windows-installation.md`
- `docs/smoke-test-integration.md`

## Current MVP scope

Currently prioritized and supported:

- Windows
- Claude Code
- `minecraft-smoke-test-kit` integration
- verified Forge 1.20.1 helper bootstrap path

Explicitly out of scope for this repository:

- all-loader / all-version compatibility implementation
- macOS / Linux install flows
- publishing a full private local environment
- a generic plugin system

## Design principles

- **KISS**: the bootstrap layer only installs, integrates, and validates
- **DRY**: central smoke-test logic remains in `minecraft-smoke-test-kit`
- **YAGNI**: v1 focuses on Windows Claude Code + Minecraft smoke-test reuse
- **SOLID**: commands, installer, doctor, and domain scripts keep separate responsibilities

## License

MIT
