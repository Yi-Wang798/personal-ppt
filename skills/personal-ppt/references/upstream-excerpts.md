# 按需原始摘录

这些摘录仅作来源记录，不替代本 skill 的执行规则。MIT 原文见 licenses/。


## zarazhangrui/frontend-slides

来源：[SKILL.md](https://github.com/zarazhangrui/frontend-slides/blob/9906a34d640d2111f724544cbc50f7f130569ae1/SKILL.md)

### Content Density Modes

Ask the user whether this is primarily a reading deck or a speaking deck, then design around that answer:

| Density mode | Best for | Design behavior |
|


## MiniMax-AI/skills

来源：[skills/pptx-generator/references/design-system.md](https://github.com/MiniMax-AI/skills/blob/60aaae52bb2af8162732751a4332f62a5fef518b/skills/pptx-generator/references/design-system.md)

### Recommended Fonts

| Language | Default Font | Alternatives |
|----------|-------------|--------------|
| **Chinese** | Microsoft YaHei | — |
| **English** | Arial | Georgia, Calibri, Cambria, Trebuchet MS |

- For mixed Chinese-English content: use Microsoft YaHei for Chinese, the chosen font for English
- Prefer system fonts for cross-platform compatibility
- Titles and body text can use different font pairings (e.g. Georgia + Calibri)


## siril9/presentation-skill

来源：[references/reproducible_workflow.md](https://github.com/siril9/presentation-skill/blob/efd899c5ddf866af2ce0001c4c9340af775d4d55/references/reproducible_workflow.md)

## Preflight (Static Outline Lint)

Before running the slow build + render cycle, run the static preflight
linter against `outline.json`. It catches common authoring errors in
under a second:

```bash
python3 scripts/preflight.py --outline outline.json
```

Exit codes:

- `0` - clean.
- `1` - warnings only (non-blocking).
- `2` - blocking errors (e.g., malformed chart, missing cards array,
  invalid `font_pair`).
- `3` - outline JSON is malformed.

`scripts/build_workspace.py` runs preflight first automatically. Use
`--strict-preflight` to abort the build on any preflight error, and
`--skip-preflight` to disable the check entirely. When `--qa` is set the
build already behaves strictly (blocking errors abort), because those
errors will reliably fail the downstream QA gate anyway and there's no
point paying the ~60s render cost to confirm it.

Use `--strict-preflight` when:

- You're iterating quickly and want fast failure feedback.
- You're running in CI and want build failures before render.
- You want to block authoring errors (non-numeric stats, malformed
  chart, bad font_pair) from ever reaching the renderer.

Skip preflight (`--skip-preflight`) only when you're intentionally
bypassing lint for a known-divergent outline, e.g., debugging a
renderer-side bug against a crafted edge-case input.


## ningzimu/codex-ppt-skill

来源：[skills/codex-ppt/docs/user-supplied-assets.md](https://github.com/ningzimu/codex-ppt-skill/blob/85d4e629275e6c5793a33801d29b364383ea4c1e/skills/codex-ppt/docs/user-supplied-assets.md)

When the user provides paper figures, experiment result charts, screenshots, logos, or other assets that must appear in the deck, treat them as source assets, not as loose visual inspiration.
