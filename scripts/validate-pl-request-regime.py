#!/usr/bin/env python3
"""Validate the Polish request-regime routing guardrails."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PL = ROOT / "plugins" / "pl"


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_file(path: Path) -> str:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def require_contains(text: str, needle: str, path: Path) -> None:
    if needle not in text:
        fail(f"{path.relative_to(ROOT)} is missing required text: {needle!r}")


def require_absent(text: str, needle: str, path: Path) -> None:
    if needle in text:
        fail(f"{path.relative_to(ROOT)} contains prohibited stale routing text: {needle!r}")


def require_json_version(path: Path, expected: str) -> None:
    data = json.loads(require_file(path))
    actual = data.get("version")
    if actual != expected:
        fail(f"{path.relative_to(ROOT)} version is {actual!r}, expected {expected!r}")


def require_marketplace_plugin_version(path: Path, plugin_name: str, expected: str) -> None:
    data = json.loads(require_file(path))
    for plugin in data.get("plugins", []):
        if plugin.get("name") == plugin_name:
            actual = plugin.get("version")
            if actual != expected:
                fail(
                    f"{path.relative_to(ROOT)} plugin {plugin_name!r} version is "
                    f"{actual!r}, expected {expected!r}"
                )
            return
    fail(f"{path.relative_to(ROOT)} is missing plugin {plugin_name!r}")


def main() -> None:
    skill_path = PL / "skills" / "determining-pl-request-regime" / "SKILL.md"
    agent_path = PL / "agents" / "request-drafter.md"
    codex_agent_path = PL / ".codex" / "agents" / "law-pl-request-drafter.toml"
    readme_path = PL / "README.md"
    agents_guide_path = PL / "AGENTS.md"
    claude_guide_path = PL / "CLAUDE.md"
    changelog_path = PL / "CHANGELOG.md"
    claude_manifest_path = PL / ".claude-plugin" / "plugin.json"
    codex_manifest_path = PL / ".codex-plugin" / "plugin.json"
    claude_marketplace_path = ROOT / ".claude-plugin" / "marketplace.json"

    skill = require_file(skill_path)
    agent = require_file(agent_path)
    codex_agent = require_file(codex_agent_path)
    readme = require_file(readme_path)
    agents_guide = require_file(agents_guide_path)
    claude_guide = require_file(claude_guide_path)
    changelog = require_file(changelog_path)

    for needle in (
        "name: determining-pl-request-regime",
        "jedno pismo = jeden tryb prawny",
        "UDIP",
        "art. 63 KPA",
        "art. 73 KPA",
        "art. 217",
        "art. 227 KPA",
        "art. 241 KPA",
        "ustawa o petycjach",
        "PPSA",
        "akta sądowe",
        "RODO",
        "rejestry publiczne",
        "Ordynacja podatkowa",
        "ZUS",
        "cudzoziemcy",
        "USC",
        "pismo adwokata / radcy",
        "nie jest ukraińskim adwokatskim zapytem",
    ):
        require_contains(skill, needle, skill_path)

    for needle in (
        "determining-pl-request-regime",
        "Mandatory routing",
        "jedno pismo = jeden tryb prawny",
        "Nie mieszaj trybów prawnych",
        "najpierw ustal tryb",
        "Drafting notes after routing",
        "WNIOSEK o udostępnienie informacji publicznej",
        "nie PETYCJA",
        "nie skarga z KPA",
    ):
        require_contains(agent, needle, agent_path)
        require_contains(codex_agent, needle, codex_agent_path)

    for needle in (
        "### Cechy wyboru trybu",
        "| Każda osoba chce informacji o działalności organu / podmiotu publicznego | UDIP |",
        "Doprecyzować tryb — UDIP / art. 73 KPA / pismo adwokata / inny (patrz tabela wyżej).",
    ):
        require_absent(agent, needle, agent_path)
        require_absent(codex_agent, needle, codex_agent_path)

    for text, path in (
        (readme, readme_path),
        (agents_guide, agents_guide_path),
        (claude_guide, claude_guide_path),
        (changelog, changelog_path),
    ):
        require_contains(text, "determining-pl-request-regime", path)

    require_contains(changelog, "## [0.4.3] — 2026-06-01", changelog_path)
    require_json_version(claude_manifest_path, "0.4.3")
    require_json_version(codex_manifest_path, "0.4.3")
    require_marketplace_plugin_version(claude_marketplace_path, "pl", "0.4.3")

    print("Validated Polish request-regime routing guardrails.")


if __name__ == "__main__":
    main()
