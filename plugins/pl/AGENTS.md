# lawpowers / pl — Codex guide

Codex plugin ID: `law-pl`. Claude Code plugin ID: `pl`.

Use this plugin for Polish legal drafting, legal analysis, and official-source workflows. The working language is Polish. Keep `agents/` and `skills/` as the source of truth, and keep this Codex guide in sync with `CLAUDE.md` and `README.md`.

## Rules

- Verify statute text, court practice, procedural terms, fees, and registry information against primary sources before use.
- Primary sources include `isap.sejm.gov.pl`, `dziennikustaw.gov.pl`, `orzeczenia.ms.gov.pl`, `sn.pl`, `nsa.gov.pl`, and `trybunal.gov.pl`.
- Never fabricate case law, case numbers, dates, quotations, registry results, or official positions.
- Use placeholders for personal data: `[imię i nazwisko]`, `[PESEL]`, `[NIP]`, `[adres]`.
- Outputs are legal-document drafts for qualified human review, not final legal advice.

## Codex maintenance

- Codex manifest: `.codex-plugin/plugin.json`.
- Claude manifest: `.claude-plugin/plugin.json`.
- If agents or skills change, update both Codex and Claude docs where user-visible names or behavior changes.
