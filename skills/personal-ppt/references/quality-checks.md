# 质量检查 2.0

检查在后台执行，发现具体问题先修复受影响页面。制作记录、技术限制和检查结论不写入正文。需要用户决定的问题集中说明，不把所有阶段变成批准流程。

## 内容与文件

定稿前核对来源、数据、名称、日期和判断强度；正文与备注、制作记录分开。运行 editorial_tools.py audit，并真实复读后保存 content-review.json。文风提示按语境判断，不用关键词、字数或 AI 分数替代内容判断。

planning 阶段允许坐标未定；layout 阶段检查版面；production 检查逐页真实生图、显示记录、母版、独立测量、设计锁、样页检查和颜色采样。运行 Presentations 的实际 finalizer，完成实际总页数和可编辑对象检查，不以 PPTX ZIP 能打开当作成品通过。

## 实际渲染

每页查看导出 PPT 的真实渲染，对照冻结设计图并检查清洁全页。核对文字断行、组件整体居中、同级元素间距、全部 runs 字重、线型、层次、素材比例与完整性。照片、复杂插画作为独立图片，不声称内部可编辑。

用 ppt_tools.py inspect 检查实际 OOXML，对象命名为 pppt:<slide-id>:<element-id>。保留结构记录和真实观察；脚本不能证明渲染画面好看。内容、布局、颜色分别记录具体问题或保留原因，不能生成没有看图依据的全套通过声明。

## 按任务检查

- 全部任务：错字、事实错误、缺元素、溢出、遮挡、图像变形、颜色与格式损失、文件损坏。
- 有业务数据：来源→spec→导出图表核对，保留单位、计算口径和时间范围。
- 科研：再读 scientific-design.md，核对证据、样本量、误差与推断。
- 商业：核对金额、计算前提和承诺；教学核对概念与步骤；品牌任务核对实际规范。

无需给纯文字或无数据页制造统计检查。文风和布局建议不机械阻断；确切错误与尚未解决的视觉问题修好后再交付。合理局部优化按调整后的目标检查，不能因为像素不同就返工。

## 命令

```text
<python> scripts/ppt_tools.py preflight --stage production --spec <deck-spec.json>
<python> scripts/reconstruction_tools.py check --stage production --spec <deck-spec.json>
<python> scripts/ppt_tools.py inspect --spec <deck-spec.json> --pptx <最终.pptx> --report <build/editability.json>
<python> scripts/reconstruction_tools.py delivery --spec <deck-spec.json> --pptx <最终.pptx> --review <build/visual-review.json>
```

新版提高首轮可用性，通过自动内部修正减少用户返工，不承诺任意任务一次完美。旧项目保持原 workflow_version；不因插件升级要求全套重制。
