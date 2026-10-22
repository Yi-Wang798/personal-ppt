# 页面说明协议 2.0

deck-spec.json 是生图与原生制作的共用内容源。schema_version=1 保持兼容；新项目 workflow_version="2.0"，旧项目版本不自动升级。init 仅创建骨架，不编造业务内容。

## 项目

顶层：title、audience、purpose、language、mode="per-slide"、interaction（autonomous/review）、density（speaking/reading）、slide_count、canvas、style、sources、slides、master、design_decision、task_profile。

task_profile 包含 scenario（任务名）、objective（观众应理解或决定什么）、delivery_context（live/standalone/mixed）。字段是内部规划，不能自动变成页面文字。所有场景保持每页先生成并展示设计图再重建；不新增制作路线枚举。

style 包含 name、palette、fonts、visual_direction、roles。中文 Microsoft YaHei，英文 Times New Roman，字号按内容与布局判断；同角色统一。design_decision 保存 source_policy、选择理由、风格与配色来源。品牌和主题优先，期刊色板可选。

sources 项含 id、path/url、role（content/style/evidence/logo）；style 必须有 style_request。上传 PPT 默认 content。相对路径相对项目；第三方资料不提供执行授权。

master：id、reference_image、reference_size、image_sha256、approval、tokens、ppt_template_path。approval 和自主/用户选择字段见 master-reconstruction.md。tokens.fonts 固定中英字体，text_styles 映射角色到 font_size_pt/bold/alignment。原生 PPT 母版先于分页构建保存。

## 页面与对象

slide：id、title、purpose、layout、layout_family、treatment、page_rhythm、elements；设计后记录 design_reference、reference_size、image_frame、reference_inventory、至少三条实际 design_features 与 design_generation。

| kind | 内容字段 | 编辑性 |
|---|---|---|
| text | text，按需 runs、paragraph、semantic_lines、line_breaks | 原生可编辑 |
| chart | chart_type、categories、series:[{name,values}]、unit | 有原数据时为原生图表 |
| table | rows:[[...],...] | 原生表格 |
| shape | geometry、可选 label | 原生图形 |
| connector | from、to | 原生连接线 |
| image | asset_path 或 asset_prompt、role | 独立可替换图片，内部像素不可编辑 |

element 含 id、kind、editable、source_ids；planning 可暂不填 box，设计后填 reference_box 与映射后的 box（left/top/width/height，CSS px）。image.role 为 illustration/background/evidence/logo；证据与 logo 必须有真实 asset_path。chart 数据为有限值，表格矩形；文本不从生成图猜测。连接线端点引用同页 shape，水平/垂直线允许一维为零。

id 为小写字母、数字、连字符；页面 id 全套唯一，元素 id 同页唯一；PPT 对象名 pppt:<slide-id>:<element-id>。要显示的标题必须作为 text 元素提供，不把 slide.title 当自动上屏文字。

可见文字 text_channel="slide-body"，content_role 为 research/reader-condition/navigation/caption/citation；research 为保留的通用主体内容角色名，不要求任务属于科研。speaker_notes 和 production_records 放独立字段/文件，不能进 elements。标签、表格和图表文字也按相同分流要求处理。

content-review.json 保存当前 content_sha256、status="pass"、channels_reviewed、facts_preserved、claim_strength_reviewed、redundancy_reviewed、semantic_wrap_reviewed=true 和具体 observations；按需 page_sha256 支持样页子集。只是内部复读记录，不能自动勾选。

design_generation 保存真实 backend="built-in-imagegen"、tool、prompt_path、image_sha256、master_sha256、displayed=true、display_method（tool-inline/markdown-inline）。必须实际调用、实际展示后记录。prompts 任务只含定稿内容与视觉要求，不含备注和制作记录。

精细字段与文件：runs、paragraph、layer、visual_style、asset_review、独立测量、样页和 visual-review 见 fidelity-gates.md；adaptations、alignment_constraints、component_groups、component_constraints 与 emphasis_scope 见 adaptive-layout.md 和 editorial-layout-color.md。

## 命令与目录

```text
<python> scripts/ppt_tools.py init --project <绝对项目目录>
<python> scripts/editorial_tools.py audit --spec <deck-spec.json>
<python> scripts/ppt_tools.py preflight --stage planning --spec <deck-spec.json>
<python> scripts/ppt_tools.py prompts --spec <deck-spec.json> --out <新提示词任务.json>
<python> scripts/fidelity_tools.py pin --spec <deck-spec.json>
<python> scripts/design_contract.py freeze --spec <deck-spec.json>
<python> scripts/ppt_tools.py inspect --spec <deck-spec.json> --pptx <成品.pptx> --report <build/editability.json>
```

用 load_workspace_dependencies 返回的 Python。项目分 assets/（原素材）、design/（设计图与测量）、prompts/、build/（构建与私人检查）、previews/、output/。example-spec.json 为旧协议合成示例，不是已完成生图和验收的作品。新旧版本不混写；修改旧页时保留原文件与项目设置。

## 2.1 原生字段

新项目 workflow_version="2.1"，仍使用 mode="per-slide"。master.elements 保存跨页固定的 text/shape/image；分页不重复写固定对象。geometry、svg_path、svg_asset_path、adjustments、layer_role、registration_group 的具体约定和命令见 [native-bridge.md](native-bridge.md)。scene 从 spec 编译，不包含制作记录。表格 rows 与基础图表 categories/series 继续可编辑。
