# 来源与整合范围

获取日期：2026-10-10。以下来自实际读取的 GitHub 源码；固定提交和文件哈希另存 sources.lock.json。只吸收所需方法，没有安装或执行这些项目的完整插件、构建脚本或生图 API。

| 项目 | 固定提交 | 读取部分 | 在本 skill 的用途 |
|---|---|---|---|
| [Frontend Slides](https://github.com/zarazhangrui/frontend-slides) | 9906a34d640d2111f724544cbc50f7f130569ae1 | SKILL.md 的视觉探索/密度，STYLE_PRESETS.md | 代表页样张、统一视觉系统、按演讲与阅读区分密度；不复制 HTML/CSS 引擎 |
| [MiniMax skills](https://github.com/MiniMax-AI/skills) | 60aaae52bb2af8162732751a4332f62a5fef518b | pptx-generator/references/design-system.md、pitfalls.md | 中文字体、配色、间距层次和复查思路；示例采用 Education & Charts 配色；不继承其 inch 坐标、PptxGenJS 和所有风格禁令 |
| [Presentation Skill](https://github.com/siril9/presentation-skill) | efd899c5ddf866af2ce0001c4c9340af775d4d55 | DESIGN.md、references/reproducible_workflow.md | 结构化内容源、快速预检、内容/视觉双检查、可重建项目；自写检查脚本，不复制其渲染器 |
| [Codex PPT Skill](https://github.com/ningzimu/codex-ppt-skill) | 85d4e629275e6c5793a33801d29b364383ea4c1e | SKILL.md、docs/outline-style-and-sample.md、docs/user-supplied-assets.md | 统一生图风格、样张参考、严格原图与风格参考区分；改为自主默认和原生重建，不继承整页图片交付、逐阶段批准和强制子 agent |

原有四个项目该提交根 LICENSE 均为 MIT，原文存于 licenses/。少量按需摘取的原始段落保存在 upstream-excerpts.md，仅作来源记录，不作为完整工作流执行。更长的本 skill 文档和 ppt_tools.py 为新写，来源方法已按当前环境和用户需求调整。

v1.1 于 2026-10-12 新增 [ggsci](https://github.com/nanxstats/ggsci) 的 NPG/nrc、AAAS/default、NEJM/default 色值子集，固定提交 37b74f85e62680b9d4523b0b4c0d9bfa0403d299。该项目许可是 GPL-3.0-or-later（区别于上述 MIT 项目），原始许可保存于 licenses/ggsci.GPL-3.0.md，色值来源和许可也写在 assets/journal-palettes.json；没有移植或运行 R 绘图实现。色板是期刊启发的社区参考，不称官方通用标准。

另参考 [Nature 概念图指南](https://www.nature.com/documents/natrev-artworkguide.pdf) 的层次、清晰标签、重点/背景和颜色可识别性；没有复制官方品牌色板或图稿。演示页面的中性色、角色分配和布局方案为本 skill 自写。

本地运行依赖：已安装的 imagegen 和 Presentations（当前运行环境提供）。它们没有复制进分发包，也没有修改。不要把本机缓存路径写成通用安装依赖；每次通过当前 skills 列表和 load_workspace_dependencies 发现实际路径。

当前通过 personal-ppt@personal 插件加载 skill，并提供相同内容的插件分发包。它不包含 Gamma/Canva 服务，也不声称已经连接这些账户。

v1.3 按用户明确要求参考 `AI Illustrator Workflow` 及其 underlay-reconstruction.md，只借鉴作者选择、底图等比像素映射、组件清单、母对象复用、分区域校准和清洁导出方法。未复制 Illustrator JSX 或几何构造代码；没有引入 Illustrator 运行依赖，PPT 原生 master/layout/placeholder 来自当前 Presentations 的 API。


v1.4 于 2026-10-12 借鉴 [academic-ppt-master](https://github.com/M1n-n9/academic-ppt-master)，固定提交 6825d33f2931b8894435b9bd25c08cfce3476ff0：规范锁、brand/layout 分层、页面节奏、转换 trace、科研叙事及数据坐标校验方法。该项目注明引擎来自 [hugohe3/ppt-master](https://github.com/hugohe3/ppt-master)。仅改写工作流方法，design_contract.py 和新增 OOXML trace 为本地新写；没有复制 SVG 转換器、模板库、生图 API 或其全部执行禁令。保留本地原生图表表格、默认视觉检查、原资料不移动和内置生图。MIT 及来源声明存于 licenses/。


v1.7 依据用户截图反馈，参考本机已安装 humanizer-zh 的保留含义、删除填充语、重复概括和协作口吻方法；未复制其全文或引入幽默/个性表演。editorial_tools.py、color_sampler.py 与组合检查为本地新写。颜色采样只读图片，使用当前工作区 bundled Pillow，不增加外部服务或付费 API。
