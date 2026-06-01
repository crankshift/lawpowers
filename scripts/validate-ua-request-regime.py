#!/usr/bin/env python3
"""Validate the Ukrainian request-regime routing guardrails."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = ROOT / "plugins" / "ua"


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


def main() -> None:
    skill_path = UA / "skills" / "determining-ua-request-regime" / "SKILL.md"
    agent_path = UA / "agents" / "request-drafter.md"
    consular_path = UA / "skills" / "applying-consular-procedures" / "SKILL.md"
    codex_agent_path = UA / ".codex" / "agents" / "law-ua-request-drafter.toml"
    readme_path = UA / "README.md"
    agents_guide_path = UA / "AGENTS.md"
    claude_guide_path = UA / "CLAUDE.md"

    skill = require_file(skill_path)
    agent = require_file(agent_path)
    consular = require_file(consular_path)
    codex_agent = require_file(codex_agent_path)
    readme = require_file(readme_path)
    agents_guide = require_file(agents_guide_path)
    claude_guide = require_file(claude_guide_path)

    for needle in (
        "name: determining-ua-request-regime",
        "один документ = один правовий режим",
        "Запит на публічну інформацію",
        "Адвокатський запит",
        "Звернення громадян",
        "Заява в адміністративній справі",
        "Клопотання учасника адміністративного провадження",
        "Доступ до матеріалів адміністративної справи",
        "Адміністративна скарга",
        "Заява на адміністративну послугу",
        "Запит суб'єкта персональних даних",
        "Витяг, довідка, копія або дублікат з реєстру",
        "консульство",
    ):
        require_contains(skill, needle, skill_path)

    for needle in (
        "determining-ua-request-regime",
        "Mandatory routing",
        "один документ = один правовий режим",
        "Не змішуй правові режими",
        "спочатку витребуй інформацію",
        "Drafting notes after routing",
        "ЗАПИТ",
        "на отримання публічної інформації",
        "не ЗВЕРНЕННЯ",
    ):
        require_contains(agent, needle, agent_path)
        require_contains(codex_agent, needle, codex_agent_path)

    for needle in (
        "Питання «чому так діє посадовець», статистика, копії актів | Публічна інформація",
        "| Режим | Коли застосовується | Основа | Типовий строк |",
        "### Ознаки, за якими обрати режим",
    ):
        require_absent(agent, needle, agent_path)
        require_absent(codex_agent, needle, codex_agent_path)

    for needle in (
        "determining-ua-request-regime",
        "request-drafter",
        "статусні запити",
        "чи надходив документ",
        "дата, вхідний номер, стан або результат обробки",
    ):
        require_contains(consular, needle, consular_path)

    for text, path in (
        (readme, readme_path),
        (agents_guide, agents_guide_path),
        (claude_guide, claude_guide_path),
    ):
        require_contains(text, "determining-ua-request-regime", path)

    print("Validated Ukrainian request-regime routing guardrails.")


if __name__ == "__main__":
    main()
