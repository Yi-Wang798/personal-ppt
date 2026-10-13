# Personal PPT

[简体中文](README.md) | English

Personal PPT is a Codex plugin for research presentations. It creates visual design references, then rebuilds text, tables, data charts, and simple process diagrams as editable PowerPoint objects.

Current version: **1.7.0**.

## What it does

- Organizes research material and keeps slide content separate from speaker notes and production records.
- Generates master-design options for you to choose from, then creates and shows slide designs in that style.
- Uses your original experimental images, data, and mechanism diagrams while preserving labels, scales, and scientific meaning.
- Builds editable slides. Complex illustrations remain separate images that you can move or replace.
- Adjusts layouts to fit real assets and checks alignment, bold text, meaningful line breaks, spacing, and reference colors.
- Reviews rendered slides for content, layout, and color.

The default fonts are Microsoft YaHei for Chinese and Times New Roman for English. Font sizes follow the content and master layout. Palette references include Nature- and Science-inspired colors; they are not official journal presentation templates.

## Installation

The full plugin includes the skill. Choose one installation method to avoid duplicate entries.

### Install the full plugin

Run these commands in a Codex CLI that supports plugins:

```shell
codex plugin marketplace add Yi-Wang798/personal-ppt
codex plugin add personal-ppt@personal-ppt-marketplace
```

The first command adds this repository's marketplace catalog. The second installs the plugin. Reopen Codex or start a new chat before using it. If your client does not provide the `plugin` command, use the skill installation method below.

For installation through the desktop plugin directory, add the repository marketplace first, select **Personal PPT**, and install the listed plugin. Interface labels may vary between clients.

### Install only the skill

Ask Codex:

```text
Use $skill-installer to install the skill from Yi-Wang798/personal-ppt.
The path inside the repository is skills/personal-ppt. Keep the complete folder.
```

You can also select **Code → Download ZIP** on GitHub, extract it, and copy the entire `skills/personal-ppt` folder to `~/.agents/skills/personal-ppt`. On Windows, that is `%USERPROFILE%\.agents\skills\personal-ppt`. Restart Codex if the skill does not appear.

Keep the `scripts`, `references`, and `assets` folders alongside `SKILL.md`. If you already installed the plugin, you do not need a second standalone copy of the skill.

## Usage

```text
Use $personal-ppt to create an editable research presentation from these materials.
Show me master-design options first, then design and build the slides.
```

The workflow covers source checks, copy editing, master selection, slide design, review of a complex sample slide, reconstruction, and final checks. The plugin keeps the original references and records layout adjustments. If a real figure has different proportions from the design image, it can resize the figure area and move nearby text to keep the content readable and balanced.

## Requirements

Codex must have access to its built-in image generation tool and the Presentations skill. Regional color sampling uses Pillow. The workflow discovers the available runtime through `load_workspace_dependencies`. It can use Humanizer-zh for copy editing when that skill is installed.

This repository contains instructions and helper tools. It does not include Codex, model services, or account quotas, and installing it does not add those capabilities. Fonts, tool versions, and models can affect the result.

## Files and entry points

```text
.agents/plugins/marketplace.json   Catalog that lets Codex find the plugin
.codex-plugin/plugin.json         Plugin name, version, and skill location
skills/personal-ppt/SKILL.md       Presentation workflow
skills/personal-ppt/scripts/      Checks and helper tools
skills/personal-ppt/references/   Schemas, workflows, and attribution
skills/personal-ppt/assets/       Technical example and palette references
```

The marketplace catalog is a repository configuration file. You do not need to purchase it, and it does not mean the plugin has passed review for the official public directory. Creating the file has no nationality or location requirement. Codex service availability and account requirements apply separately.

## Limitations

Rebuilding editable objects from an image still requires measurement and visual calibration. Scripts can catch some structural, text, and color issues, but they cannot establish scientific accuracy or judge every layout. Complex raster illustrations are replaceable images, not fully editable vector paths.

`assets/example-spec.json` is a synthetic technical example, not a finished project that has completed the image-generation and review workflow.

## Attribution and licensing

See [sources.md](skills/personal-ppt/references/sources.md) for borrowed methods and scope, and [sources.lock.json](skills/personal-ppt/references/sources.lock.json) for pinned revisions. Upstream license files are included; palette sources have separate license notices. Read [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for details.

Installation follows OpenAI's [plugin documentation](https://developers.openai.com/plugins/build/plugins) and [skill documentation](https://learn.chatgpt.com/docs/build-skills).
