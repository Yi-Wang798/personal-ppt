# 来源与许可说明

本仓库公开发布 personal-ppt 2.0.0 的工作流程和辅助工具。
上游项目的原始许可及来源声明保存在
`skills/personal-ppt/references/licenses/`。

## 参考方法

- Frontend Slides、MiniMax skills、Presentation Skill、Codex PPT Skill：MIT，借鉴所需工作流程与设计方法。
- Academic PPT Master：MIT；该项目注明引擎来源为 Hugo He 的 PPT Master。保留其 MIT 与 ATTRIBUTION 文件，1.4 版本未集成其完整 SVG 导出引擎；2.1 的实际接入见下方。
- AI Illustrator Workflow、Humanizer-zh：借鉴局部重建或表达精简方法，未复制其全文或运行实现。

## 配色资料

`assets/journal-palettes.json` 的部分色值来源于 ggsci。
其来源标注为 GPL-3.0-or-later，原始许可一并保留；未移植 R 绘图实现。

本仓库尚未另行指定统一的主许可证；上游材料按其各自许可和来源声明标注。
不要将仓库公开可见视为统一 MIT 授权。

2.0 的通用场景、文案与设计方法参考范围见 sources.md 与 sources.lock.json；新增实现由本项目编写，未复制外部改写或检测引擎。

## PPT Master native conversion dependency (2.1)

Copyright (c) 2025-2026 Hugo He. Licensed under MIT. Upstream: https://github.com/hugohe3/ppt-master, commit 604ecdec8dd6a0405e1abdb49565430902373276.

The dependency subset under skills/personal-ppt/vendor/ppt-master is copied without modifying upstream files. Its LICENSE, original SKILL metadata, attribution integrity checks, sponsor documents required by those checks, and data notices are preserved. The six composition reference SVGs under assets/components/upstream come from the same commit. These are reference assets, not alternate production workflows.

See vendor/ppt-master/vendor-manifest.json and assets/components/index.json for individual file hashes. The preset-shape data also retains its original Apache 2.0 / Open XML SDK license and notice files under vendor/ppt-master/scripts/pptx_shapes/data. No trademark or upstream endorsement is implied.
