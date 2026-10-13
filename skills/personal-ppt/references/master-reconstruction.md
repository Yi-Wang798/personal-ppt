# 母版优先与测量重建 v1.3

借鉴 AI Illustrator Workflow 的有用机制：审批参考 → 等比像素映射 → 底图定位 → 组件清单 → 主对象复用 → 分区域校准 → 清洁导出。只借鉴方法，不调用 Illustrator、不要求 .ai、不移植路径拟合/描边/布尔操作等不适合 PPT 的规则。

## 1. 用户确认的母版

默认提供 3 张编号母版图，由用户选择。每张体现完整的标题/正文/证据区、颜色、固定结构、字体层级和常用元素，数量可按用户要求调整。收到明确选择后记录 approval.confirmed=true、user_selection 原话、reference_sha256。已有用户确认母版可直接复用；上传内容 PPT 不自动成为已确认母版。

master 对象：id、reference_image、reference_size（真实像素 width/height）、image_sha256、approval、tokens（fonts.zh/fonts.en、text_styles 的角色→font_size_pt/bold/alignment）、ppt_template_path。选定母版时自主测量字号，经用户确认后同一角色全套固定，不能每页根据生成图再次随意改。中文微软雅黑、英文 Times New Roman 保持。

文字样式可额外记录 line_spacing、段前段后间距、文本框内边距和允许换行规则；同角色沿用这些值。可编辑文本的实际字形/基线需在叠图中校正，文本框矩形对齐不等于文字视觉位置对齐，不借用 Illustrator 的字形转轮廓方法来破坏 PPT 文字编辑性。

不强求所有内容页长得完全相同，但必须共享母版壳、文字层级和字号。确有图表/流程图等不同内容需要时，在同一母版体系内建立命名 layout；不逐页发明新主题。不为了“版式多样”破坏用户要求的母版统一。

## 2. 母版指导每页生图

每次生图必须将所选母版图实际传作参考输入；prompt 中描述母版不等于已传图。记录 design_generation.master_sha256，匹配所选母版。多轮可复用同一 style-only 图，避免仅参考上一页造成逐步漂移。

原始数据、原图和原机理流程图优先。原数据决定数值；原流程决定节点、状态、箭头方向和连接关系。母版决定呈现方式，不能改变科学内容。机制多步实体应保存身份、颜色/类别、状态、连接关系和出现次数，避免分页生图自行增删或重连。最终原图证据直接嵌入，生成图中数据重绘不得取代真实证据。

## 3. 原生 PPT 母版

读取 Presentations 的 master.spec.md、layout.spec.md、template_following.md 与字体/占位符文档。使用 presentation.masters.add、layouts.add、setParentLayoutId、slide.setLayout 和 placeholders；不是给普通页命名为“母版”就算完成。原生 master 统一主题/背景；layout 统一标题/内容占位符；常用组合构建一次后复制。

先构建 master 样页，叠入母版图校准位置、字号、对齐、边距、色彩及固定元素，再保存 build/master-template.pptx。pagination 重用同一 master/layout 或 duplicate 校准样页，主要替换准确文字、数据和图片，不重新设计固定对象。若原生导出不支持某个固定对象的继承，可复制同一经过校准的对象组，并如实说明；不要丢元素或虚称完整继承。

实测当前 API 的占位符实例化可能不保留预期位置。不同角色使用唯一 placeholder index；将母版坐标保存在统一 slots 合约，创建分页占位符后明确设置其 position 和 text.style，值一律来自母版合约而非逐页估计。导出后核查真实 XML/渲染位置，不能仅相信 setLayout。新建母版不照抄未验证的 setColorMap({bg1:'bg1'}) 例子，当前导出器会报该 token 不支持；默认色图可直接导出，特定主题映射需查当前支持值并验证。

## 4. 底图与坐标

每页插入完整 design_reference 作为临时图片对象，名称 `pppt:underlay:<slide-id>`，置于背景之上、重建对象之下。底图比例保持，使用统一变换，禁止横向纵向各自拉伸。

