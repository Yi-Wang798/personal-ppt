# 可编辑制作

2.0/2.1 的交互、逐页生图、样页与交付要求以 SKILL.md、master-reconstruction.md、fidelity-gates.md 为准。以下为构建细节，不增加用户批准节点。

## 原生重建

按 master-reconstruction.md 选定母版并制作原生 master/layout，分页复制/继承，插入临时底图逐项测量重建，复杂元素独立生图插入，最后移除底图。

2.1 新项目读取 [原生转换接入](native-bridge.md)，使用随 skill 固定版本的 PPT Master 几何转换及统一 native_bridge 封装；不拼接多个 PPTX 导出引擎。旧项目保留原构建方式。读取当前 Presentations 的 SKILL.md，用 load_workspace_dependencies 发现实际运行时与包目录，用 Presentations 导入最终文件进行渲染检查，不再次导出替换原文件。

构建源保存在 build/，准确文字与数据在 spec。按当前 API 编写；画布和 box 是 CSS px，字号使用 pt 或明确转换为 px，不能粘贴外部 inch 坐标。

默认中文使用微软雅黑（Microsoft YaHei），英文使用 Times New Roman。混排文本按文字段分别设置字体，图表、表格及节点同样遵循。母版阶段按参考图自主确定字号并记录到 master.tokens.text_styles；确认后同角色全套固定。分页通过 master_slot 继承，不逐页随意缩放标题或更改字重/对齐。

重建顺序：

1. 查看真实样张，分清背景、文本、证据、语义结构、独立插画。
2. 用真实 reference_size、image_frame 和 reference_box 测量位置、大小、焦点、行距与层叠，记录完整 reference_inventory。借助临时底图校准，不只描述“图文比例相近”。内容正确性/可编辑性引起的必要差异须具体记录，不能把大幅偏移或遗漏当作微调。
3. 创建原生文字、表格、图表、语义节点与连接线。每个约定对象名称 `pppt:<slide-id>:<element-id>`；chart/table 名称在 graphicFrame 的 cNvPr，使用当前 API 的真实名称字段。API 不暴露名称时，导出草稿后运行 `ppt_tools.py bind --spec <spec> --pptx <草稿> --out <新的命名候选>`，按原生类型、准确文案和坐标唯一匹配，容差 3px；只写元数据，不创建或替换内容。把命名候选交给正式 finalizer。歧义时修正布局或 API 对象命名，不猜对象。
4. 插入独立素材；无文字背景可铺底，原图保持比例。纯装饰和复杂插画使用生图或来源图片，不把流程图编辑例外扩大为程序绘制装饰。
5. 来源按引用需要写入页面或项目来源记录；演讲备注按用户或项目设置写入，制作提醒不自动进入备注。正式导出后渲染成品。

文本保留合理段落，不拆成逐字对象。图表使用原始 categories/series，为轴、图例、标签分别设置字体和单位。表格不转图片。连接线有明确方向，靠近对应节点边界。

2.1 的 native_bridge 根据 spec 中明确的字面数据嵌入 Excel 工作簿；检查实际关系和数值。2.0 旧项目继续在其正式 finalizer 中显式设置 `materializeLiteralChartWorkbooks: true`。编辑现有图表若需要保留公式或原工作簿血缘，不以字面快照替换，按 Presentations 的 native_evidence 流程保留原工作簿。流程线的 head/tail 分别对应起端/终端，不能凭名称猜箭头方向，必须看渲染结果。

复杂插画内部像素不可编辑，只能移动/裁剪/替换；用户要求编辑路径时需另行矢量重建并说明范围。截图图表没有数据时保留原图或取得准确数据，不猜柱高。inspect 只查原生类型和准确文字，不能证明连接附着、视觉质量或数据语义正确；这些仍需正式检查与视觉审阅。

本 skill 是 Codex 可执行工作流，辅助脚本不是无人判断的自动图片矢量化程序。


参见 [设计合同](design-contract.md)：构建源读取 spec，不复制另一套坐标；预览与导出共用构建模型。母版固定外框，内容布局按证据选择。inspect 从实际成品输出 conversion_trace，不支持的核心元素需改用明确原生或独立图片路线，不得略过。


先检查代表性复杂样页再批量，参见 [还原验收](fidelity-gates.md)。构建读取独立测量转录后的 spec；段落/分段颜色、粗斜体、字号、内边距逐项设置；面板、色带、内白底、横线、箭头逐层建立，不能单个矩形代替。每个裁剪素材先独立预览，等比优先，证据保持原图。能力缺失先说明并解决，不能删除元素或生成简化参考图替换。
