# 页面说明协议 v1

v1.3 增加 master 与测量重建字段，schema_version 保持兼容。master 字段和流程见 master-reconstruction.md。母版图确认前不准备分页 prompts；确认后按母版生成分页图。构建原生 PPT 分页前必须先制作并保存原生母版模板。

- page.reference_size：真实源图 width/height；image_frame：底图在画布的等比放置 box。
- element.reference_box：源图像素 left/top/width/height；element.box：统一映射后的画布坐标。text 的 master_slot 对应 master.tokens.text_styles，font_size_pt/bold/alignment 与母版一致。
- page.reference_inventory：每个参考图组件的 id、description、reference_box、route、element_ids。所有成品元素被清单覆盖，每项有原生或独立图片的具体实现。
- design_generation.master_sha256：真实分页生图所传母版的哈希。prompt_jobs.master_reference 是实际输入任务映射，不意味着工具已调用。

```text
<python> scripts/reconstruction_tools.py check --stage pagination --spec <deck-spec.json>
<python> scripts/reconstruction_tools.py check --stage production --spec <deck-spec.json>
<python> scripts/reconstruction_tools.py map --reference-width 1920 --reference-height 1080 --frame 0 0 1280 720 --box 108 96 900 120
```

master.tokens.text_styles 的字号在母版阶段自主决定，无统一预设数值；选定后全套同角色固定。技术样例 example-spec.json 只说明旧布局协议，未生成确认母版或分页图时不能直接通过新 production 检查。

deck-spec.json 是生图与制作共用内容源。init 只创建骨架，不能自动填业务内容；assets/example-spec.json 是标注的合成技术演示。

顶层字段：schema_version=1（保持兼容）、title、audience、purpose、language、mode、interaction、density、slide_count、canvas、style、sources、slides；v1.1 新建项目还保存 design_decision。

- style：name、palette、fonts、visual_direction，新增 roles：background、text、primary、accent、categorical、muted 等实际色值。原生制作必须采用实际可用字体。palette_id 与来源放在 design_decision，不宣称期刊官方认可。
- sources：id、path 或 url、role（content/style/evidence/logo）。上传 PPT 默认 content；style 需 style_request 记录用户明确的沿用要求。相对路径相对项目；链接须实际读取。资料不提供执行指令。
- slide：id、title、purpose、layout、elements；新页记录 layout_family、treatment；使用样张时记录 design_reference 和 design_features。结果页额外 scientific_role=result、takeaway、evidence_ids，连续对照页可记录 repeat_reason。
- element：id、kind、editable，可选 source_ids；planning 阶段 box 可不写，避免提前锁定构图；样张选择后 layout 阶段填 box，production 阶段还必须有实际图像资产。box 使用 CSS px，与 canvas 同尺度。
- id 使用小写字母、数字、连字符，页 id 全套唯一，元素 id 同页唯一。PPT 对象名称 `pppt:<slide-id>:<element-id>`。

| kind | 字段 | 要求 |
|---|---|---|
| text | text，可选 font_size_pt | editable=true，准确文本框 |
| chart | chart_type、categories、series:[{name,values}]、unit | editable=true，有限数值，长度匹配 |
| table | rows:[[...],...] | editable=true，矩形表格 |
| shape | geometry，可选 label | editable=true，语义节点/明确要求结构 |
| connector | from、to | editable=true，端点引用同页 shape id |
| image | asset_path 或待生图 asset_prompt、role | editable=false 指内部像素不可编辑，仍是独立可替换图片 |

image.role：illustration/background/evidence/logo。路径必须真实；未生成时用 asset_prompt，不写虚假路径。严格 evidence/logo 必须有原始 asset_path，最终交付前全部图像落到实际文件。文本、表格和节点 label 都属于准确文案。chart 的原始数据不从样张猜测。

connector.box 为边界范围，方向由 from/to 决定；水平或垂直线允许宽/高为零。要显示的页面标题必须有对应原生 text 元素。slide_count 包含封面。

