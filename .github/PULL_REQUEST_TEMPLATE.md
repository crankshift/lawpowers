<!--
Thanks for contributing to lawpowers! Before you submit, check:
  - Run `claude plugin validate .` locally. It must pass.
  - If you changed plugin content, update that plugin's CHANGELOG
    (plugins/ua/CHANGELOG.md in Ukrainian or plugins/pl/CHANGELOG.md in Polish).
    The root CHANGELOG.md is historical — only touch it for cross-cutting
    monorepo changes (tooling, structural reshuffle).
  - Plugin releases are tagged per plugin: ua/vX.Y.Z, pl/vX.Y.Z.
    If you're cutting a release, follow docs/RELEASING.md.
-->

## Summary

<!-- 1–3 sentences. What does this PR change and why? -->

## Scope

<!-- Tick all that apply. -->

- [ ] Plugin `ua` (Ukrainian law)
- [ ] Plugin `pl` (Polish law)
- [ ] Marketplace (catalog, `.claude-plugin/marketplace.json`)
- [ ] Monorepo-level (root docs, tooling, CI, scripts)

## Type of change

- [ ] New agent or skill
- [ ] Fix in an existing agent or skill (wording, legal accuracy, outdated norm)
- [ ] Docs only
- [ ] Tooling / scripts / CI
- [ ] Refactor (no behavior change)
- [ ] Breaking change (see Migration below)

## Details

<!--
If you added an agent or skill: what does it do, which statutes/norms does it reference, and why is it useful?
If you changed an existing one: what was wrong, what changed, and what's the evidence (a ruling, a statute revision, a reader's report)?
If this is a fix for an outdated norm: link the current redaction on zakon.rada.gov.ua (UA) or isap.sejm.gov.pl (PL) and include the redaction date you verified.
-->

## CHANGELOG

- [ ] `plugins/ua/CHANGELOG.md` updated (Ukrainian) if plugin `ua` changed.
- [ ] `plugins/pl/CHANGELOG.md` updated (Polish) if plugin `pl` changed.
- [ ] Root `CHANGELOG.md` updated — only for cross-cutting monorepo changes (tooling, structural reshuffle).
- [ ] N/A — purely tooling/infra change.

## Migration

<!-- Only if this is a breaking change. Give the exact commands users need to run. -->

```
/plugin marketplace update lawpowers
/reload-plugins
```

## Test plan

<!-- What did you actually verify? Examples below, edit to match. -->

- [ ] `claude plugin validate .` → ✔ Validation passed.
- [ ] Loaded locally with `claude --plugin-dir ./plugins/ua` (or `./plugins/pl`), confirmed agent appears under `/agents` with the correct namespace.
- [ ] Asked the agent a representative question and verified the output quotes the primary source (zakon.rada / isap.sejm) with a redaction date.
- [ ] Cross-links in READMEs / CHANGELOGs render correctly on GitHub.

## Related

<!-- Linked issues, PRs, release notes. Use "Closes #N" to auto-close an issue on merge. -->
