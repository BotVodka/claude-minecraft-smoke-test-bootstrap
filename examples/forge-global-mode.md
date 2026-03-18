# Forge Global Mode Example

## Purpose

This example shows the intended cross-project workflow when using the global Claude bootstrap layer with a verified Forge 1.20.1 project.

## Assumptions

- `claude-minecraft-smoke-test-bootstrap` has been installed into Claude
- `minecraft-smoke-test-kit` exists locally
- `MC_SMOKE_TEST_KIT_ROOT` points to that clone
- target project is a verified Forge 1.20.1 project

## Recommended flow

### 1. Verify the local environment

```text
/botvodka:doctor
```

### 2. Bootstrap the project if needed

```text
/botvodka:bootstrap-project --project-root "D:/path/to/your-project"
```

### 3. Run the smoke test

```text
/botvodka:mc-smoke-test server --project-root "D:/path/to/your-project"
/botvodka:mc-smoke-test client --project-root "D:/path/to/your-project"
```

## Under the hood

The global command layer should call the central script:

```text
MC_SMOKE_TEST_KIT_ROOT/scripts/mc_smoke_test.py
```

For the current verified path, helper bootstrap is handled by Repository A and the target project only keeps the minimum helper Java files required for compilation.

## Why this example matters

This example makes the repository intent clear:

- Repository B installs and guides the Claude-side workflow
- Repository A remains the source of truth for smoke-test behavior
- target projects keep minimal local smoke-test code
