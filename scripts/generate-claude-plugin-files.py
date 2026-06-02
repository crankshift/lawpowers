#!/usr/bin/env python3
"""Generate Claude-compatible plugin files from canonical sources."""

from __future__ import annotations

import shutil
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JURISDICTIONS = ("pl", "ua")


def fail(message: str) -> None:
    raise SystemExit(f"error: {message}")


def mirror_tree(source: Path, destination: Path) -> None:
    if not source.is_dir():
        fail(f"missing source directory: {source.relative_to(ROOT)}")
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def rewrite_agent_skill_links(text: str, jurisdiction: str) -> str:
    return re.sub(
        rf"\.\./\.\./skills/{re.escape(jurisdiction)}/([A-Za-z0-9_-]+)/SKILL\.md",
        r"../skills/\1/SKILL.md",
        text,
    )


def generate_agents(source: Path, destination: Path, jurisdiction: str) -> int:
    if not source.is_dir():
        fail(f"missing source directory: {source.relative_to(ROOT)}")
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)
    count = 0
    for agent in sorted(source.glob("*.md")):
        text = rewrite_agent_skill_links(agent.read_text(encoding="utf-8"), jurisdiction)
        (destination / agent.name).write_text(text, encoding="utf-8")
        count += 1
    return count


def generate_jurisdiction(jurisdiction: str) -> tuple[int, int]:
    plugin_dir = ROOT / "plugins" / jurisdiction
    if not plugin_dir.is_dir():
        fail(f"missing plugin directory: {plugin_dir.relative_to(ROOT)}")

    source_agents = ROOT / "agents" / jurisdiction
    source_skills = ROOT / "skills" / jurisdiction
    agents = generate_agents(source_agents, plugin_dir / "agents", jurisdiction)
    mirror_tree(source_skills, plugin_dir / "skills")
    return agents, len([p for p in source_skills.iterdir() if p.is_dir()])


def main() -> None:
    total_agents = 0
    total_skills = 0
    for jurisdiction in JURISDICTIONS:
        agents, skills = generate_jurisdiction(jurisdiction)
        total_agents += agents
        total_skills += skills
    print(f"Generated Claude plugin files: {total_agents} agents, {total_skills} skills.")


if __name__ == "__main__":
    main()
