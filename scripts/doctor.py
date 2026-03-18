#!/usr/bin/env python3
"""Validate Claude Code bootstrap integration for minecraft smoke-test reuse."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from common import (
    CENTRAL_SCRIPT_RELATIVE_PATH,
    INSTALLER_SCRIPT_RELATIVE_PATH,
    command_target_dir,
    default_claude_dir,
    expected_command_names,
    load_json_object,
    repo_root,
    settings_path_for,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Claude bootstrap setup for minecraft smoke-test reuse.",
    )
    parser.add_argument(
        "--claude-dir",
        help="Claude config directory. Defaults to ~/.claude.",
    )
    parser.add_argument(
        "--kit-root",
        help="Override minecraft-smoke-test-kit path for validation.",
    )
    return parser.parse_args()


def resolve_claude_dir(args: argparse.Namespace) -> Path:
    if args.claude_dir:
        return Path(args.claude_dir).expanduser().resolve()
    return default_claude_dir().resolve()


def load_settings(settings_path: Path) -> dict[str, object] | None:
    if not settings_path.exists():
        return None
    try:
        return load_json_object(settings_path)
    except json.JSONDecodeError:
        return {"__invalid_json__": True}
    except ValueError:
        return {"__invalid_json__": True}


def print_check(name: str, passed: bool, detail: str, fix: str | None = None) -> None:
    status = "OK" if passed else "FAIL"
    print(f"- [{status}] {name}: {detail}")
    if not passed and fix:
        print(f"  fix: {fix}")


def main() -> int:
    args = parse_args()
    root = repo_root()
    claude_dir = resolve_claude_dir(args)
    settings_path = settings_path_for(claude_dir)
    settings = load_settings(settings_path)
    expected_commands = expected_command_names(root)
    command_dir = command_target_dir(claude_dir)

    failures = 0

    print("## Doctor Report")
    print(f"- Repo Root: {root.as_posix()}")
    print(f"- Claude Dir: {claude_dir.as_posix()}")
    print()

    claude_dir_exists = claude_dir.exists()
    print_check(
        "Claude config directory",
        claude_dir_exists,
        claude_dir.as_posix() if claude_dir_exists else "missing",
        f'Run the bootstrap installer or create: {claude_dir.as_posix()}',
    )
    failures += 0 if claude_dir_exists else 1

    settings_exists = settings is not None
    settings_valid = settings_exists and "__invalid_json__" not in settings
    print_check(
        "Claude settings.json",
        settings_valid,
        settings_path.as_posix() if settings_valid else ("invalid JSON" if settings_exists else "missing"),
        f'Fix or recreate: {settings_path.as_posix()}',
    )
    failures += 0 if settings_valid else 1

    configured_kit_root: str | None = None
    if settings_valid and settings is not None:
        env = settings.get("env")
        if isinstance(env, dict) and env.get("MC_SMOKE_TEST_KIT_ROOT"):
            configured_kit_root = str(env["MC_SMOKE_TEST_KIT_ROOT"])

    effective_kit_root = Path(args.kit_root).expanduser().resolve() if args.kit_root else (Path(configured_kit_root).expanduser().resolve() if configured_kit_root else None)

    print_check(
        "MC_SMOKE_TEST_KIT_ROOT",
        effective_kit_root is not None,
        effective_kit_root.as_posix() if effective_kit_root else "missing",
        "Configure env.MC_SMOKE_TEST_KIT_ROOT in Claude settings or pass --kit-root.",
    )
    failures += 0 if effective_kit_root is not None else 1

    command_dir_exists = command_dir.exists()
    print_check(
        "Command directory",
        command_dir_exists,
        command_dir.as_posix() if command_dir_exists else "missing",
        f'Install commands into: {command_dir.as_posix()}',
    )
    failures += 0 if command_dir_exists else 1

    for command_name in expected_commands:
        command_path = command_dir / command_name
        command_exists = command_path.exists()
        print_check(
            f"Command {command_name}",
            command_exists,
            command_path.as_posix() if command_exists else "missing",
            f'Install command file: {command_path.as_posix()}',
        )
        failures += 0 if command_exists else 1

    if effective_kit_root is not None:
        kit_root_exists = effective_kit_root.exists()
        print_check(
            "minecraft-smoke-test-kit root",
            kit_root_exists,
            effective_kit_root.as_posix() if kit_root_exists else "missing",
            "Clone minecraft-smoke-test-kit locally or update MC_SMOKE_TEST_KIT_ROOT.",
        )
        failures += 0 if kit_root_exists else 1

        central_script = effective_kit_root / CENTRAL_SCRIPT_RELATIVE_PATH
        central_script_exists = central_script.exists()
        print_check(
            "Central smoke-test script",
            central_script_exists,
            central_script.as_posix() if central_script_exists else "missing",
            f'Ensure this file exists: {central_script.as_posix()}',
        )
        failures += 0 if central_script_exists else 1

        installer_script = effective_kit_root / INSTALLER_SCRIPT_RELATIVE_PATH
        installer_script_exists = installer_script.exists()
        print_check(
            "Forge helper installer",
            installer_script_exists,
            installer_script.as_posix() if installer_script_exists else "missing",
            f'Ensure this file exists: {installer_script.as_posix()}',
        )
        failures += 0 if installer_script_exists else 1

    print()
    if failures:
        print(f"Doctor result: FAILED ({failures} issue(s))")
        return 1

    print("Doctor result: PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
