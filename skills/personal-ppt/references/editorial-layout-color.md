# 文案、组件与取色 2.0

先读 natural-copy.md，按任务起草准确文案并轻量精简。保留已有术语、事实、数字、因果和判断强度，不用固定关键词证明严谨性。真实需要的限定保留，不反复堆叠提醒。中文与英文使用对应的已安装 Humanizer 方法；不为了“像人”增加幽默、故事或数据。

正文、演讲备注、制作记录分开。slide-body 只含本页内容、图注、导航、引用和读图必要条件；speaker_notes 按请求写口头补充；production_records 保存缺失定义、待核对事项和技术限制，默认不上屏、不自动进备注。

spec.elements 只包含可见对象。text.text_channel="slide-body"，content_role 为 research/reader-condition/navigation/caption/citation，research 沿用为主体内容角色名。非 text 的标签、表格和图表文字也不能夹带制作记录。读图必要条件可用 reader-condition，记录 source_ids 与 editorial_exception.reason，不以关键词扫描删除真实前提。

运行 editorial_tools.py audit 后实际复读。2.0 文风提示为建议，不设置 AI 味分数；制作记录上屏、无效字段、文字遗漏和事实变化须先修正。content-review.json 保存 status=pass、content_sha256、channels_reviewed/facts_preserved/claim_strength_reviewed/redundancy_reviewed/semantic_wrap_reviewed=true 和具体 observations。材料、用途或文字变化后重新复读，不能自动打勾。

组件每层承担不同信息功能，不在标题、副标题、正文与总结条重复同一意思。允许留白，不为凑满三张卡片添字。固定三项、问题标题或纯文字页按表达需要保留。

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
