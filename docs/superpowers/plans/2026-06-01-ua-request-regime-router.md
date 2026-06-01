# UA Request Regime Router Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `ua:request-drafter` choose one correct Ukrainian legal regime before drafting letters, requests, applications, or complaints, so public-information requests are not mixed with citizen appeals, administrative complaints, consular procedure details, or premature enforcement language.

**Architecture:** Add a focused routing skill as the source of truth for request regimes, then make `request-drafter` consume that routing model before drafting. Keep consular logic as a cross-reference into the router, not a consular-specific workaround. Validate with a repository script that checks the skill, Claude agent, generated Codex agent, and consular skill all contain the required guardrails.

**Tech Stack:** Markdown-based lawpowers plugin agents/skills, Python validation scripts, generated Codex TOML shims, JSON plugin manifests.

---

## Current State At Save Time

These changes have already been made in the working tree before this plan file was written:

- Created `scripts/validate-ua-request-regime.py` as the failing validator.
- Confirmed RED state: `python3 scripts/validate-ua-request-regime.py` failed because `plugins/ua/skills/determining-ua-request-regime/SKILL.md` was missing.
- Created `plugins/ua/skills/determining-ua-request-regime/SKILL.md`.
- Reworked `plugins/ua/agents/request-drafter.md` into a regime router/drafter.
- Updated `plugins/ua/skills/applying-consular-procedures/SKILL.md` with a status-request section.
- Updated `plugins/ua/README.md`, `plugins/ua/AGENTS.md`, `plugins/ua/CLAUDE.md`, and `plugins/ua/CHANGELOG.md` partially.
- Regenerated Codex shims after the source-agent changes.
- `python3 scripts/validate-codex-agents.py` passes with `Validated 33 Codex agent files.`
- `python3 scripts/validate-ua-request-regime.py` passes with `Validated Ukrainian request-regime routing guardrails.`
- `git diff --check` passes with no output.
- Code review follow-up removed duplicated routing tables from `request-drafter`, fixed the stale “why” routing conflict, strengthened `scripts/validate-ua-request-regime.py` against that drift, and updated the pre-existing OASK reference in the consular skill using ZU № 2825-IX.

## File Structure

- `scripts/validate-ua-request-regime.py`: repository validator for the new routing guardrails.
- `plugins/ua/skills/determining-ua-request-regime/SKILL.md`: source-of-truth routing skill for Ukrainian request/application/complaint regimes.
- `plugins/ua/agents/request-drafter.md`: drafting agent that must first route to one legal regime.
- `plugins/ua/skills/applying-consular-procedures/SKILL.md`: consular procedure skill, with cross-reference for status requests.
- `plugins/ua/README.md`: public list of UA agents/skills.
- `plugins/ua/AGENTS.md`: Codex-facing UA plugin instructions.
- `plugins/ua/CLAUDE.md`: Claude-facing UA plugin instructions.
- `plugins/ua/CHANGELOG.md`: UA plugin changelog.
- `plugins/ua/.claude-plugin/plugin.json`: Claude plugin manifest version.
- `plugins/ua/.codex-plugin/plugin.json`: Codex plugin manifest version.
- `.claude-plugin/marketplace.json`: root Claude marketplace version entry for UA plugin.
- `plugins/ua/.codex/agents/law-ua-request-drafter.toml`: generated Codex shim, do not edit directly.

### Task 1: Finish Version And Manifest Updates

