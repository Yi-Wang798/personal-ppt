# 原生重建

v1.3 以 master-reconstruction.md 为主要流程：先获母版选择并制作原生 master/layout，分页复制/继承，插入临时底图逐项测量重建，复杂元素独立生图插入，最后移除底图。不是从图片另作一套“类似”设计。

读当前 Presentations 的 SKILL.md、implementation、API_QUICK_START、finalization，使用 load_workspace_dependencies 返回的 Node/Python 与包目录。创建前遵守该技能的 operation-start 记录要求。第一版使用 @oai/artifact-tool，不运行下载项目脚本，不拼接 PptxGenJS 引擎。

构建源保存在 build/，准确文字与数据在 spec。按当前 API 编写；画布和 box 是 CSS px，字号使用 pt 或明确转换为 px，不能粘贴外部 inch 坐标。

默认中文使用微软雅黑（Microsoft YaHei），英文使用 Times New Roman。混排文本按文字段分别设置字体，图表、表格及节点同样遵循。母版阶段按参考图自主确定字号并记录到 master.tokens.text_styles；确认后同角色全套固定。分页通过 master_slot 继承，不逐页随意缩放标题或更改字重/对齐。

重建顺序：

1. 查看真实样张，分清背景、文本、证据、语义结构、独立插画。
2. 用真实 reference_size、image_frame 和 reference_box 测量位置、大小、焦点、行距与层叠，记录完整 reference_inventory。借助临时底图校准，不只描述“图文比例相近”。科学正确性/可编辑性引起的必要差异须具体记录，不能把大幅偏移或遗漏当作微调。
3. 创建原生文字、表格、图表、语义节点与连接线。每个约定对象名称 `pppt:<slide-id>:<element-id>`；chart/table 名称在 graphicFrame 的 cNvPr，使用当前 API 的真实名称字段。API 不暴露名称时，导出草稿后运行 `ppt_tools.py bind --spec <spec> --pptx <草稿> --out <新的命名候选>`，按原生类型、准确文案和坐标唯一匹配，容差 3px；只写元数据，不创建或替换内容。把命名候选交给正式 finalizer。歧义时修正布局或 API 对象命名，不猜对象。
4. 插入独立素材；无文字背景可铺底，原图保持比例。纯装饰和复杂插画使用生图或来源图片，不把流程图编辑例外扩大为程序绘制装饰。
5. 来源写进各页备注，演讲稿按请求写入。finalizer 后渲染成品。

文本保留合理段落，不拆成逐字对象。图表使用原始 categories/series，为轴、图例、标签分别设置字体和单位。表格不转图片。连接线有明确方向，靠近对应节点边界。

新建图表的完整字面数据已明确保存在 spec 时，在正式 finalizer 中显式设置 `materializeLiteralChartWorkbooks: true`，使图表带嵌入的 Excel 数据工作簿，并检查该关系有效。编辑现有图表若需要保留公式或原工作簿血缘，不以字面快照替换，按 Presentations 的 native_evidence 流程保留原工作簿。流程线的 head/tail 分别对应起端/终端，不能凭名称猜箭头方向，必须看渲染结果。

复杂插画内部像素不可编辑，只能移动/裁剪/替换；用户要求编辑路径时需另行矢量重建并说明范围。截图图表没有数据时保留原图或取得准确数据，不猜柱高。inspect 只查原生类型和准确文字，不能证明连接附着、视觉质量或数据语义正确；这些仍需正式检查与视觉审阅。

本 skill 是 Codex 可执行工作流，辅助脚本不是无人判断的自动图片矢量化程序。


v1.4 参见 [设计合同](design-contract.md)：构建源读取 spec，不复制另一套坐标；预览与导出共用构建模型。母版固定外框，内容布局按证据选择。inspect 从实际成品输出 conversion_trace，不支持的核心元素需改用明确原生或独立图片路线，不得略过。


v1.5 先复杂样页再批量，参见 [还原验收](fidelity-gates.md)。构建读取独立测量转录后的 spec；段落/分段颜色、粗斜体、字号、内边距逐项设置；面板、色带、内白底、横线、箭头逐层建立，不能单个矩形代替。每个裁剪素材先独立预览，等比优先，证据保持原图。能力缺失先说明并解决，不能删除元素或生成简化参考图替换。


v1.6 更新优先于本文旧版的机械坐标/差异清零约束：参考保留原样，允许授权范围内按真实素材、可读性、居中和均衡纠正布局；记录 adaptations 的原始 before 与目标 after，未解决问题仍阻断，合理调整可作为已解决差异。新增 alignment_constraints、paragraph.vertical_alignment 与 emphasis_scope=all，核对实际 PPT；完整字段与调整边界见 [灵活排版](adaptive-layout.md)。新项目 workflow_version="1.6"。


v1.7：生图前完成正文/演讲备注/制作记录分流、Humanizer 有限精简与独立文案审核；新增 semantic_lines、component_groups、component_constraints、editorial_groups、continuation_indent_px；颜色逐角色区域取样并链接母版；最终独立 content/layout/color 三项验收。新项目 workflow_version="1.7"，规则与命令见 [文案、组合布局和取色](editorial-layout-color.md)。保持 1.6 的可追溯灵活调整，不能用新规则强制机械复刻。
