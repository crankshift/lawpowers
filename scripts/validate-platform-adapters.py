#!/usr/bin/env python3
"""Validate generated lawpowers platform adapter files."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JURISDICTIONS = ("pl", "ua")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.S)
EXPECTED_PACKAGE_JSON = {
    "name": "lawpowers",
    "version": "0.7.0",
    "type": "module",
    "main": ".opencode/plugins/lawpowers.js",
}


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read(path: Path) -> str:
    if not path.is_file():
        fail(f"missing required file: {rel(path)}")
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str, path: Path) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        fail(f"{rel(path)} is missing YAML frontmatter")
    raw, body = match.groups()
    values: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.startswith(" "):
            continue
        key, sep, value = line.partition(":")
        if not sep:
            fail(f"{rel(path)} has unparsable frontmatter line: {line!r}")
        values[key.strip()] = value.strip().strip('"')
    return values, body


def plugin_codex_name(jurisdiction: str) -> str:
    manifest = ROOT / "plugins" / jurisdiction / ".codex-plugin" / "plugin.json"
    return json.loads(read(manifest))["name"]


def prefixed_name(jurisdiction: str, name: str) -> str:
    plugin_name = plugin_codex_name(jurisdiction)
    return name if name.startswith(f"{plugin_name}-") else f"{plugin_name}-{name}"


def source_agent_paths(jurisdiction: str) -> list[Path]:
    source_dir = ROOT / "agents" / jurisdiction
    if not source_dir.is_dir():
        fail(f"missing canonical agent directory: {rel(source_dir)}")
    return sorted(source_dir.glob("*.md"))


def source_skill_dirs(jurisdiction: str) -> list[Path]:
    source_dir = ROOT / "skills" / jurisdiction
    if not source_dir.is_dir():
        fail(f"missing canonical skill directory: {rel(source_dir)}")
    return sorted(path for path in source_dir.iterdir() if (path / "SKILL.md").is_file())


def canonical_names(jurisdiction: str) -> set[str]:
    return {path.stem for path in source_agent_paths(jurisdiction)} | {path.name for path in source_skill_dirs(jurisdiction)}


def unprefixed_canonical_names(jurisdiction: str) -> set[str]:
    plugin_name = plugin_codex_name(jurisdiction)
    names: set[str] = set()
    for name in canonical_names(jurisdiction):
        if name.startswith(f"{plugin_name}-"):
            names.add(name.removeprefix(f"{plugin_name}-"))
    return names


def rewrite_plugin_agent_skill_links(text: str, jurisdiction: str) -> str:
    return re.sub(
        rf"\.\./\.\./skills/{re.escape(jurisdiction)}/([A-Za-z0-9_-]+)/SKILL\.md",
        r"../skills/\1/SKILL.md",
        text,
    )


def require_prefixed_canonical_sources(jurisdiction: str) -> None:
    plugin_name = plugin_codex_name(jurisdiction)
    for source in source_agent_paths(jurisdiction):
        if not source.stem.startswith(f"{plugin_name}-"):
            fail(f"canonical agent is not prefixed: {rel(source)}")
        metadata, _ = parse_frontmatter(read(source), source)
        if metadata.get("name") != source.stem:
            fail(f"{rel(source)} name is {metadata.get('name')!r}; expected {source.stem!r}")
    for source_dir in source_skill_dirs(jurisdiction):
        if not source_dir.name.startswith(f"{plugin_name}-"):
            fail(f"canonical skill directory is not prefixed: {rel(source_dir)}")
        source = source_dir / "SKILL.md"
        metadata, _ = parse_frontmatter(read(source), source)
        if metadata.get("name") != source_dir.name:
            fail(f"{rel(source)} name is {metadata.get('name')!r}; expected {source_dir.name!r}")


def require_no_bare_same_jurisdiction_names(text: str, generated: Path, jurisdiction: str, plugin_name: str) -> None:
    stale_reference = re.search(rf"\b{re.escape(jurisdiction)}:[A-Za-z0-9_-]+", text)
    if stale_reference:
        fail(f"{rel(generated)} contains stale same-jurisdiction reference {stale_reference.group(0)!r}")
    for name in sorted(unprefixed_canonical_names(jurisdiction)):
        pattern = re.compile(rf"(?<![A-Za-z0-9_-])(?<!{re.escape(plugin_name)}-){re.escape(name)}(?![A-Za-z0-9_-])")
        if pattern.search(text):
            fail(f"{rel(generated)} contains unprefixed same-jurisdiction canonical name {name!r}")


def parse_generated_toml(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in read(path).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, sep, raw_value = line.partition("=")
        if not sep:
            fail(f"{rel(path)} has unparsable line: {line!r}")
        try:
            data[key.strip()] = json.loads(raw_value.strip())
        except json.JSONDecodeError as exc:
            fail(f"{rel(path)} has invalid string value for `{key.strip()}`: {exc}")
    return data


def opencode_source_body(body: str) -> str:
    parts = body.lstrip("\n").split("\n\n", 1)
    return parts[1] if len(parts) == 2 else body


def codex_source_body(body: str) -> str:
    return body.split("\n\n## Codex migration notes", 1)[0]


def require_exact_file_set(directory: Path, expected_names: set[str], pattern: str) -> None:
    if not directory.is_dir():
        fail(f"missing generated directory: {rel(directory)}")
    actual_names = {path.name for path in directory.glob(pattern)}
    missing = sorted(expected_names - actual_names)
    extra = sorted(actual_names - expected_names)
    if missing:
        fail(f"{rel(directory)} is missing generated files: {', '.join(missing)}")
    if extra:
        fail(f"{rel(directory)} has stale generated files: {', '.join(extra)}")


def require_exact_dir_set(directory: Path, expected_names: set[str]) -> None:
    if not directory.is_dir():
        fail(f"missing generated directory: {rel(directory)}")
    actual_names = {path.name for path in directory.iterdir() if path.is_dir()}
    missing = sorted(expected_names - actual_names)
    extra = sorted(actual_names - expected_names)
    if missing:
        fail(f"{rel(directory)} is missing generated directories: {', '.join(missing)}")
    if extra:
        fail(f"{rel(directory)} has stale generated directories: {', '.join(extra)}")


def validate_claude_copies(jurisdiction: str) -> tuple[int, int]:
    agent_sources = source_agent_paths(jurisdiction)
    skill_sources = source_skill_dirs(jurisdiction)
    plugin_dir = ROOT / "plugins" / jurisdiction
    plugin_name = plugin_codex_name(jurisdiction)

    require_exact_file_set(plugin_dir / "agents", {path.name for path in agent_sources}, "*.md")
    for source in agent_sources:
        generated = plugin_dir / "agents" / source.name
        expected = rewrite_plugin_agent_skill_links(read(source), jurisdiction)
        generated_text = read(generated)
        if generated_text != expected:
            fail(f"{rel(generated)} does not match transformed canonical source {rel(source)}")
        require_no_bare_same_jurisdiction_names(generated_text, generated, jurisdiction, plugin_name)

    require_exact_dir_set(plugin_dir / "skills", {path.name for path in skill_sources})
    for source_dir in skill_sources:
        source = source_dir / "SKILL.md"
        generated = plugin_dir / "skills" / source_dir.name / "SKILL.md"
        generated_text = read(generated)
        if generated_text != read(source):
            fail(f"{rel(generated)} does not match canonical source {rel(source)}")
        require_no_bare_same_jurisdiction_names(generated_text, generated, jurisdiction, plugin_name)

    return len(agent_sources), len(skill_sources)


def validate_codex_agents(jurisdiction: str, seen_names: set[str]) -> int:
    plugin_name = plugin_codex_name(jurisdiction)
    sources = source_agent_paths(jurisdiction)
    output_dir = ROOT / "plugins" / jurisdiction / ".codex" / "agents"
    expected_names = {f"{prefixed_name(jurisdiction, source.stem)}.toml" for source in sources}
    require_exact_file_set(output_dir, expected_names, "*.toml")

    for source in sources:
        expected_name = prefixed_name(jurisdiction, source.stem)
        generated = output_dir / f"{expected_name}.toml"
        text = read(generated)
        if f'name = "{expected_name}"' not in text:
            fail(f"{rel(generated)} does not declare expected name {expected_name!r}")
        if f"Source canonical agent: `agents/{jurisdiction}/{source.name}`." not in text:
            fail(f"{rel(generated)} does not reference canonical source {rel(source)}")
        data = parse_generated_toml(generated)
        require_no_bare_same_jurisdiction_names(data.get("description", ""), generated, jurisdiction, plugin_name)
        require_no_bare_same_jurisdiction_names(
            codex_source_body(data.get("developer_instructions", "")),
            generated,
            jurisdiction,
            plugin_name,
        )
        if expected_name in seen_names:
            fail(f"duplicate generated Codex agent name: {expected_name}")
        seen_names.add(expected_name)
    return len(sources)


def validate_opencode_package() -> None:
    package_path = ROOT / "package.json"
    if json.loads(read(package_path)) != EXPECTED_PACKAGE_JSON:
        fail(f"{rel(package_path)} does not match expected OpenCode package metadata")
    plugin_path = ROOT / ".opencode" / "plugins" / "lawpowers.js"
    plugin_text = read(plugin_path)
    for needle in (
        "export default async function lawpowers",
        "fileURLToPath(import.meta.url)",
        'join(ROOT, "skills", jurisdiction)',
        'join(ROOT, "agents", jurisdiction)',
        "config(cfg)",
    ):
        if needle not in plugin_text:
            fail(f"{rel(plugin_path)} is missing root-anchored OpenCode loader text: {needle!r}")
    for obsolete in (
        ROOT / "opencode.json",
        ROOT / ".opencode" / "agents",
        ROOT / ".opencode" / "skills",
        ROOT / ".opencode" / "package.json",
        ROOT / ".opencode" / "package-lock.json",
        ROOT / ".opencode" / "node_modules",
    ):
        if obsolete.exists():
            fail(f"{rel(obsolete)} must not exist for package-plugin OpenCode install")


def validate_canonical_text(jurisdiction: str) -> None:
    plugin_name = plugin_codex_name(jurisdiction)
    for path in source_agent_paths(jurisdiction) + [d / "SKILL.md" for d in source_skill_dirs(jurisdiction)]:
        text = read(path)
        require_no_bare_same_jurisdiction_names(text, path, jurisdiction, plugin_name)


def main() -> None:
    claude_agents = 0
    claude_skills = 0
    codex_names: set[str] = set()
    codex_agents = 0

    for jurisdiction in JURISDICTIONS:
        require_prefixed_canonical_sources(jurisdiction)
        validate_canonical_text(jurisdiction)
        agents, skills = validate_claude_copies(jurisdiction)
        claude_agents += agents
        claude_skills += skills
        codex_agents += validate_codex_agents(jurisdiction, codex_names)

    validate_opencode_package()

    if claude_agents != codex_agents:
        fail(f"agent count mismatch: claude={claude_agents}, codex={codex_agents}")

    print(f"Validated platform adapters: {claude_agents} agents, {claude_skills} skills.")


if __name__ == "__main__":
    main()
