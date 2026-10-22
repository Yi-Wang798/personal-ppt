# personal-ppt

English | [简体中文](README.zh-CN.md)

A Codex plugin for editable presentations: work reports, business proposals, lessons, product introductions, research talks, and personal portfolios. It generates and shows a design image for each slide, then rebuilds the slide in PowerPoint.

Version **2.1.0**.

## How it works

1. Read the brief and source material, identify the audience, and decide what the presentation needs to communicate.
2. Draft the slide content and edit it for clear, natural language. Keep speaker notes and production records separate.
3. Generate and show a master design. In automatic mode, select a direction and continue. If you ask to review samples, wait for your choice.
4. Generate and show every slide design using the selected master and your real assets.
5. Build a native PowerPoint master, reconstruct the slides, and review the exported result. Fix concrete problems before delivery.

Text, tables, data charts, and simple diagrams use editable objects where supported. Photos and complex illustrations remain separate images you can move or replace. Original data and evidence images take priority over generated approximations.

The plugin adjusts image areas, text, and spacing when real assets have different proportions from the design. It checks alignment, mixed-language bold text, meaningful line breaks, color, and missing elements against the actual PPTX and its rendered pages.

## What changed in 2.1

- Native geometry conversion now uses a pinned, attributed subset of [PPT Master](https://github.com/hugohe3/ppt-master). Simple SVG paths and selected Office shapes become editable PowerPoint objects.
- A single scene description carries measured positions, text styles, and asset references into the PPTX. Fixed elements live in a real slide master; text roles inherit its settings.
- Complex artwork can be split into a clean background, subject, and foreground. Each image-generation request uses the original slide design as its reference. Text stays native, and evidence images are kept intact.
- Six composition references cover comparisons, key statements, image-and-text pages, timelines, chart commentary, and table summaries. They guide planning without imposing one layout on every slide.
- Native tables and basic charts remain editable. Charts include an Excel workbook containing the supplied values.

The new bridge is documented in [native-bridge.md](skills/personal-ppt/references/native-bridge.md). This is a scoped integration, not the full upstream product: animations, external image-generation services, and formula conversion are outside this release.

New projects use workflow version 2.1. Existing projects keep their settings. The production method stays the same: generate and show every slide design, then rebuild it. Chinese uses **Microsoft YaHei** and English uses **Times New Roman**; font sizes follow the content and layout.

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

Or download the repository using **Code → Download ZIP**, extract it, and copy the complete `skills/personal-ppt` directory to `~/.agents/skills/personal-ppt`. On Windows, use `%USERPROFILE%\.agents\skills\personal-ppt`. Keep `scripts`, `references`, `assets`, and `vendor` beside `SKILL.md`. Restart Codex if the skill is not listed.

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

Codex needs access to its built-in image generation tool and the Presentations skill. Runtime discovery uses `load_workspace_dependencies`; the native bridge uses Python with python-pptx, Pillow, and lxml. The pinned converter is included under `vendor`. Humanizer and Humanizer ZH can support copy editing when installed. The workflow also includes a self-contained copy guide.

This repository provides instructions and helper scripts, not model access, subscriptions, or image-generation quota. Rebuilding images as editable slides still requires measurement and visual review. Internal checks aim to reduce revisions; they cannot guarantee a perfect first result for every brief. Complex raster illustrations are not editable vector paths.

`assets/example-spec.json` is a synthetic example of the earlier layout schema. It is not a completed deck or proof of the full image-generation workflow. See [validation-v2.1.md](validation-v2.1.md) for the current tests and their limits; the earlier results remain in [validation-v2.md](validation-v2.md).

## Repository structure

```text
.agents/plugins/marketplace.json   Marketplace catalog
.codex-plugin/plugin.json         Plugin metadata
skills/personal-ppt/SKILL.md       Main workflow
skills/personal-ppt/scripts/      Native bridge, checks, and helper tools
skills/personal-ppt/references/   Task, writing, design, and reconstruction guides
skills/personal-ppt/assets/       Technical example, palettes, composition references
skills/personal-ppt/vendor/       Pinned converter and original notices
```

The marketplace catalog is a configuration file you can create and share without purchasing it. It is separate from approval for an official public plugin directory. Codex service availability and account requirements apply separately.

## Sources and licensing

See [sources.md](skills/personal-ppt/references/sources.md), [sources.lock.json](skills/personal-ppt/references/sources.lock.json), and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for sources, scope, and upstream notices. Version 2.1 includes a scoped PPT Master code dependency with its original notices and file hashes. Writing guidance does not require third-party rewriting services.

Installation references: OpenAI's [plugin documentation](https://developers.openai.com/plugins/build/plugins) and [skill documentation](https://learn.chatgpt.com/docs/build-skills).
