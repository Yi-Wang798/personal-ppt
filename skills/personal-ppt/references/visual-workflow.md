# 生图与视觉流程

## 默认逐页流程（v1.2）

v1.3 先按 master-reconstruction.md 生成母版候选并等待用户明确选择；未经确认不进入分页生成。每次分页调用都把确认母版图作为实际图像输入，design_generation.master_sha256 与母版哈希一致。原数据和原机理流程图优先作为严格输入，母版仅约束视觉风格。

新任务默认 per-slide。必须实际调用当前内置 imagegen，为每页输出完整设计参考图；prompts 命令只是准备任务，不能代替调用。读取当前 imagegen 技能，按工具真实支持的参数生成，不要求 API 密钥。先完成一页可重建性检查，再生成其余页。

每页保存到项目 design/ 并记录 design_reference、reference_size、image_frame、reference_inventory 和至少 3 条 design_features。design_generation 包括 backend="built-in-imagegen"、实际 tool、prompt_path、image_sha256、master_sha256、displayed=true、display_method（tool-inline 或 markdown-inline）。只有图片已显示后才能记录 displayed=true，不能伪造回执。

显示每页设计图并注明页码，页数多可按小组展示，不必每页停下来确认。联系表可作全套浏览，但不能用一次文字“已生成”替代图片显示。autonomous 显示后继续；review 按用户要求等待。内置生图不可用/失败时报告该阶段受阻，不转而偷偷直接做 PPT。

完成设计后执行 production 预检；制作前 view_image 查看对应设计文件，再按图构建。每页最终原生渲染对照自己的 design_reference；生成图中的错误文字和数据仍以准确 spec 修正。

脚本检查真实文件、哈希及声明记录，不能独立证明工具调用或用户实际看到图片，agent 必须从真实工具结果和聊天显示生成记录。不得为通过检查将 PPT 渲染图、原材料截图或占位图标成内置生图产物。

代表性模式：先规划准确文案与对象，只写布局意图、不锁定坐标。按 scientific-design.md 选择期刊参考色板和全套构图节奏；未知风格的 2–3 个候选需有结构差异。生成代表性正文样张，必要时补封面/数据页，通常 1–3 张。风格探索只对代表页做候选，不为每页重复探索。

调用现有 imagegen 并采用内置工具。prompts 命令输出逐页设计提示词和独立无文字素材提示词，不调用 API。用户要求先选样张时展示候选并等待；已指定风格则直接用。默认 autonomous 时自主选择、展示真实样张后继续，不逐阶段增加批准。

representative 仅在用户明确要求只做代表性样张时使用，仍要求真实调用与图片显示。默认 per-slide，保持配色和视觉语言、构图随内容变化，每页 design_reference 对应自己的真实生图。

样张提示词包含比例、受众、准确文案/表格/节点/图表数据、布局意图、颜色角色、字体、密度、主视觉和输入图角色。默认不继承原材料的外观；原材料的证据图可保留。数据图表样张只作设计参考，最终以原始数据创建原生图表。长正文不需要在样张精准呈现每字；最终文案以 spec 为准。

选定样张后更新 box、字号、layout_family、treatment 和 design_features；不把一张正文样张机械复制成所有页面。成品保持设计特征时也要保持全套论证节奏，必要的同构实验对照可保持一致。

选定样张后，背景、插画、cutout 独立生图。背景要求无正文、无数字、无图表标签，主图避开文本区；透明素材请求真实透明背景。禁止裁切带正文的整页图再覆盖原生文字。

严格论文原图、实验图、logo 在最终 PPT 直接嵌入原文件，保留比例，不让模型替换成近似图。只有图像没有数据时不声称标签和曲线可编辑。

编辑本地图片前通过 view_image 实际查看；按内置工具支持的 referenced_image_paths 传本地输入，缺少路径才使用最小必要近期图片数量。明确标注“风格参考”和“严格证据”，不混用。

将工具产物复制到项目 design/ 或 assets/，记录真实路径、提示词、实际工具方式和用途。不伪造生成记录或模型名称，不将仅有的任务文件当生成成功。内置生图失败时有针对性重试；重复故障报告限制。只有用户明确选择 API 后才采用现有 imagegen 的 CLI 路径。


v1.7：生图前完成正文/演讲备注/制作记录分流、Humanizer 有限精简与独立文案审核；新增 semantic_lines、component_groups、component_constraints、editorial_groups、continuation_indent_px；颜色逐角色区域取样并链接母版；最终独立 content/layout/color 三项验收。新项目 workflow_version="1.7"，规则与命令见 [文案、组合布局和取色](editorial-layout-color.md)。保持 1.6 的可追溯灵活调整，不能用新规则强制机械复刻。
