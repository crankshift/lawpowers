#!/usr/bin/env python3
"""Validate practical drafting-style guardrails for UA and PL request drafters."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


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
        fail(f"{path.relative_to(ROOT)} contains prohibited drafting text: {needle!r}")


def require_all(path: Path, needles: tuple[str, ...]) -> str:
    text = require_file(path)
    for needle in needles:
        require_contains(text, needle, path)
    return text


def main() -> None:
    ua_agent_needles = (
        "## Real-world drafting style",
        "Не проси адресата зареєструвати документ саме в обраному режимі.",
        "Не додавай погрози штрафом, відповідальністю, скаргою або позовом",
        "Якщо користувач просить знайти, перевірити або порівняти з інтернет-прикладами",
    )
    pl_agent_needles = (
        "## Praktyczny styl pisma",
        "Nie proś adresata o zarejestrowanie pisma dokładnie w wybranym trybie.",
        "Nie dodawaj gróźb sankcjami, odpowiedzialnością, skargą albo pozwem",
        "Jeżeli użytkownik prosi o wyszukanie, sprawdzenie albo porównanie z przykładami z internetu",
    )
    ua_skill_needles = (
        "## Стиль після вибору режиму",
        "Правильний режим не є підставою для перевантаженого тексту.",
        "мінімально достатніми: назвою документа, ключовою правовою підставою і конкретними пунктами прохання",
    )
    pl_skill_needles = (
        "## Styl po wyborze trybu",
        "Prawidłowy tryb nie jest powodem do przeładowania pisma.",
        "minimum: tytułem pisma, kluczową podstawą prawną i konkretnymi punktami żądania",
    )

    files_to_check = {
        ROOT / "agents" / "ua" / "law-ua-request-drafter.md": ua_agent_needles,
        ROOT / "plugins" / "ua" / "agents" / "law-ua-request-drafter.md": ua_agent_needles,
        ROOT / "plugins" / "ua" / ".codex" / "agents" / "law-ua-request-drafter.toml": ua_agent_needles,
        ROOT / "agents" / "pl" / "law-pl-request-drafter.md": pl_agent_needles,
        ROOT / "plugins" / "pl" / "agents" / "law-pl-request-drafter.md": pl_agent_needles,
        ROOT / "plugins" / "pl" / ".codex" / "agents" / "law-pl-request-drafter.toml": pl_agent_needles,
        ROOT
        / "skills"
        / "ua"
        / "law-ua-determining-ua-request-regime"
        / "SKILL.md": ua_skill_needles,
        ROOT
        / "plugins"
        / "ua"
        / "skills"
        / "law-ua-determining-ua-request-regime"
        / "SKILL.md": ua_skill_needles,
        ROOT
        / "skills"
        / "pl"
        / "law-pl-determining-pl-request-regime"
        / "SKILL.md": pl_skill_needles,
        ROOT
        / "plugins"
        / "pl"
        / "skills"
        / "law-pl-determining-pl-request-regime"
        / "SKILL.md": pl_skill_needles,
    }

    checked_texts = []
    for path, needles in files_to_check.items():
        checked_texts.append((path, require_all(path, needles)))

    prohibited = (
        "Прошу зареєструвати цей документ саме як запит",
        "прошу зареєструвати цей документ саме як запит",
        "відповідь не по суті = неправомірна відмова",
        "zarejestrować ten dokument dokładnie jako",
        "zarejestrować to pismo dokładnie jako",
    )
    for path, text in checked_texts:
        for needle in prohibited:
            require_absent(text, needle, path)

    print("Validated UA and PL practical request-drafting style guardrails.")


if __name__ == "__main__":
    main()
