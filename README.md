# 个人 PPT · Personal PPT

面向 Codex 的可编辑科研 PPT 插件：母版选型、逐页 AI 设计、原生对象重建、灵活排版与质量检查。

当前版本：**1.7.0**。

## 主要特点

- **先设计后制作**：生成母版候选供用户选择，再按统一风格生成并展示逐页设计图。
- **保留编辑能力**：文字、表格、数据图表和简单流程结构采用原生 PPT 对象，复杂插画使用独立图片素材。
- **尊重原始材料**：优先使用真实数据、实验图片和机制图，保留科学内容、主体、图例与刻度。
- **灵活优化排版**：尽量还原参考设计，同时根据真实素材比例改善对齐、可读性和页面均衡。
- **文案先定稿**：区分页面正文、演讲备注与制作记录，精简重复表达，按语义设计换行。
- **分项质量检查**：检查元素完整性、字体与字重、组合居中、参考颜色，并结合实际渲染验收。

默认中文使用微软雅黑（Microsoft YaHei），英文使用 Times New Roman。提供 Nature、Science 等期刊启发的参考配色，不代表期刊官方模板。

## 工作流程

材料核实 → 文案定稿 → 母版选择 → 逐页 AI 设计 → 复杂样页验收 → 可编辑 PPT 重建 → 内容、排版、颜色检查 → 交付。

## 使用示例

```text
使用 $personal-ppt，根据这份材料制作可编辑科研汇报 PPT，
先生成母版让我选择，再逐页设计和制作。
```

插件入口为 `.codex-plugin/plugin.json`，技能入口为
[`skills/personal-ppt/SKILL.md`](skills/personal-ppt/SKILL.md)。
安装时保留完整的 `skills/personal-ppt` 目录，按当前 Codex 支持的技能或插件安装方式加载。

## 依赖与目录

依赖 Codex 中可用的内置生图工具与 Presentations 技能；运行时通过
`load_workspace_dependencies` 发现。区域取色使用 Pillow。
已安装 Humanizer-zh 时可借用其表达精简方法，不把它的所有写作建议套用到科研内容。

```text
.codex-plugin/             插件元数据
skills/personal-ppt/
  SKILL.md                技能入口
  agents/                 调用信息
  references/             工作流程、协议与来源
  scripts/                预检、重建核查、文案与取色工具
  assets/                 技术示例与配色参考
```

## 当前边界

插件采用设计参考与逐项重建流程，图片到可编辑对象仍需测量和视觉校准。
辅助脚本不等同于自动图片矢量化引擎；结构检查通过不能代替科学核对或真实视觉验收。
`assets/example-spec.json` 是合成技术示例，并非完成全部生图与验收的成品项目。

## 来源与许可

借鉴项目、固定提交与整合范围见
[`sources.md`](skills/personal-ppt/references/sources.md) 和
[`sources.lock.json`](skills/personal-ppt/references/sources.lock.json)。
保留各上游项目的许可文件；期刊参考配色的来源和许可单独标注。
详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
