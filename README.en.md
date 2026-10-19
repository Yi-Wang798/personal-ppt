# personal-ppt

English | [简体中文](README.zh-CN.md)

A Codex plugin for editable presentations: work reports, business proposals, lessons, product introductions, research talks, and personal portfolios. It generates and shows a design image for each slide, then rebuilds the slide in PowerPoint.

Version **2.0.0**.

## How it works

1. Read the brief and source material, identify the audience, and decide what the presentation needs to communicate.
2. Draft the slide content and edit it for clear, natural language. Keep speaker notes and production records separate.
3. Generate and show a master design. In automatic mode, select a direction and continue. If you ask to review samples, wait for your choice.
4. Generate and show every slide design using the selected master and your real assets.
5. Build a native PowerPoint master, reconstruct the slides, and review the exported result. Fix concrete problems before delivery.

Text, tables, data charts, and simple diagrams use editable objects where supported. Photos and complex illustrations remain separate images you can move or replace. Original data and evidence images take priority over generated approximations.

The plugin adjusts image areas, text, and spacing when real assets have different proportions from the design. It checks alignment, mixed-language bold text, meaningful line breaks, color, and missing elements against the actual PPTX and its rendered pages.

## What changed in 2.0

- Content planning now covers different audiences and presentation types. Research-specific requirements apply to research tasks.
- Copy is edited before image generation. Production reminders stay out of slides, and inference wording is no longer checked against a fixed list of keywords.
- Colors and layouts follow the topic, audience, and brand. Journal-inspired palettes remain available.
- Automatic mode handles master selection and sample checks internally. Review mode keeps the approval steps you request.
- New projects use workflow version 2.0. Existing projects keep their original settings and review requirements.

The production method is unchanged: design every slide with built-in image generation, show the image, then rebuild it as an editable slide. Chinese uses **Microsoft YaHei** and English uses **Times New Roman**. Font sizes are chosen for the content and layout, then kept consistent by role.

## Install the plugin

Use a Codex CLI that supports plugin commands:

```shell
codex plugin marketplace add Yi-Wang798/personal-ppt
codex plugin add personal-ppt@personal-ppt-marketplace
```

The first command adds this repository's marketplace catalog; the second installs the plugin. Reopen Codex or start a new chat after installation. In a desktop client with marketplace support, add this repository and install `personal-ppt` from its listing.

The plugin already includes the skill. Installing a second standalone copy can create duplicate entries.

## Install only the skill

Ask Codex:

```text
Use $skill-installer to install skills/personal-ppt from Yi-Wang798/personal-ppt.
Keep the complete skill folder.
```

Or download the repository using **Code → Download ZIP**, extract it, and copy the complete `skills/personal-ppt` directory to `~/.agents/skills/personal-ppt`. On Windows, use `%USERPROFILE%\.agents\skills\personal-ppt`. Keep `scripts`, `references`, and `assets` beside `SKILL.md`. Restart Codex if the skill is not listed.

## Use it

```text
Use $personal-ppt to make a 12-slide business presentation from these materials.
Generate and show every slide design, then build the editable PPTX. Complete it automatically.
```

```text
Use $personal-ppt to create a lesson presentation. Show me master-design options before continuing.
```

You can specify the audience, duration, slide count, language, and brand requirements. The plugin can infer details from the supplied material and asks when missing information would change the result.

## Requirements and limits

Codex needs access to its built-in image generation tool and the Presentations skill. Runtime discovery uses `load_workspace_dependencies`; regional color sampling uses Pillow. Humanizer and Humanizer ZH can support copy editing when installed. The workflow also includes a self-contained copy guide.

This repository provides instructions and helper scripts, not model access, subscriptions, or image-generation quota. Rebuilding images as editable slides still requires measurement and visual review. Internal checks aim to reduce revisions; they cannot guarantee a perfect first result for every brief. Complex raster illustrations are not editable vector paths.

`assets/example-spec.json` is a synthetic example of the earlier layout schema. It is not a completed deck or proof of the full image-generation workflow. The 2.0 script regression results are in [validation-v2.md](validation-v2.md).

## Repository structure

```text
.agents/plugins/marketplace.json   Marketplace catalog
.codex-plugin/plugin.json         Plugin metadata
skills/personal-ppt/SKILL.md       Main workflow
skills/personal-ppt/scripts/      Checks and helper tools
skills/personal-ppt/references/   Task, writing, design, and reconstruction guides
skills/personal-ppt/assets/       Technical example and optional palettes
```

The marketplace catalog is a configuration file you can create and share without purchasing it. It is separate from approval for an official public plugin directory. Codex service availability and account requirements apply separately.

## Sources and licensing

See [sources.md](skills/personal-ppt/references/sources.md), [sources.lock.json](skills/personal-ppt/references/sources.lock.json), and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for sources, scope, and upstream notices. Version 2.0 selectively adapts writing and design ideas; it does not bundle a chain of third-party rewriting services.

Installation references: OpenAI's [plugin documentation](https://developers.openai.com/plugins/build/plugins) and [skill documentation](https://learn.chatgpt.com/docs/build-skills).
