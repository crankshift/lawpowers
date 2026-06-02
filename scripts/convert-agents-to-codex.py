#!/usr/bin/env python3
"""Generate Codex custom-agent TOML files from canonical lawpowers agents.

This keeps `agents/<jurisdiction>/*.md` as the source of truth and writes
Codex-compatible custom agents to `plugins/<jurisdiction>/.codex/agents/*.toml`.
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.S)
SUPPORTED_MODELS = {
    "sonnet": "gpt-5.4-mini",
    "claude-sonnet": "gpt-5.4-mini",
    "haiku": "gpt-5.4-mini",
    "opus": "gpt-5.4",
}
OMIT_MODELS = {"inherit", "default", ""}


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    raw, body = match.groups()
    return parse_simple_yaml(raw), body


def parse_simple_yaml(raw: str) -> dict[str, object]:
    values: dict[str, object] = {}
    current_key: str | None = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith("  - ") and current_key:
            current = values.setdefault(current_key, [])
            if not isinstance(current, list):
                current = [current]
                values[current_key] = current
            current.append(line[4:].strip())
            continue
        key, sep, value = line.partition(":")
        if not sep:
            continue
        current_key = key.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            values[current_key] = [part.strip().strip('"\'') for part in value[1:-1].split(",") if part.strip()]
        elif value:
            values[current_key] = value.strip('"')
        else:
            values[current_key] = []
    return values


def as_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [part.strip() for part in str(value).split(",") if part.strip()]


def toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def toml_multiline(value: str) -> str:
    return toml_string(value.rstrip())


def plugin_codex_name(plugin_dir: Path) -> str:
    manifest = plugin_dir / ".codex-plugin" / "plugin.json"
    if not manifest.is_file():
        raise FileNotFoundError(f"Missing Codex plugin manifest: {manifest}")
    return json.loads(manifest.read_text(encoding="utf-8"))["name"]


def canonical_names(jurisdiction: str) -> set[str]:
    agent_dir = ROOT / "agents" / jurisdiction
    skill_dir = ROOT / "skills" / jurisdiction
    names = {path.stem for path in agent_dir.glob("*.md")}
    if skill_dir.is_dir():
        names.update(path.name for path in skill_dir.iterdir() if (path / "SKILL.md").is_file())
    return names


def unprefixed_canonical_names(jurisdiction: str, plugin_name: str) -> set[str]:
    prefix = f"{plugin_name}-"
    return {name.removeprefix(prefix) if name.startswith(prefix) else name for name in canonical_names(jurisdiction)}


def prefixed_name(plugin_name: str, source_name: str) -> str:
    return source_name if source_name.startswith(f"{plugin_name}-") else f"{plugin_name}-{source_name}"


def rewrite_body_references(body: str, jurisdiction: str, plugin_name: str, same_jurisdiction_names: set[str]) -> str:
    body = re.sub(rf"\b{re.escape(jurisdiction)}:(?!{re.escape(plugin_name)}-)([A-Za-z0-9_-]+)", rf"{plugin_name}-\1", body)
    body = re.sub(
        rf"\.\./\.\./skills/{re.escape(jurisdiction)}/(?:{re.escape(plugin_name)}-)?([A-Za-z0-9_-]+)/SKILL\.md",
        rf"../skills/{plugin_name}-\1/SKILL.md",
        body,
    )
    body = re.sub(rf"\.\./(?:{re.escape(plugin_name)}-)?([A-Za-z0-9_-]+)/SKILL\.md", rf"../skills/{plugin_name}-\1/SKILL.md", body)
    for name in sorted(same_jurisdiction_names, key=len, reverse=True):
        body = re.sub(
            rf"(?<![A-Za-z0-9_-])(?<!{re.escape(plugin_name)}-){re.escape(name)}(?![A-Za-z0-9_-])",
            f"{plugin_name}-{name}",
            body,
        )
    return body


def render_agent(source: Path, jurisdiction: str, plugin_name: str, same_jurisdiction_names: set[str]) -> tuple[str, str]:
    metadata, body = parse_frontmatter(source.read_text(encoding="utf-8"))
    body = rewrite_body_references(body, jurisdiction, plugin_name, same_jurisdiction_names)
    source_name = str(metadata.get("name") or source.stem).strip()
    codex_name = prefixed_name(plugin_name, source_name)
    description = str(metadata.get("description") or f"Migrated lawpowers agent `{source_name}`.").strip()
    description = rewrite_body_references(description, jurisdiction, plugin_name, same_jurisdiction_names)
    tools = as_list(metadata.get("tools"))
    source_model = str(metadata.get("model") or "").strip()
    mapped_model = SUPPORTED_MODELS.get(source_model.lower())

    notes: list[str] = [
        "## Codex migration notes",
        "",
        f"- Source canonical agent: `agents/{jurisdiction}/{source.name}`.",
        "- This file is generated by `scripts/convert-agents-to-codex.py`; edit the canonical Markdown agent, then regenerate.",
    ]
    if tools:
        notes.extend([
            "- Claude `tools` metadata is preserved as prompt guidance only; Codex does not treat this as a hard permission boundary.",
            "- Suggested tools from source: " + ", ".join(f"`{tool}`" for tool in tools) + ".",
        ])
    if source_model and source_model.lower() not in OMIT_MODELS and not mapped_model:
        notes.append(f"- Source model `{source_model}` has no explicit Codex mapping; session defaults apply.")

    instructions = body.rstrip() + "\n\n" + "\n".join(notes) + "\n"

    lines = [
        "# Generated from canonical lawpowers agent Markdown. Do not edit directly.",
        f"name = {toml_string(codex_name)}",
        f"description = {toml_string(description)}",
    ]
    if mapped_model:
        lines.append(f"model = {toml_string(mapped_model)}")
    lines.append(f"developer_instructions = {toml_multiline(instructions)}")
    return codex_name, "\n".join(lines) + "\n"


def convert_plugin(plugin_dir: Path) -> int:
    jurisdiction = plugin_dir.name
    agents_dir = ROOT / "agents" / jurisdiction
    if not agents_dir.is_dir():
        return 0
    plugin_name = plugin_codex_name(plugin_dir)
    same_jurisdiction_names = unprefixed_canonical_names(jurisdiction, plugin_name)
    output_dir = plugin_dir / ".codex" / "agents"
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for source in sorted(agents_dir.glob("*.md")):
        codex_name, content = render_agent(source, jurisdiction, plugin_name, same_jurisdiction_names)
        (output_dir / f"{codex_name}.toml").write_text(content, encoding="utf-8")
        count += 1
    return count


def main() -> None:
    total = 0
    for plugin_dir in sorted((ROOT / "plugins").iterdir()):
        if plugin_dir.is_dir():
            total += convert_plugin(plugin_dir)
    print(f"Generated {total} Codex agent files.")


if __name__ == "__main__":
    main()
