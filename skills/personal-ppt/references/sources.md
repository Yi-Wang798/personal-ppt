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

v1.3 按用户明确要求参考 [AI Illustrator Workflow](https://github.com/Yi-Wang798/ai-illustrator-workflow) 及其 underlay-reconstruction.md，只借鉴作者选择、底图等比像素映射、组件清单、母对象复用、分区域校准和清洁导出方法。未复制 Illustrator JSX 或几何构造代码；没有引入 Illustrator 运行依赖，PPT 原生 master/layout/placeholder 来自当前 Presentations 的 API。


v1.4 于 2026-10-12 借鉴 [academic-ppt-master](https://github.com/M1n-n9/academic-ppt-master)，固定提交 6825d33f2931b8894435b9bd25c08cfce3476ff0：规范锁、brand/layout 分层、页面节奏、转换 trace、科研叙事及数据坐标校验方法。该项目注明引擎来自 [hugohe3/ppt-master](https://github.com/hugohe3/ppt-master)。仅改写工作流方法，design_contract.py 和新增 OOXML trace 为本地新写；没有复制 SVG 转換器、模板库、生图 API 或其全部执行禁令。保留本地原生图表表格、默认视觉检查、原资料不移动和内置生图。MIT 及来源声明存于 licenses/。


v1.7 依据用户截图反馈，参考本机已安装 humanizer-zh 的保留含义、删除填充语、重复概括和协作口吻方法；未复制其全文或引入幽默/个性表演。editorial_tools.py、color_sampler.py 与组合检查为本地新写。颜色采样只读图片，使用当前工作区 bundled Pillow，不增加外部服务或付费 API。


## 2.0 通用化与文案设计参考

2026-10-19：按任务分流、逐页生图输入分离、内部样页检查和兼容代码为本项目新增实现。以下仅选择性参考方法，没有复制这些项目的脚本或完整 skill，也未引入去检测或删除来源标记的功能。

- [larashero3-dotcom/lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone)：体裁优先、最小改写、保留事实与判断强度。转换为生图前的中文轻量编辑，不照搬其冻结文章结构规则。
- [blader/humanizer](https://github.com/blader/humanizer)：重复结构、空泛拔高和聊天残留的识别；本次 README 实际使用本地 Humanizer 2.8.2 与 Humanizer ZH 0.1.0 润色。
- [daniel-bogale/anti-ai-writing-humanizer](https://github.com/daniel-bogale/anti-ai-writing-humanizer)：起草时保持自然、轻量编辑。未引入多轮检测引擎。
- [keez97/humanizer](https://github.com/keez97/humanizer)：保留必要限定的轻量模式；未采用评分门槛或模型检测器。
- [pbakaus/impeccable](https://github.com/pbakaus/impeccable)：按任务建立视觉层级，避免无目的套用界面卡片与装饰；只转化为幻灯片设计建议，未使用网页检测代码。
- [opitaru-sys/deck-dna](https://github.com/opitaru-sys/deck-dna)：参考设计特征与文字容量的观察方法；未复制其脚本或模板。

本次实现没有复制 Anthropic PPTX skill 的代码或专有许可文本；既有引擎与 upstream 许可保持原样。引用网页的项目自述不等于本插件经过成品质量验证。

## 2.1 实际代码接入

2026-10-22 集成 hugohe3/ppt-master，固定提交 604ecdec8dd6a0405e1abdb49565430902373276，MIT。范围是原生 SVG 几何转换及静态依赖闭包、预设形状数据和六个 presentation_core 构图参考。vendor/ppt-master/vendor-manifest.json 与 assets/components/index.json 记录文件与 SHA-256。原文件不改写，保留 LICENSE、SKILL 元数据、署名检查以及预设数据的第三方许可证。native_bridge.py 是本地新增适配层；文字、图片、图表、表格与母版由同一个 python-pptx 包封装。未接入整套上游交互、外部生图、动画或公式管线。此前版本仅借鉴方法的说明属于历史版本，不代表 2.1 的范围。