**Files:**
- Modify: `plugins/ua/.claude-plugin/plugin.json`
- Modify: `plugins/ua/.codex-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Update UA Claude plugin manifest**

Change `plugins/ua/.claude-plugin/plugin.json`:

```json
"version": "0.6.4"
```

- [ ] **Step 2: Update UA Codex plugin manifest**

Change `plugins/ua/.codex-plugin/plugin.json`:

```json
"version": "0.6.4"
```

- [ ] **Step 3: Update root Claude marketplace UA version**

Change `.claude-plugin/marketplace.json`, first plugin entry only:

```json
"version": "0.6.4"
```

- [ ] **Step 4: Validate JSON edited in this task**

Run:

```bash
python3 -m json.tool plugins/ua/.claude-plugin/plugin.json
python3 -m json.tool plugins/ua/.codex-plugin/plugin.json
python3 -m json.tool .claude-plugin/marketplace.json
```

Expected: each command prints formatted JSON and exits `0`.

### Task 2: Regenerate Codex Agent Shims

**Files:**
- Modify: `plugins/ua/.codex/agents/law-ua-request-drafter.toml`
- Possibly modify: other files under `plugins/*/.codex/agents/*.toml` if the converter rewrites all generated agents byte-for-byte.

- [ ] **Step 1: Run converter**

Run:

```bash
python3 scripts/convert-agents-to-codex.py
```

Expected:

```text
Generated 33 Codex agent files.
```

- [ ] **Step 2: Confirm generated request drafter contains routing guardrails**

Run:

```bash
python3 scripts/validate-ua-request-regime.py
```

Expected after Task 2 and before any remaining fixes:

```text
Validated Ukrainian request-regime routing guardrails.
```

If this fails, read the error. The validator names the missing file/text. Fix the source Markdown file, not generated TOML, then rerun the converter.

### Task 3: Finish Public Documentation Consistency

**Files:**
- Modify: `plugins/ua/README.md`
- Modify: `plugins/ua/AGENTS.md`
- Modify: `plugins/ua/CLAUDE.md`
- Modify: `plugins/ua/CHANGELOG.md`

- [ ] **Step 1: Check README mentions the new skill exactly once in the general skills table**

Ensure `plugins/ua/README.md` contains this row:

```markdown
| `ua:determining-ua-request-regime` | Визначення правильного режиму для листів, запитів, заяв і скарг до органів: не змішує ЗУ «Про доступ до публічної інформації», ЗУ «Про звернення громадян», ЗУ «Про адміністративну процедуру», адмінпослуги, персональні дані та адвокатські запити |
```

- [ ] **Step 2: Check `request-drafter` README description describes routing**

Ensure `plugins/ua/README.md` contains this row:

```markdown
| `ua:request-drafter` | Режимний маршрутизатор і drafter для запитів/заяв/скарг до органів: публічна інформація, адвокатські запити, звернення громадян, адмінпроцедура, адмінпослуги, персональні дані, реєстри |
```

- [ ] **Step 3: Check UA AGENTS and CLAUDE contain the routing rule**

Ensure `plugins/ua/AGENTS.md` contains:

```markdown
For letters, requests, applications, and complaints to authorities, first route the document through `skills/determining-ua-request-regime/SKILL.md`. Do not mix public-information requests, citizen appeals, administrative-procedure filings, administrative services, personal-data requests, and advocate requests in one document.
```

Ensure `plugins/ua/CLAUDE.md` contains:

```markdown
Перед складанням листів, запитів, заяв і скарг до органів влади, консульств, установ або розпорядників інформації спочатку визначити правовий режим через `skills/determining-ua-request-regime/SKILL.md`. Не змішувати в одному документі запит на публічну інформацію, звернення громадян, адміністративну процедуру, адмінпослугу, запит суб'єкта персональних даних і адвокатський запит.
```

- [ ] **Step 4: Check changelog entry**

Ensure `plugins/ua/CHANGELOG.md` has a top `## [0.6.4] — 2026-06-01` entry mentioning:

```markdown
- Додано скіл `determining-ua-request-regime`
- `request-drafter` перероблено з двохрежимного агента на режимний маршрутизатор
- Запити про дату надходження, вхідний номер, стан або результат опрацювання документа органом більше не повинні оформлюватися як універсальне `ЗВЕРНЕННЯ`
```

### Task 4: Validate Codex Support

**Files:**
- Read-only validation of generated files.

- [ ] **Step 1: Run Codex agent validator**

Run:

```bash
python3 scripts/validate-codex-agents.py
```

Expected:

```text
Validated 33 Codex agent files.
```

- [ ] **Step 2: Run request-regime validator**

Run:

```bash
python3 scripts/validate-ua-request-regime.py
```

Expected:

```text
Validated Ukrainian request-regime routing guardrails.
```

### Task 5: Validate JSON Manifests

**Files:**
- Read-only validation of JSON manifests.

- [ ] **Step 1: Validate UA manifests and marketplaces**

Run:

```bash
python3 -m json.tool plugins/ua/.claude-plugin/plugin.json
python3 -m json.tool plugins/ua/.codex-plugin/plugin.json
python3 -m json.tool .claude-plugin/marketplace.json
python3 -m json.tool .agents/plugins/marketplace.json
```

Expected: each command prints formatted JSON and exits `0`.

### Task 6: Diff And Whitespace Review

**Files:**
- Review all changed files.

- [ ] **Step 1: Check whitespace**

Run:

```bash
git diff --check
```

Expected: no output, exit `0`.

- [ ] **Step 2: Inspect status**

Run:

```bash
git status --short
```

Expected changed files should include only intended files:

```text
M .claude-plugin/marketplace.json
A docs/superpowers/plans/2026-06-01-ua-request-regime-router.md
M plugins/ua/.claude-plugin/plugin.json
M plugins/ua/.codex-plugin/plugin.json
M plugins/ua/.codex/agents/law-ua-request-drafter.toml
M plugins/ua/AGENTS.md
M plugins/ua/CHANGELOG.md
M plugins/ua/CLAUDE.md
M plugins/ua/README.md
M plugins/ua/agents/request-drafter.md
M plugins/ua/skills/applying-consular-procedures/SKILL.md
A plugins/ua/skills/determining-ua-request-regime/SKILL.md
A scripts/validate-ua-request-regime.py
```

The converter may rewrite other generated Codex agent TOML files without semantic change. If that happens, inspect the diff before deciding whether to keep them.

- [ ] **Step 3: Inspect diff**

Run:

```bash
git diff
```

Expected: changes implement only the request-regime router, consular status-request cross-reference, docs, manifests, generated Codex shim, validator, and this plan.

### Task 7: Final Regression Reasoning Check

**Files:**
- No edits unless check fails.

- [ ] **Step 1: Confirm the original bad case routes correctly**

Use the source text mentally against `plugins/ua/skills/determining-ua-request-regime/SKILL.md` and `plugins/ua/agents/request-drafter.md`:

```text
Polish authority says it sent documents to the Ukrainian consulate. User needs to know whether the consulate received them, the incoming registration date/number, and the processing result.
```

Expected route:

```text
ЗАПИТ на отримання публічної інформації
```

Expected exclusions:

```text
No ЗВЕРНЕННЯ title.
No ZU «Про звернення громадян» basis.
No immediate complaint about inactivity.
No penalty demand in the same document.
No unrelated Reserve+ attachment unless needed to identify the exact consular record.
```

---

## Completion Criteria

- `python3 scripts/convert-agents-to-codex.py` has been run after source agent changes and reports `Generated 33 Codex agent files.`
- `python3 scripts/validate-codex-agents.py` passes.
- `python3 scripts/validate-ua-request-regime.py` passes.
- JSON manifest checks pass.
- `git diff --check` passes.
- Diff contains no unrelated edits.
