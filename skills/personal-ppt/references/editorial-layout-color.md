# 文案、组合布局和参考图取色 v1.7

流程：材料核实 → 科研叙事 → Humanizer 精简 → 文案定稿与独立审核 → 母版/分页生图 → 组合排版及原生重建 → 内容、排版、颜色三项验收。v1.6 的灵活调整仍有效；新规则解决布局看似不越界却不好读、整体偏心和文案上错层的问题。

## 先定稿，再生图

从当前 skills 列表发现并读取已安装 humanizer-zh。只借用删除填充语、重复概括、编辑口吻、抽象总结、直接表达等方法。科研 PPT 不引入幽默、个性表演、随意改术语、为避免三段式硬改真实三项结果、自动删科学限定或机械删除强调字重。Humanizer 不可用时按本文直接精简并说明实际使用的方法，不自动安装外部依赖。

三类文字分流：
- slide-body：研究内容、方法、结果、来源引用，以及读图必需的条件/局限。
- speaker-notes：口头展开的解释，按用户或项目设置写入备注。
- production-record：未知定义、待补数据、核对事项、重绘限制、制作提醒，保存到 build/production-records.json 或补充清单，默认不上屏，也不自动进演讲备注。

spec.elements 仅包含可见页面对象，text 的 text_channel="slide-body"，content_role 为 research/reader-condition/navigation/caption/citation。speaker_notes、production_records 保存在各自字段/文件，不放进 elements，也不进入生图准确文字清单。单位、样本量、误差线、统计符号、公式定义等读图必需信息保留；不能用去 AI 味掩盖未知数据。未知值记录为待补，正文不能编造已确认数值。

说明直接写做了什么、怎样做、观察到什么；不默认加“当前解释”“为确保”等制作口吻和每页免责声明。若属于推测，claim_type=inference 并用“可能”“提示”等准确限定，不把推测升级为证实因果。确需显示待核实条件时，content_role=reader-condition、source_ids 和 editorial_exception.reason 记录科学必要性，避免关键词扫描机械删除真实局限。

每个 component 的标题、说明只各承担一个信息功能；用 editorial_groups:[{element_ids:[...]}] 关联并检查重复。“来源可追溯/单克隆来源证据/保留完整来源与成像记录”这样的近义堆叠由实际复读识别，保留最具体的一层，不为填版面补文字，允许留白。规则脚本只检测确切重复和常见制作口吻，不能理解所有近义重复。

```text
<python> scripts/editorial_tools.py audit --spec <deck-spec.json>
```

在 build/content-review.json 保存 status=pass、content_sha256（audit 输出）、channels_reviewed/scientific_details_preserved/redundancy_reviewed/semantic_wrap_reviewed=true、observations（具体改写及保留事项）。这个审核必须来自实际核对，不由脚本自动勾选。文字、数据或用途改变后审核失效；仅改变颜色/坐标不会使内容审核失效。分页 prompts 与生产预检对新项目检查该记录。母版候选也在文案审核后生成，不能先把未定稿的制作文字画进去。

## 句子与换行一起设计

短说明优先完整一行。必须换行时先按语义写 semantic_lines，拼接后与定稿 text（去换行）完全相同；人工硬换行需 line_breaks 与实际 PPT 输出一致。不把单位与数值、术语、括号或孤立标点拆开；不能仅因文本框装不下就插斜杠或回车。语义是否完整仍需复读。

若短标签与正文并列，优先拆成独立标签和正文对象，正文各行共享同一起始位置，别让第二行回到标签的最左端。需要悬挂结构时 paragraph.continuation_indent_px 指定段落左缩进，检查实际 OOXML marL；多行软换行、字形基线和缩进的视觉关系通过最终渲染观察。生图提示词采用已定稿的句子与布局意图，不把生成图中文字当准确内容。

## 整体组件与跨组件布局

component_groups 每项 id、element_ids、container_box、center_axis。把“图标+标题”按全部成员的联合边界整体居中，不再给图标和文本各设固定偏移；成员之间的间距按文字真实宽度设计。标题单独居中不等于整个组合居中。

component_constraints 的 kind 为 equal-width/equal-height/equal-horizontal-gap/common-top/common-bottom/common-center-y，element_ids 为实际 PPT 对象。三张同级卡片默认等宽、等间距；标题、分隔线和正文起点分别成组对齐。不是所有正文必须居中：短标签可居中，较长解释可左对齐；不同字数不靠缩字号强塞一行，也不为行数一致补废话。

这些检查从成品对象坐标提取，不能只检查手填容器。共同 top/bottom 是原生几何检查，不能冒充字形真实基线；正文行数、视觉基线、组合重心和留白通过清洁渲染复查。源图不适合时沿用 adaptations 的灵活调整机制，记录具体原因。

## 从参考区域读取颜色

使用当前 load_workspace_dependencies 提供的 Python/Pillow，只读原图像素，不编辑图片。样区从已确认母版或当前冻结设计图中选择实际纯色内部，记录 x/y/w/h、用途、图像 SHA256、RGB/HEX；避开文字抗锯齿、阴影、压缩边缘。正文取色须选字形内部，不能拿大面积白背景的主色当文字色。工具用小区域不透明像素的主导 RGB，低占比时要求换样区或判定为复杂色，不强行输出一个平均颜色。

```text
<python> scripts/color_sampler.py sample --image <参考图.png> --region X Y W H --role title-blue --out <新的取色结果.json>
<python> scripts/color_sampler.py check --spec <deck-spec.json>
```

将单项输出原样汇入 design/color-samples.json 的 samples。master.tokens.color_roles 使用这些实际取样值；runs.color_role 和 visual_style.fill_role/stroke_role 引用它，文字与线条不各自猜色。全部可见的原生文字/填充/描边角色进入清单；独立原始证据图片不改色。采样结果过期或原图改变需重新检查。

渐变和半透明不能用单一吸管值冒充。把背景、透明度、渐变多个实际色段分别记录并视觉核查，必要时保留无正文的独立背景素材。半透明区域显示出来的合成 RGB 不等于源前景 RGB；工具不会逆推出未知透明度。复杂效果先说明实现方式，不静默铺成纯色。

## 三项独立验收

content-review 可同时保存 audit 输出的 page_sha256，用于一页 sample-spec 子集复用对应定稿审核，避免样页流程因全套哈希不同而循环受阻；正式全套仍检查完整 content_sha256。

visual-review 每页 review_sections 包含 content/layout/color，各含 passed 和 observations。内容查正文用途、科学限定、重复、语义断行；排版查组件整体、等宽等距、标题/分隔线/正文起点及实际软换行；颜色查真实取样角色、图中文字/线色和来源图片原配色。每页还需保留实际渲染、并排/叠图与原有 blockers，不能因结构 pass 或文本框不越界就判整页美观。

脚本不自动证明 Humanizer 执行、科研内容正确、软换行合理、渲染 provenance 或所有复杂色效果准确。三项记录必须源自真实查看，不允许生成一串没有观察依据的 passed=true。
