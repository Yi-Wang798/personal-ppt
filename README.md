# 个人 PPT

简体中文 | [English](README.en.md)

个人 PPT 是一个面向 Codex 的科研演示文稿插件。它先生成设计参考图，再把文字、表格、数据图表和简单流程结构做成可编辑的 PowerPoint 对象。

当前版本：**1.7.0**。

## 它能做什么

- 整理研究材料，核对数据，把页面正文、演讲备注和制作记录分开。
- 生成母版候选供你选择，再按选定风格生成并展示逐页设计图。
- 优先使用你的原始实验图片、数据和机制图，保留主体、图例、刻度及科学含义。
- 重建可编辑 PPT；复杂插画作为独立图片插入，可以移动或替换。
- 按真实素材比例调整布局，检查居中、字重、语义换行、组件间距和参考颜色。
- 对照实际 PPT 渲染，分别检查内容、排版和颜色。

默认中文字体为微软雅黑（Microsoft YaHei），英文字体为 Times New Roman。字号在母版设计阶段按内容和排版确定。配色可参考 Nature、Science 等期刊风格，这些色板不是期刊官方 PPT 模板。

## 安装

推荐安装完整插件。插件已经包含技能，二者选一种安装即可。

### 安装完整插件

在支持插件命令的 Codex CLI 中运行：

```shell
codex plugin marketplace add Yi-Wang798/personal-ppt
codex plugin add personal-ppt@personal-ppt-marketplace
```

第一条命令添加本仓库的市场目录，第二条安装插件。重新打开 Codex 或新建聊天后使用。如果你的客户端没有 `plugin` 命令，可以采用下面的技能安装方式。

想在桌面插件目录中操作时，先添加上述仓库市场，再在插件目录选择 **Personal PPT**，找到“个人 PPT”并安装。不同客户端的界面名称可能略有区别。

### 只安装技能

在 Codex 中发送：

```text
使用 $skill-installer，从 Yi-Wang798/personal-ppt 仓库安装技能，
仓库内部路径是 skills/personal-ppt，请保留完整目录。
```

也可以从 GitHub 的 **Code → Download ZIP** 下载并解压，将完整的 `skills/personal-ppt` 文件夹放到用户级技能目录 `~/.agents/skills/personal-ppt`。Windows 对应 `%USERPROFILE%\.agents\skills\personal-ppt`。如果没有识别，重启 Codex。

不要只下载 `SKILL.md`，它需要旁边的 `scripts`、`references` 和 `assets`。已经安装插件时，不必再安装同名独立技能，以免重复显示。

## 使用

```text
使用 $personal-ppt，根据这份材料制作可编辑科研汇报 PPT。
先生成母版让我选择，再逐页设计和制作。
```

流程是：核实材料、定稿文案、选择母版、逐页设计、验收复杂样页、重建 PPT，最后检查并交付。插件会保留参考图和调整记录；当真实图片的比例与设计图不同，它可以调整图区、文字和间距，优先保证完整、清晰和匀称。

## 运行条件

Codex 需要能调用内置生图工具和 Presentations 技能。区域取色使用 Pillow；运行时通过 `load_workspace_dependencies` 发现可用环境。已安装 Humanizer-zh 时，插件可借用它的表达精简方法。

本仓库提供工作流程和检查工具，不附带 Codex、模型服务或账户额度。安装文件不会自动补齐这些能力。字体、工具版本和模型不同，也可能影响输出效果。

## 目录与两个入口

```text
.agents/plugins/marketplace.json   市场目录：让 Codex 找到插件
.codex-plugin/plugin.json         插件入口：名称、版本及技能位置
skills/personal-ppt/SKILL.md       技能入口：实际制作流程
skills/personal-ppt/scripts/      检查与辅助工具
skills/personal-ppt/references/   协议、流程和来源说明
skills/personal-ppt/assets/       技术示例与参考配色
```

市场目录是仓库内的配置文件，不需要购买，也不代表已经通过官方公共插件目录审核。创建这个文件不限制国籍或所在地；Codex 服务的地区可用性和账户要求另行适用。

## 当前限制

图片到可编辑对象仍需测量、重建和视觉校准。脚本可以发现部分结构、文字和颜色问题，但不能自动证明科研内容正确或每页都美观。复杂插画内部仍是像素，不能承诺逐路径编辑。

`assets/example-spec.json` 是合成技术示例，并非完成全部生图与验收的成品项目。

## 来源与许可

借鉴项目及整合范围见 [来源说明](skills/personal-ppt/references/sources.md)，固定提交见 [来源记录](skills/personal-ppt/references/sources.lock.json)。上游许可文件一并保留，配色资料的来源和许可单独标注。详情见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

安装方式参考 OpenAI 的[插件说明](https://developers.openai.com/plugins/build/plugins)和[技能说明](https://learn.chatgpt.com/docs/build-skills)。
