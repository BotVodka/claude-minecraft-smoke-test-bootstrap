# Windows Installation

## Goal

Set up a Windows Claude Code environment so that global Minecraft smoke-test commands can call `minecraft-smoke-test-kit` as the central source of truth.

## Prerequisites

- Windows machine
- Claude Code installed
- Python 3 available in PATH
- local clone of `minecraft-smoke-test-kit`

## Installation Steps

### 1. Clone Repository B

```bash
git clone https://github.com/BotVodka/claude-minecraft-smoke-test-bootstrap.git
```

### 2. Clone Repository A

```bash
git clone https://github.com/BotVodka/minecraft-smoke-test-kit.git
```

### 3. Run the installer entrypoint

Default install:

```powershell
./scripts/install.ps1
```

Explicit kit root:

```powershell
./scripts/install.ps1 --kit-root "D:/projects/code/minecraft-smoke-test-kit"
```

Dry-run preview:

```powershell
./scripts/install.ps1 --dry-run
```

## What the installer currently does

`install.ps1` calls `bootstrap_claude_windows.py`.

The Python bootstrap script currently:

- detects the Claude config directory
- creates the Claude directory if needed
- installs or updates `commands/botvodka/*.md`
- loads existing `settings.json` if present
- merges the public-safe settings template
- writes `env.MC_SMOKE_TEST_KIT_ROOT`
- creates `settings.json.bak` before overwriting an existing settings file

## Kit root resolution order

The installer resolves `MC_SMOKE_TEST_KIT_ROOT` in this order:

1. `--kit-root`
2. existing `settings.json` value
3. auto-detected sibling repository at `../minecraft-smoke-test-kit`

If no valid path can be resolved, the installer fails loudly with a repair hint.

## Validate with doctor

Run:

```bash
python3 ./scripts/doctor.py
```

Optional override:

```bash
python3 ./scripts/doctor.py --kit-root "D:/projects/code/minecraft-smoke-test-kit"
```

The doctor flow currently checks:

- Claude config directory exists
- `settings.json` exists and contains valid JSON
- `MC_SMOKE_TEST_KIT_ROOT` is configured
- `commands/botvodka/` exists
- expected botvodka command files exist
- referenced `minecraft-smoke-test-kit` root exists
- central script exists
- Forge helper installer exists

## Installed Commands

After installation, the user should have:

```text
/botvodka:mc-smoke-test
/botvodka:doctor
/botvodka:bootstrap-project
```

Recommended first checks:

```text
/botvodka:doctor
/botvodka:mc-smoke-test server
```

## First Use

After installation, the user should be able to invoke:

```text
/botvodka:mc-smoke-test server
/botvodka:mc-smoke-test client
/botvodka:mc-smoke-test both
```

## Safety Notes

Do not commit as defaults:

- private API tokens
- private MCP endpoints
- machine-local secret paths
- private memory files

Only public-safe path contracts and templates should be distributed.
