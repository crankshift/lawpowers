#!/usr/bin/env python3
"""Validate generated Codex custom-agent files."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def plugin_codex_name(plugin_dir: Path) -> str:
    return json.loads((plugin_dir / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))["name"]


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_generated_toml(path: Path) -> dict[str, str]:
    """Parse the small TOML subset emitted by convert-agents-to-codex.py."""
    lines = path.read_text(encoding="utf-8").splitlines()
    data: dict[str, str] = {}
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            fail(f"{path} has unparsable line: {line!r}")
        key, raw_value = [part.strip() for part in line.split("=", 1)]
        if raw_value == '"""':
            value_lines: list[str] = []
            while i < len(lines):
                if lines[i] == '"""':
                    i += 1
                    break
                value_lines.append(lines[i])
                i += 1
            else:
                fail(f"{path} has unterminated multiline value for `{key}`")
            data[key] = "\n".join(value_lines)
            continue
        try:
            data[key] = json.loads(raw_value)
        except json.JSONDecodeError as exc:
            fail(f"{path} has invalid string value for `{key}`: {exc}")
    return data


def main() -> None:
    seen_names: set[str] = set()
    source_count = 0
    generated_count = 0

    for plugin_dir in sorted((ROOT / "plugins").iterdir()):
        if not plugin_dir.is_dir():
            continue
        agents_dir = plugin_dir / "agents"
        if not agents_dir.is_dir():
            continue
        plugin_name = plugin_codex_name(plugin_dir)
        output_dir = plugin_dir / ".codex" / "agents"
        if not output_dir.is_dir():
            fail(f"missing generated agent directory: {output_dir}")

        for source in sorted(agents_dir.glob("*.md")):
            source_count += 1
            expected_name = f"{plugin_name}-{source.stem}"
            generated = output_dir / f"{expected_name}.toml"
            if not generated.is_file():
                fail(f"missing generated agent for {source}: {generated}")
            generated_count += 1
            text = generated.read_text(encoding="utf-8")
            data = parse_generated_toml(generated)
            for key in ("name", "description", "developer_instructions"):
                if not str(data.get(key, "")).strip():
                    fail(f"{generated} missing non-empty `{key}`")
            if data["name"] != expected_name:
                fail(f"{generated} has name {data['name']!r}; expected {expected_name!r}")
            if data["name"] in seen_names:
                fail(f"duplicate generated agent name: {data['name']}")
            seen_names.add(data["name"])
            if "[TODO" in text:
                fail(f"placeholder found in {generated}")

        extra = sorted(output_dir.glob("*.toml"))
        expected = {f"{plugin_name}-{source.stem}.toml" for source in agents_dir.glob("*.md")}
        for generated in extra:
            if generated.name not in expected:
                fail(f"stale generated agent file: {generated}")

    if source_count != generated_count:
        fail(f"source/generated count mismatch: {source_count}/{generated_count}")
    print(f"Validated {generated_count} Codex agent files.")


if __name__ == "__main__":
    main()
