# 参考优先，合理调整

生成图片是设计提案，不是最终答案。优先级为：真实内容与素材完整性 → 可读性及无溢出 → 对齐、匀称与全套风格 → 尽量还原参考图。参考图若出现歪斜、错误居中、文字不足以容纳、图像比例失真或错误字重，应纠正，不为了贴图复刻缺陷。冻结图保留用于追溯，不要求每次局部调整都重新生整页或请用户确认；超出用户要求的全局主题、内容含义或页数变化先说明影响；review 模式涉及已确认方向的变化再请用户确认。

## 居中和加粗

居中分三层：对象在所属区域居中、文字在文本框内水平居中、文字在文本框内垂直居中。标题按选定母版的意图，不能一律居中；正文段落通常左对齐。短标签、图注、对比标题和节点文字需要居中时设置 paragraph.alignment=center、vertical_alignment=center，明确 margins_px，避免不对称内边距导致视觉偏移。对象中心通过 alignment_constraints 指定所属 panel/column/figure 区域，不拿整页中心替代局部容器中心；实际 PPT 对象检查该约束，字形的视觉中心仍看渲染。纵横比不同的两张证据图可等高或共享基线，不要求拉伸成一样宽。

整段加粗设置 emphasis_scope=all，所有中英文 runs 都明确 bold=true，不只第一个 run 或中文部分加粗。局部强调设置 emphasis_scope=runs 并逐段处理；材料决定哪些信息重要，不把整页正文都加粗。检查导出的实际文字样式，不能只相信 text.style；字体中文微软雅黑、英文 Times New Roman。母版角色一致，同类标题保持字号与字重；局部强调和经记录的可读性调整不能被母版默认样式覆盖。

## 真实图片进入后的排版

先查看原图的真实宽高比、主体、图例、刻度和内白边，再决定图片占位区。完整等比放入后若太小或留白失衡，先扩大证据区域、移动相邻说明、调整列宽与间距，必要时改变单页内容区结构并同步箭头/图注。原始内容不删、不改数据、不改变机制拓扑、不裁掉主体或标尺。可裁的仅是经查看确认的多余背景。

图注与图靠近，标签与所属对象绑定，结论可移到较宽区域；优先合理换行/扩大文本框，再优化行距和局部密度，不为塞进去盲目缩小所有文字。若仍不可读，说明实质冲突；增加页数或改变用户指定内容范围需用户决定。统一壳、分类颜色和文字层级，不强迫每页网格与参考坐标毫无差别。

## 可追溯的局部修正

新项目 workflow_version="2.0"；旧 1.6/1.7 项目继续采用原版本。原 reference-measurements.json 与冻结图不变；每页 adaptations 保存各项调整。category 为 source-fit/text-readability/alignment/balance/reference-error；每项 id、element_id、reference_sha256、reason、observations、changes。changes 仅允许 box、paragraph、runs、line_breaks，每项含 before（原始独立测量或等比映射的 box）与 after（新的目标）。不能修改 text/kind/source_ids/数据/机制连接/实验组颜色或替换证据图片；如确需科学修改，走明确的内容修订流程。runs 局部排版调整保留原分段文字、字体、颜色，只调整字号、粗斜体；整段加粗逐个 run 设置。

每个字段只记一次完整 before→after，不用一串互相覆盖的补丁。调整后 spec 保存 after，构建源读取 spec；更新设计锁、重新渲染成品。同一页多个相关对象分别记录；不得只移动图片却让图注或箭头悬空。全套标题等角色需要改变时统一更新母版，避免局部调整制造全套漂移。

示例（坐标仅演示）：

```json
{
  "id": "fit-evidence-01",
  "element_id": "evidence",
  "reference_sha256": "实际冻结图 SHA256",
  "category": "source-fit",
  "reason": "原机制图较宽，旧区域完整放入后标注过小",
  "observations": ["扩大图区并右移说明后，标注清晰、主体完整、与相邻图共享基线"],
  "changes": {"box": {
    "before": {"left":80,"top":180,"width":400,"height":250},
    "after": {"left":80,"top":180,"width":520,"height":250}
  }}
}
```

alignment_constraints 示例：[{"axis":"horizontal","element_ids":["caption"],"container_box":{"left":80,"top":180,"width":520,"height":250},"tolerance_px":3}]。容器为最终布局区域，不必是原图位置。

## 验收看最终效果

未解决差异仍阻断；合理调整记录为 differences:[{status:"resolved-design-adjustment",adaptation_id:"对应调整 id",description:"实际变更"}]。visual-review 对每页含 adaptation_ids 和 adaptations_sha256（用 adaptive_layout.digest(page.adaptations)）；哈希绑定当前调整。这样差异无需假装为零，且未知偏移不能借“灵活调整”逃过检查。changed_layout 表示未经解释或破坏内容关系的改版，有有效记录且实际视觉改善的局部优化可为 false。

看并排/叠图找遗漏，也看不带参考底图的最终清洁渲染评估阅读效果、均衡、对齐和图文比例。视感优先于机械像素相似。独立测量保留原样；检查按有效调整后的目标核对实际 PPT，不改原测量来消除错误。复杂样页的已确认版若被修改需重渲染对照；其余页的授权局部优化不逐页请求确认。

数值检查不能自动判断美观或光学中心，也不能验证作者观察是否真实；最终仍需实际看图。旧 1.5 项目需升级 workflow_version 才采用此弹性机制，旧严格模式保持兼容。