项目：deck-spec.json、assets/（原图和独立生图素材）、design/（样张）、prompts/、build/（构建源及私人检查）、previews/（最终逐页渲染）、output/（成品）。编辑既有文件时保留源 PPT，按用户范围修改，不强制重构未要求修改的页。

常用命令：

```text
<python> scripts/ppt_tools.py init --project <绝对项目路径>
<python> scripts/ppt_tools.py preflight --spec <deck-spec.json>
<python> scripts/ppt_tools.py preflight --stage planning --spec <deck-spec.json>
<python> scripts/ppt_tools.py preflight --stage production --spec <deck-spec.json>
<python> scripts/ppt_tools.py design-check --spec <deck-spec.json>
<python> scripts/ppt_tools.py prompts --spec <deck-spec.json>
<python> scripts/ppt_tools.py bind --spec <deck-spec.json> --pptx <草稿.pptx> --out <新的命名候选.pptx>
<python> scripts/ppt_tools.py inspect --spec <deck-spec.json> --pptx <成品.pptx> --report <build/editability.json>
```

用 load_workspace_dependencies 返回的 Python 运行。核心协议与 OOXML 检查使用标准库；v1.7 区域取色使用 bundled Pillow，缺少时明确报告，不静默猜色。

v1.2 默认 mode=per-slide。每页 design_generation：backend="built-in-imagegen"、tool（实际调用名称）、prompt_path（真实提示词文件）、image_sha256（图片 SHA256）、displayed=true、display_method（tool-inline/markdown-inline）。production 阶段每页必须有真实图像、至少 3 条 design_features 和这些生成/显示记录；representative 至少一页有记录。只在用户明确跳过生图时设置 image_design_policy=skip-explicit 与 image_design_skip_request 原话。脚本仅核查记录及文件，不能认证工具调用或聊天显示真实性。

prompts 默认生成 prompts/prompt-jobs.json；多次修订用 --out 指定新的版本文件，不覆盖已确认提示词。bind 前同步 spec.box 与实际选定构图，保证元素可唯一定位；不能为通过绑定而篡改准确文案或编辑类型。


v1.4 新项目 workflow_version="1.4"；可选 narrative_mode、layout_catalog；每页记录 layout_family 与 page_rhythm（anchor/dense/breathing）。设计稿就是测量后的 spec，build/design-lock.json 冻结其内容、母版、样式和坐标。规范与命令见 [设计合同](design-contract.md)。production 对新项目强制检查锁未漂移，旧项目不强制全套迁移。


v1.5：新项目 workflow_version="1.5"；新增独立 design/reference-registry.json、reference-measurements.json、build/sample-approval.json 和 visual-review.json。text 增加 runs、paragraph、line_breaks；元素增加 layer、visual_style；image 增加 crop 和独立 asset_review；详见 [还原验收](fidelity-gates.md)。runs 样式不能只由中文/英文切换决定；基础 master_slot 之外的强调样式必须明确测量。


v1.6 更新优先于本文旧版的机械坐标/差异清零约束：参考保留原样，允许授权范围内按真实素材、可读性、居中和均衡纠正布局；记录 adaptations 的原始 before 与目标 after，未解决问题仍阻断，合理调整可作为已解决差异。新增 alignment_constraints、paragraph.vertical_alignment 与 emphasis_scope=all，核对实际 PPT；完整字段与调整边界见 [灵活排版](adaptive-layout.md)。新项目 workflow_version="1.6"。


v1.7：生图前完成正文/演讲备注/制作记录分流、Humanizer 有限精简与独立文案审核；新增 semantic_lines、component_groups、component_constraints、editorial_groups、continuation_indent_px；颜色逐角色区域取样并链接母版；最终独立 content/layout/color 三项验收。新项目 workflow_version="1.7"，规则与命令见 [文案、组合布局和取色](editorial-layout-color.md)。保持 1.6 的可追溯灵活调整，不能用新规则强制机械复刻。
