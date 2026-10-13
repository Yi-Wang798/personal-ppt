# 还原验收 v1.5

先读本文件再执行新项目。截图反馈表明：冻结 spec 不够，错误坐标/样式也能被原样导出并自检通过。新项目 workflow_version="1.5"。独立参考测量负责描述设计图，构建 spec 负责实现，成品报告从 PPTX 提取实际对象；不能由构建脚本生成三份一样的答案。

## 1. 参考图不可替换

每页设计图真实生成并展示后，在项目根 spec 中记录页码、design_reference、design_generation.image_sha256/displayed。完整设计图保留，不为降低难度生成简化图替换它。运行 fidelity_tools.py pin，创建一次性 design/reference-registry.json 和按原文件 SHA256 命名的 design/frozen/ 副本。pin 不覆盖已冻结记录；check 会核对冻结副本、当前设计图和测量哈希。

科学内容有错、真实证据放不下或文字密度不可执行时，先展示具体问题和修订设计图，经用户接受后另存项目版本，保留旧图、旧注册表及确认记录。不能重钉/删注册表/改测量只为了通过检查。上传原数据图必须在设计阶段按真实比例预留；结果页不得以生成图冒充证据。

## 2. 独立测量文件

逐页记录独立 reference_size 与 image_frame，与冻结图尺寸及实际映射一致。delivery 直接把测量的 reference_box 映射后与实际 PPT 对象比较，即使错误 spec.box 和错误成品互相吻合也应失败。

design/reference-measurements.json 由实际看冻结图测量得到，origin="visual-reference-measurement"；slides 中每项包含 id、reference_sha256、observations（具体区域与观察）、elements。elements 按对应 PPT 对象分解记录，不从 spec 或导出对象回填。允许登记后手动复制准确测量到 spec，但不得反过来让检查跟随错误构建值。

每个元素包含 id、kind、reference_box、layer（整数，底到顶）。背景必须分解为外边框、标题色带、内白底、分隔线、文字、箭头等独立对象，不用一个填色矩形替代多层。shape/connector 的 visual_style 明确 fill/stroke（#RRGGBB）、stroke_width_pt、dash（solid/dash/dot 等实际 DrawingML token），必要时 start_arrow/end_arrow。无填充用 fill_none=true，不用透明白色冒充；颜色、线宽不得统一写成 2px。实验组身份色单独记录到 group_color_map，生图到成品不得重新分配。

text 包含 text、runs、paragraph、line_breaks。每个 run 明确 text/font_family/font_size_pt/color/bold/italic。准确文字以业务材料为源；样式从冻结图测量。中文微软雅黑、英文 Times New Roman；同一句“学校名称蓝色加粗、学历黑色常规”需要分别建 run，不把整框套一个样式。字号自主测量，master_slot 表示基础语义角色，强调 run 可不同字重/颜色；显式字号变体先登记到母版文字规范，不能借变体逐页改标题。

paragraph 明确 alignment、margins_px（left/right/top/bottom）、line_spacing_pt、space_before_pt、space_after_pt。line_breaks 记录硬换行后的字符偏移，软换行在实际渲染中确认。文字 bbox 对齐仍需检查基线、行高、文本内边距和可见字形。若工具不能设置混合 runs/行距，读取当前 API 找实际支持方式；必要时拆成连续文字段并校准，保持段落可编辑，不能静默丢格式。

image 包含 crop.fit=contain 或 crop-background-only；subject_box（素材像素中的完整主体）与允许背景裁剪范围。优先等比 contain，不能裁瓶口、瓶底、仪器边缘、证据图图例或 AFM 色标刻度。asset_review 包含实际 asset_sha256、subject_complete=true、displayed=true、observations 和 preview:{path,sha256}；每个裁剪素材先独立展示并查看完整性，验收后才插入。复杂非证据元素可独立生图；科研证据仅用原图，主体缺失则重新提取。

## 3. 复杂样页先验收

母版通过不等于重建质量通过。全套设计图和独立测量完成后，选择实际最复杂的一页（通常混合文字、分层色带、原图、箭头/机制中至少三项），先重建这一页。不要固定选第 3/5 页或最简单封面。样页使用项目内 sample-spec.json：只选该页，slide_count=1，其余母版/参考数据不变。sample 预检允许没有批量验收记录；执行正式 finalizer 后得到真实一页 PPT、渲染图。

