# personal-ppt

[English](README.md) | 简体中文

一个用于制作可编辑演示文稿的 Codex 插件，适用于工作汇报、商业方案、教学培训、产品介绍、科研汇报和个人展示。它先生成并展示每页设计图，再重建为 PowerPoint。

当前版本 **2.0.0**。

## 制作流程

1. 阅读要求和材料，确定受众、用途，以及这份 PPT 要讲清什么。
2. 起草并精简页面文案，将演讲备注、制作记录与正文分开。
3. 生成并展示母版设计图。自动模式自行选型并继续；你要求先看样张时，等待你选择。
4. 按所选母版和真实素材生成、展示每页设计图。
5. 建立原生 PPT 母版，逐页重建，检查实际导出结果并修正具体问题。

文字、表格、有数据的图表和简单流程结构尽量使用可编辑对象。照片与复杂插画作为独立图片，可以移动或替换。原数据和真实证据图片优先，不用生图结果冒充原材料。

真实素材的比例与设计图不同时，插件可以调整图区、文字和间距。它会结合实际 PPTX 与逐页渲染，检查对齐、混排文字加粗、语义换行、颜色和元素遗漏。

## 2.0 改了什么

- 内容规划适配不同受众和用途，科研附加要求只用于科研任务。
- 文案在生图前定稿，制作提醒留在后台；推测表达不再靠固定关键词通过检查。
- 配色和布局根据主题、受众和品牌选择，期刊参考色板继续保留。
- 自动模式内部完成母版选型和样页检查；先看样张模式保留你要求的确认步骤。
- 新项目使用 workflow_version 2.0，旧项目保留原设置和验收要求。

制作路线保持不变：每页先内置生图并展示，再重建可编辑 PPT。中文使用**微软雅黑 Microsoft YaHei**，英文使用 **Times New Roman**；字号按内容与排版判断，同角色全套统一。

## 安装插件

在支持插件命令的 Codex CLI 中运行：

```shell
codex plugin marketplace add Yi-Wang798/personal-ppt
codex plugin add personal-ppt@personal-ppt-marketplace
```

第一条添加本仓库的市场目录，第二条安装插件。安装后重新打开 Codex 或新建聊天。支持仓库市场的桌面客户端，也可以添加本仓库，在列表中安装 `personal-ppt`。

插件已包含技能，不必再安装一份同名独立技能，以免重复显示。

## 只安装技能

在 Codex 中发送：

```text
使用 $skill-installer，从 Yi-Wang798/personal-ppt 安装技能，
仓库内路径是 skills/personal-ppt，保留完整文件夹。
```

也可以点击 GitHub 的 **Code → Download ZIP**，解压后将完整的 `skills/personal-ppt` 文件夹放入 `~/.agents/skills/personal-ppt`。Windows 对应 `%USERPROFILE%\.agents\skills\personal-ppt`。保留 `SKILL.md` 旁的 `scripts`、`references` 和 `assets`；未识别时重启 Codex。

## 使用

```text
使用 $personal-ppt，根据这些材料制作 12 页商业汇报。
每页先生图并展示，再制作可编辑 PPT，直接完成。
```

```text
使用 $personal-ppt，制作课堂教学 PPT，先给我看母版样张再继续。
```

你可以指定受众、时长、页数、语言和品牌要求。插件会结合材料判断其余信息，缺失内容会影响结果时再询问。

## 运行条件与限制

Codex 需要能调用内置生图工具和 Presentations 技能。运行时通过 `load_workspace_dependencies` 发现，区域取色使用 Pillow。已安装 Humanizer、Humanizer ZH 时可辅助文案编辑；工作流也自带文案说明。

仓库提供流程和辅助脚本，不附带模型权限、订阅或生图额度。图片到可编辑对象仍需要测量与视觉校准。内部检查用于减少返工，不能保证所有任务首轮都完美；复杂插画的内部像素也不能逐路径编辑。

`assets/example-spec.json` 是旧布局协议的合成示例，不是完成整套生图流程的作品。2.0 脚本回归结果见 [validation-v2.md](validation-v2.md)。

## 仓库结构

```text
.agents/plugins/marketplace.json   市场目录
.codex-plugin/plugin.json         插件元数据
skills/personal-ppt/SKILL.md       主流程
skills/personal-ppt/scripts/      检查与辅助工具
skills/personal-ppt/references/   场景、文案、设计与重建说明
skills/personal-ppt/assets/       技术示例与可选配色
```

市场目录是可自行创建和分享的配置文件，不需要购买；它与进入官方公共插件目录的审核分开。Codex 服务本身的地区可用性和账户要求另行适用。

## 来源与许可

来源和整合范围见 [sources.md](skills/personal-ppt/references/sources.md)、[sources.lock.json](skills/personal-ppt/references/sources.lock.json) 与 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。2.0 选择性借鉴文案和设计方法，不把多套外部改写服务串联进制作流程。

安装参考 OpenAI 的[插件说明](https://developers.openai.com/plugins/build/plugins)和[技能说明](https://learn.chatgpt.com/docs/build-skills)。
