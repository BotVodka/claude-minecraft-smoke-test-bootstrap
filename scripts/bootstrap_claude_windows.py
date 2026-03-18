#!/usr/bin/env python3
"""Bootstrap Claude Code integration for minecraft-smoke-test-kit on Windows."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from common import (
    CENTRAL_SCRIPT_RELATIVE_PATH,
    build_settings_payload,
    command_source_dir,
    command_target_dir,
    default_claude_dir,
    detect_default_kit_root,
    load_json_object,
    repo_root,
    settings_path_for,
    sync_command_files,
    write_json_object,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install public-safe Claude bootstrap assets for minecraft smoke-test reuse.",
    )
    parser.add_argument(
        "--claude-dir",
        help="Claude config directory. Defaults to ~/.claude.",
    )
    parser.add_argument(
        "--kit-root",
        help="Path to the local minecraft-smoke-test-kit clone.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview actions without writing files.",
    )
    return parser.parse_args()


def resolve_claude_dir(args: argparse.Namespace) -> Path:
    if args.claude_dir:
        return Path(args.claude_dir).expanduser().resolve()
    return default_claude_dir().resolve()


def resolve_kit_root(args: argparse.Namespace, root: Path, existing_settings: dict[str, object]) -> tuple[Path, str]:
    env = existing_settings.get("env")
    if env is not None and not isinstance(env, dict):
        raise SystemExit("Invalid Claude settings: 'env' must be a JSON object.")

    if args.kit_root:
        kit_root = Path(args.kit_root).expanduser().resolve()
        source = "argument"
    elif isinstance(env, dict) and env.get("MC_SMOKE_TEST_KIT_ROOT"):
        kit_root = Path(str(env["MC_SMOKE_TEST_KIT_ROOT"])).expanduser().resolve()
        source = "existing settings"
    else:
        detected = detect_default_kit_root(root)
        if detected is None:
            raise SystemExit(
                "Unable to determine MC_SMOKE_TEST_KIT_ROOT. Pass --kit-root or clone minecraft-smoke-test-kit next to this repository."
            )
        kit_root = detected
        source = "auto-detected sibling repo"

    if not kit_root.exists():
        raise SystemExit(f"minecraft-smoke-test-kit path does not exist: {kit_root}")

    central_script = kit_root / CENTRAL_SCRIPT_RELATIVE_PATH
    if not central_script.exists():
        raise SystemExit(f"Central smoke-test script not found: {central_script}")

    return kit_root, source


def load_existing_settings(settings_path: Path) -> dict[str, object]:
    if not settings_path.exists():
        return {}
    try:
        return load_json_object(settings_path)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in Claude settings: {settings_path} ({exc})") from exc
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc


def install_commands(root: Path, claude_dir: Path, dry_run: bool) -> tuple[int, int, int]:
    source_dir = command_source_dir(root)
    target_dir = command_target_dir(claude_dir)

    if dry_run:
        installed = 0
        updated = 0
        unchanged = 0
        for source in sorted(source_dir.glob("*.md")):
            target = target_dir / source.name
            if not target.exists():
                installed += 1
                continue
            existing = target.read_text(encoding="utf-8")
            if existing == source.read_text(encoding="utf-8"):
                unchanged += 1
            else:
                updated += 1
        return installed, updated, unchanged

    result = sync_command_files(source_dir, target_dir)
    return len(result.installed), len(result.updated), len(result.unchanged)


def write_settings(settings_path: Path, payload: dict[str, object], dry_run: bool) -> str:
    if dry_run:
        if settings_path.exists():
            existing = settings_path.read_text(encoding="utf-8")
            next_content = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
            return "updated" if existing != next_content else "unchanged"
        return "created"

    next_content = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if settings_path.exists():
        existing = settings_path.read_text(encoding="utf-8")
        if existing == next_content:
            return "unchanged"
        backup_path = settings_path.with_name("settings.json.bak")
        shutil.copy2(settings_path, backup_path)
        write_json_object(settings_path, payload)
        return "updated"

    write_json_object(settings_path, payload)
    return "created"


def main() -> int:
    args = parse_args()
    root = repo_root()
    claude_dir = resolve_claude_dir(args)
    settings_path = settings_path_for(claude_dir)

    claude_dir.mkdir(parents=True, exist_ok=True)
    existing_settings = load_existing_settings(settings_path)
    kit_root, kit_root_source = resolve_kit_root(args, root, existing_settings)

    installed_count, updated_count, unchanged_count = install_commands(root, claude_dir, args.dry_run)
    next_settings = build_settings_payload(existing_settings, kit_root, root)
    settings_action = write_settings(settings_path, next_settings, args.dry_run)

    print("## Bootstrap Result")
    print(f"- Repo Root: {root.as_posix()}")
    print(f"- Claude Dir: {claude_dir.as_posix()}")
    print(f"- MC_SMOKE_TEST_KIT_ROOT: {kit_root.as_posix()}")
    print(f"- Kit Root Source: {kit_root_source}")
    print(f"- Commands Installed: {installed_count}")
    print(f"- Commands Updated: {updated_count}")
    print(f"- Commands Unchanged: {unchanged_count}")
    print(f"- Settings Action: {settings_action}")
    print(f"- Dry Run: {'true' if args.dry_run else 'false'}")
    print()
    print("### Next Steps")
    print(f'- Run doctor: python3 "{(root / "scripts" / "doctor.py").as_posix()}"')
    print('- Use /botvodka:mc-smoke-test in a supported Minecraft project.')
    return 0


if __name__ == "__main__":
    sys.exit(main())