制作并展示设计图/实际 PPT 渲染并排图及叠图，列出实际差异。由用户明确认可还原方式后记录 build/sample-approval.json；此前不批量重建。该记录含 slide_id、complexity（三种实际特征）、approved、user_reply、pptx/reference/render/comparison/measurements 文件 {path,sha256}、displayed、observations、blockers、differences。measurements 指独立测量文件。样页文件或测量改了必须重新对照；既有相同文件的明确验收可复用，不重复询问。只写 approved=true 不能证明用户回复真实。

## 4. 逐页交付阻断

build/visual-review.json 顶层记录当前 pptx_sha256、measurements_sha256，slides 每页含 id、reference/render/comparison 的真实文件 {path,sha256}、displayed、observations、blockers、differences。comparison 使用 reconstruction_tools.py compare 创建真实并排/叠图；每页展示实际对照与差异清单。observations 按标题、面板、原图主体、标注/色标、连线与结论等实际区域写结果，不填“已检查，通过”。

blockers 必须逐项记录：missing_elements、text_overflow、subject_cropped、lost_emphasis、wrong_layers、changed_layout、wrong_group_colors、wrong_text_styles。未检查或任一为 true 都阻断；differences 未清零不能交付。无法修复时交付说明失败页和具体冲突，不能称整套完成；需要用户接受的实质修改先展示再修订版本，不抹掉原设计差异。

结构 pass 与视觉通过分开。delivery 检查参考与文件哈希、独立测量、实际 OOXML 的分段字体/颜色/字号/字重、可检查的段落间距、层级和线样式以及样页验收。继承样式无法解析时先显式设置或解决工具限制，不能默认通过。delivery 对视觉记录最多称 record-complete，不能替代真实看图，更不能把来自别的 PPT 的 PNG 标成当前渲染。渲染 provenance、实际换行、主体完整性、科学拓扑、箭头外观和像素还原仍须实际观察；不提供假的相似度分数。

```text
<python> scripts/fidelity_tools.py pin --spec <项目根 deck-spec.json>
<python> scripts/fidelity_tools.py check --spec <deck-spec.json>
<python> scripts/ppt_tools.py preflight --stage sample --spec <项目根 sample-spec.json>
<python> scripts/ppt_tools.py inspect --stage sample --spec <项目根 sample-spec.json> --pptx <样页.pptx> --report <样页结构报告.json>
<python> scripts/fidelity_tools.py sample --spec <deck-spec.json>
<python> scripts/design_contract.py freeze --spec <deck-spec.json>
<python> scripts/ppt_tools.py preflight --stage production --spec <deck-spec.json>
<python> scripts/reconstruction_tools.py delivery --spec <deck-spec.json> --pptx <最终.pptx> --review <build/visual-review.json>
```

本次改进针对截图反馈的执行漏洞，未取得截图所述原设计图、实际 PPT 与构建代码，不能声称已修复那一套十页成品。旧项目修复时明确升级到 1.5，保留参考和源 PPT，按用户范围施工；不得用关闭新版本 gate 的方式绕过验收。

仅当用户明确要求跳过参考图重建时沿用 reconstruction_policy=skip-explicit 与原话；生产预检核对原话后不套图片还原 gate。此类任务按 Presentations 的正式 finalizer 与逐页视觉验收交付，不调用本文件的还原 delivery，也不声称按图还原。不能自行设置 skip 解决困难。


v1.6 更新优先于本文旧版的机械坐标/差异清零约束：参考保留原样，允许授权范围内按真实素材、可读性、居中和均衡纠正布局；记录 adaptations 的原始 before 与目标 after，未解决问题仍阻断，合理调整可作为已解决差异。新增 alignment_constraints、paragraph.vertical_alignment 与 emphasis_scope=all，核对实际 PPT；完整字段与调整边界见 [灵活排版](adaptive-layout.md)。新项目 workflow_version="1.6"。


v1.7：生图前完成正文/演讲备注/制作记录分流、Humanizer 有限精简与独立文案审核；新增 semantic_lines、component_groups、component_constraints、editorial_groups、continuation_indent_px；颜色逐角色区域取样并链接母版；最终独立 content/layout/color 三项验收。新项目 workflow_version="1.7"，规则与命令见 [文案、组合布局和取色](editorial-layout-color.md)。保持 1.6 的可追溯灵活调整，不能用新规则强制机械复刻。