reference_size 为真实图像尺寸。image_frame 为图片在画布上的等比放置范围；reference_box 为每元素在源图上的 left/top/width/height。统一变换：x=frame.left+source.left×scale；y=frame.top+source.top×scale；w/h 同比例。不能以估算的 PPT 坐标冒充测量。source 与画布比例不一致时保留等比 letterbox/crop 映射，不能偷偷拉伸。

`reconstruction_tools.py map --reference-width W --reference-height H --frame X Y W H --box X Y W H` 输出换算 box。逐页 measured box 保存在 spec；构建时不另外重算一套近似值。位置容差以映射后的画布 CSS px 表示，默认 3px，用于提示/阻止明显偏移，不承诺源图像素级一致。

## 5. 所有元素进入清单

查看全图，把文字、箭头、图形、图例、角标、背景构件、原图与机制组件登记为 reference_inventory。每项包含 id、description、reference_box、route、element_ids，route 为 native/generated-image/source-image/master-element。一个组合可映射多个对象；所有项都必须有可追踪的成品对象，不得因为难画直接省略。

优先保留原始可用元素。简单语义图原生创建；复杂装饰/机制插画如难以原生还原，可用内置生图按母版/分页原图生成独立元素（透明背景按需要请求），或通过内置编辑工具提取该元素。保存实际资产，按测量 bbox 插入、调整大小和层叠关系。文字尽量另做原生文本；保留为图片的复杂内部细节明确不可逐路径编辑，但可替换移动。禁止整个机制被简化为几个空框，或让素材生图改掉拓扑。

reference_inventory 由实际看图建立，脚本不能自动证明清单覆盖原图全部细节。每页看图时单独做“未列入清单的可见元素”检查。必要省略必须先有用户明确同意，不能仅填技术原因。

## 6. 重建和双重核对

在底图上逐区域制作，逐项核对文字内容、基线/行距、边界、比例、元素数量、颜色、箭头和遮挡。用 master_slot 关联 title/body/caption 等文字角色及固定样式；同角色的字号/字重/对齐一致。分页字数变化时先修改非关键文案、调整合法换行或使用同体系内容 layout，不只缩小这一页标题。需要全局改变字号时统一改母版。

区域校准后移除临时底图，输出 clean 渲染，检查底图消失后是否暴露遗漏。保存 overlays/或 build/ 的对照证据（可用 HTML 的叠图/透明度交互，不用视觉近似评分冒充科学准确性），在 build/reconstruction-review.json 记录区域观察。正式 PPT 中不能有 pppt:underlay 对象；原始图放在项目 design/，不删原材料。

代码检查只是位置、尺寸、字号和清单关系检查，不能证明轮廓、颜色、视觉行距和科学拓扑正确。用户确认只针对母版选择，不要求每一页都等待批准；确认之后可连续执行。

```text
<python> scripts/reconstruction_tools.py compare --reference <设计图.png> --render <清洁PPT渲染.png> --out <新的对照.html> --canvas 1280 720
```

若底图不是满幅放置，compare 的 --frame 使用实际 image_frame 的 left top width height。工具只在本地 HTML 中显示两张原图和透明度滑块，不修改图像，也不自动声称视觉通过。


v1.5 更严格的默认流程见 [还原验收](fidelity-gates.md)：母版确认后还需最复杂样页的实际重建对照验收，之后分页自主执行；此前“仅母版确认即可连续重建”由本条更新。冻结参考图不可简化换稿，测量记录独立于构建。混合文字样式按 runs 保留，不能为全套角色统一把学校名等强调色/字重抹平。


v1.6 更新优先于本文旧版的机械坐标/差异清零约束：参考保留原样，允许授权范围内按真实素材、可读性、居中和均衡纠正布局；记录 adaptations 的原始 before 与目标 after，未解决问题仍阻断，合理调整可作为已解决差异。新增 alignment_constraints、paragraph.vertical_alignment 与 emphasis_scope=all，核对实际 PPT；完整字段与调整边界见 [灵活排版](adaptive-layout.md)。新项目 workflow_version="1.6"。
