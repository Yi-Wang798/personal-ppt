# 设计稿、页面节奏与科研校验

v1.4 借鉴 academic-ppt-master 的规范锁、页面节奏和转换追踪。保留内置生图和原生 PPT 引擎，不集成其 SVG 转换器。

## 同源设计稿

母版图确认后先规划全套内容布局，再逐页生图、测量。deck-spec.json 的准确文案、box、reference_box、字体、素材路径与连接关系就是可编辑设计稿；不从生成图片重新抄录数值。构建程序从该文件读取数据，不再维护另一份手写坐标表。使用同一构建模型渲染预览和导出 PPT，最终仍需查看实际 PPT 渲染。图片到设计稿需要人工视觉测量，本工具不自动识别图片元素。

保持先建立原生母版并校准样页的流程。允许分阶段施工，全部页测量完成后冻结正式设计稿；母版模板路径等构建字段先填真实值，再冻结。每页施工前读取 build/design-lock.json 以及本页 spec，不能凭记忆设置配色和字号。最后生产预检核查设计稿没有漂移。

```text
<python> scripts/design_contract.py freeze --spec <deck-spec.json>
<python> scripts/design_contract.py check --spec <deck-spec.json>
```

项目顶层 workflow_version="1.4"。freeze 不覆盖已有锁；修改内容或测量布局后同步构建源、重渲染、重新校准，再用 freeze --replace。实质风格变化仍需母版重新确认。旧项目按本次修改范围迁移，不要求重制未修改页。

## 统一外框，多种内容布局

将母版 tokens（配色、中文微软雅黑、英文 Times New Roman、同角色字号、外框）与 layout_catalog（内容区域布局）分开。layout_catalog 可记录 id、用途和槽位；槽位坐标由已确认母版测量取得，没有全局固定数值。根据材料选择 evidence-figure、mechanism、comparison、data-table、takeaway 等布局，不能为了多样性改乱严谨证据。

每页 layout_family 指向选定布局，page_rhythm 为 anchor（封面/结构导航）、dense（数据/多证据）、breathing（单一结论/大图/留白）。维持统一标题、页脚和文字层级，内容区随证据调整；不要求机械交替或强行增加过渡页。生图前把本页布局意图与节奏加入提示词，不能测量完才改节奏。

## 转换追踪

ppt_tools.py inspect 报告每页 conversion_trace，记录 element_id、期望类型、实际类型、PPT 对象名/ID、参考组件 ID、实际 box 与 missing/mismatch/verified 状态。记录从成品 OOXML 提取，不由作者手填成功。文字或坐标检查错误标记 mismatch；没有对象标记 missing；缺少可测位置或字号继承时附带 pending_visual_checks，必须看最终渲染。

原图清单 reference_inventory 仍是覆盖依据。图表/表格必须为原生 chart/table，不能以可编辑的独立形状替代数据编辑能力。复杂图仍采用独立来源图片或内置生图素材。

## 科研内容与数据

根据用途选择 narrative_mode：paper-reading 可参考背景与目的、技术路径、结果、讨论、展望；research-progress 按问题、进展、证据、未解决问题、下一步组织；defense 按学校要求组织。不把五模块硬套所有演讲。

每个结果页关联准确来源的结论与证据；结论式标题适用于新撰写标题，用户给定标题不擅改。讲稿区分作者结论、我们推断、局限及对用户研究的意义，不虚构科研关联。资料默认复制到项目，保留原文件。

对含数据的页，在 build/data-review.json 记录页/元素 ID、source_ids、逐项核对的数据、单位、坐标轴范围、对数/线性尺度、误差线含义和实际发现。先比较 spec 与原数据，再比较导出图表缓存/嵌入工作簿与 spec；仅从 SVG 或成品标签自证数值正确不够。有数据驱动的自定义形状时用明确公式计算位置，核对实际坐标，不凭看起来相似绘制。截图无准确数据则保留原图，不猜数。

公式检查符号、上下标、分式、单位。工具支持原生公式则优先；复杂公式需清晰独立素材并保留 LaTeX 源，明确内部不可编辑。不要强制把所有公式转 PNG。每页视觉检查默认必做，不能只检查设计稿而不看实际 PPT。


v1.5 使用 fidelity-gates.md 补足独立测量与交付阻断；设计锁只防漂移，不能证明初始坐标/样式正确。新项目先冻结参考、测量全套，再做复杂样页验收，最后冻结 spec 批量构建。1.4 旧项目按修复范围迁移，不利用旧版本字段绕过新项目检查。


v1.6 更新优先于本文旧版的机械坐标/差异清零约束：参考保留原样，允许授权范围内按真实素材、可读性、居中和均衡纠正布局；记录 adaptations 的原始 before 与目标 after，未解决问题仍阻断，合理调整可作为已解决差异。新增 alignment_constraints、paragraph.vertical_alignment 与 emphasis_scope=all，核对实际 PPT；完整字段与调整边界见 [灵活排版](adaptive-layout.md)。新项目 workflow_version="1.6"。


v1.7：生图前完成正文/演讲备注/制作记录分流、Humanizer 有限精简与独立文案审核；新增 semantic_lines、component_groups、component_constraints、editorial_groups、continuation_indent_px；颜色逐角色区域取样并链接母版；最终独立 content/layout/color 三项验收。新项目 workflow_version="1.7"，规则与命令见 [文案、组合布局和取色](editorial-layout-color.md)。保持 1.6 的可追溯灵活调整，不能用新规则强制机械复刻。
