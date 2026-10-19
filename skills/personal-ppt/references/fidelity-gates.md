# 参考、样页与交付检查 2.0

保留已展示的设计图，不能为方便构建换成简化稿。`fidelity_tools.py pin` 一次性保存 design/reference-registry.json 和 design/frozen/；改设计时另存版本并说明实际变化。

## 独立测量

design/reference-measurements.json 的 origin="visual-reference-measurement"。slides 每页记录 id、reference_sha256、reference_size、image_frame、observations、elements 与需要的 group_color_map。元素含 id、kind、reference_box、box、layer，不能从构建 spec 复制数值冒充观察。

text 记录每段 runs 的 text、font_family、font_size_pt、color、bold、italic；paragraph 保存 alignment、margins_px、line_spacing_pt、space_before_pt、space_after_pt，适用时 vertical_alignment、continuation_indent_px；line_breaks 记录真实硬换行。整段加粗应覆盖全部中英文 runs。字号来自母版与内容判断。

shape/connector 的 visual_style 记录实际 fill/stroke、stroke_width_pt、dash 和适用箭头端点；无填充用 fill_none。背景按实际构成分层，不用一个填色矩形替代标题条、内白底和边框。

image 用 contain 或只裁多余背景；subject_box、crop 与 asset_review 记录主体完整、实际查看、观察及预览文件 {path,sha256}。真实数据图、证据、产品图和 logo 保留原始文件，复杂装饰插画可独立生图。design_generation.displayed 指在聊天中展示设计图；asset_review.displayed 指实际查看素材预览，不要求为每项素材询问用户。

局部调整使用 adaptations 的 before/after/reason，细节见 adaptive-layout.md。比较的是有效调整目标，不要求机械复制参考图缺陷。

## 代表性样页

先做本项目最有代表性的复杂页，保存 build/sample-approval.json（文件名为兼容保留）。每项文件记录 {path,sha256}：pptx、reference、render、comparison、measurements。另存 slide_id、complexity、displayed、observations、blockers、differences。displayed 表示实际查看了对照。

- autonomous：reviewed=true、reviewer="agent"，user_reply 留空；内部查看和修正后继续，不伪造 approved 或用户回复。
- review：approved=true、user_reply 为真实验收回复；等待用户认可后继续。

2.0 complexity 按实际内容至少一项，可为 text-layout、table、mixed-text、layered-panel、source-image、connectors、chart、mechanism。没有复杂图形的任务可以检查文字布局，不为凑数增加三种装饰。旧项目仍保留原来的三特征和用户确认要求。

样页文件或独立测量变化后重新对照；review 模式涉及已验收内容变化时再请用户确认。通过内部检查不能宣称用户已经看过或批准。

## 交付

visual-review.json 绑定当前 pptx_sha256 和 measurements_sha256。slides 每项含 id、reference/render/comparison 的文件记录、displayed、observations、blockers、differences；review_sections.content/layout/color 各含 passed 和实际 observations。内部查看并修正后保存，不要求用户逐页签字。

blockers：missing_elements、text_overflow、subject_cropped、lost_emphasis、wrong_layers、changed_layout、wrong_group_colors、wrong_text_styles。确切错误未修复时不标完成。无未解决差异时 differences=[]；合理调整记录 status="resolved-design-adjustment" 与 adaptation_id，并绑定 adaptation_ids、adaptations_sha256。

实际执行 reconstruction_tools.py delivery，核对 OOXML 与文件。检查记录只是依据，不能自动证明内容准确、图片来源或视觉质量。不把这些字段、哈希和检查提醒写进幻灯片。
