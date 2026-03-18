#!/usr/bin/env python3
"""Shared helpers for claude-minecraft-smoke-test-bootstrap scripts."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SETTINGS_SCHEMA_URL = "https://json.schemastore.org/claude-code-settings.json"
COMMAND_NAMESPACE = "botvodka"
CENTRAL_SCRIPT_RELATIVE_PATH = Path("scripts") / "mc_smoke_test.py"
INSTALLER_SCRIPT_RELATIVE_PATH = Path("scripts") / "install_forge_smoke_test.py"


@dataclass(frozen=True)
class CommandSyncResult:
    installed: tuple[Path, ...]
    updated: tuple[Path, ...]
    unchanged: tuple[Path, ...]


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def default_claude_dir() -> Path:
    return Path.home() / ".claude"


def settings_path_for(claude_dir: Path) -> Path:
    return claude_dir / "settings.json"


def command_source_dir(root: Path | None = None) -> Path:
    actual_root = root or repo_root()
    return actual_root / "commands" / COMMAND_NAMESPACE


def command_target_dir(claude_dir: Path) -> Path:
    return claude_dir / "commands" / COMMAND_NAMESPACE


def expected_command_names(root: Path | None = None) -> tuple[str, ...]:
    source_dir = command_source_dir(root)
    return tuple(sorted(path.name for path in source_dir.glob("*.md")))


def detect_default_kit_root(root: Path | None = None) -> Path | None:
    actual_root = root or repo_root()
    candidate = actual_root.parent / "minecraft-smoke-test-kit"
    if candidate.exists():
        return candidate.resolve()
    return None


def ensure_object(value: Any, field_name: str) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValueError(f"Expected '{field_name}' to be a JSON object.")
    return dict(value)


def load_json_object(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"Expected JSON object at: {path}")
    return dict(raw)


def write_json_object(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def normalize_path_string(path: Path) -> str:
    return path.resolve().as_posix()


def settings_template(root: Path | None = None) -> dict[str, Any]:
    actual_root = root or repo_root()
    template_path = actual_root / "templates" / "claude" / "settings.json.template"
    return load_json_object(template_path)


def build_settings_payload(existing: dict[str, Any], kit_root: Path, root: Path | None = None) -> dict[str, Any]:
    template = settings_template(root)
    payload = dict(existing)
    payload.setdefault("$schema", SETTINGS_SCHEMA_URL)

    template_env = ensure_object(template.get("env"), "env")
    current_env = ensure_object(payload.get("env"), "env")

    for key, value in template_env.items():
        current_env.setdefault(key, value)

    current_env["MC_SMOKE_TEST_KIT_ROOT"] = normalize_path_string(kit_root)
    payload["env"] = current_env
    return payload


def sync_command_files(source_dir: Path, target_dir: Path) -> CommandSyncResult:
    installed: list[Path] = []
    updated: list[Path] = []
    unchanged: list[Path] = []

    target_dir.mkdir(parents=True, exist_ok=True)

    for source in sorted(source_dir.glob("*.md")):
        target = target_dir / source.name
        content = source.read_text(encoding="utf-8")
        if not target.exists():
            target.write_text(content, encoding="utf-8", newline="\n")
            installed.append(target)
            continue

        existing = target.read_text(encoding="utf-8")
        if existing == content:
            unchanged.append(target)
            continue

        target.write_text(content, encoding="utf-8", newline="\n")
        updated.append(target)

    return CommandSyncResult(
        installed=tuple(installed),
        updated=tuple(updated),
        unchanged=tuple(unchanged),
    )
